import json
import os

from . import (
    exceptions,
    parse_config,
    store_payload,
    unpack_payload,
    uploaders,
    zip_install,
)


def upload(
    file: str,
    config: str,
    cwd: str,
    remote: list[str],
    install: str,
    deploy: bool,
    force_upload: bool,
    force_deploy: bool,
):
    """
    Parses :term:`root` data from `file`, finds the zip-files at the `install` location,
    and uploads the files to `remote`.
    """

    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    abs_conf_path = os.path.abspath(os.path.expanduser(config))
    local_config = parse_config.parse(abs_conf_path, "", "")

    uploader = Uploader(local_config)

    requires_file_data = uploader.parse_requires_file(file)
    install_data = uploader.parse_install_to(install, requires_file_data)
    remote_data = uploader.parse_remotes(remote, requires_file_data)

    requires_data = requires_file_data["requires"]
    uploader.upload(
        install_data, remote_data, requires_data, deploy, force_upload, force_deploy
    )


class Uploader(zip_install.RequireFile):
    """
    A subclass of `.zip_install.RequireFile` that add a method for uploading
    zip-files to given `remote`.
    """

    def upload(
        self,
        install_data,
        remote_data,
        requires_data: dict,
        deploy: bool,
        force_upload: bool,
        force_deploy: bool,
    ):
        """
        Iterates over `gen` and prints the result to stdout.

        :param dict[str, str, str] install_data:
           A dict containing ``"install_section"``, ``"install_root"``
           and ``"cache_root"``.

        :param list[dict] remote_data:
           A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

        """

        _handle_zip = self.gen(
            install_data, remote_data, requires_data, deploy, force_upload, force_deploy
        )

        try:
            for res in _handle_zip:
                if isinstance(res, dict):
                    if "root" in res:
                        print(f"Requires: {res['root']}")
                    elif "result" in res:
                        print(f"{json.dumps(res)}")
                else:
                    print(f"          {res}")
        except exceptions.CommandFail as err:
            print("          ERROR:")
            raise exceptions.CommandFail(f"             {err}")

    def gen(
        self,
        install_data,
        remote_data,
        requires_data: dict,
        deploy: bool,
        force_upload: bool,
        force_deploy: bool,
    ):
        """
        Iterates over the data in `requires_data`. Checks the zip-files in the local
        cache given in `install_data`. Checks if the zip-files is available in
        the remote api. Uploads the missing zip-files. Yields progress and result.

            Yield protocol:

            - If type is `str`: log message
            - If type is `dict`: progress info

        :param dict[str, str, str] install_data:
           A dict containing ``"install_section"``, ``"install_root"``
           and ``"cache_root"``.

        :param list[dict] remote_data:
           A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

        :returns: A generator

        """
        cache_root = install_data["cache_root"]

        for root, shasum in requires_data.items():
            yield {"root": root}  # first result: returns only root
            yield f"checking {root}={shasum[:15]}..."

            if shasum.startswith("tag:"):
                headers = {"Zip-Tag": shasum.split(":", 1)[1].strip()}
            elif shasum.startswith("sha256:"):
                headers = {"Zip-Sha256": shasum.split(":", 1)[1].strip()}
            else:
                raise exceptions.CommandFail(
                    "Only sha256 is supported in the [requires] section. "
                    f"ie. {root} = sha256:AABBCC"
                )

            yield f"using cache_root: {cache_root}"
            try:
                cache_file, shasum, tag = store_payload.find_file_from_headers(
                    cache_root, root, headers
                )
            except exceptions.Fail as err:
                raise exceptions.CommandFail(err)
            zip_root = unpack_payload.extract_root_dir_name(cache_file)
            headers["Zip-Root"] = zip_root

            for remote_data_item in remote_data:

                if not force_upload and uploaders.api_check_is_uploaded(
                    root, shasum, tag, remote_data_item
                ):
                    yield f"{root} already uploaded to {remote_data_item['url']}"
                    if force_deploy:
                        yield from uploaders.api_deploy(
                            root,
                            remote_data_item,
                            headers,
                        )
                else:
                    yield from uploaders.api_upload(
                        cache_file,
                        root,
                        remote_data_item,
                        headers,
                        deploy or force_deploy,
                    )
