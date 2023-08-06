from . import (
    deploy_state,
    downloaders,
    exceptions,
    hooks,
    store_payload,
    tags,
    unpack_payload,
    verify_payload,
)


def client_install_zip_sequence(
    install_data: dict,
    keep_on_disk: int,
    remote_data: list[dict],
    requires_data: dict,
    extra_data: dict,
):
    """
    Handle unpacking/installation of zip files in client computers.

    Returns a generator.

        Yield protocol:

        - if type is `str`: log message.
        - if type is `dict`: result or progress.

    :param dict[str, str] install_data: install path and cache path
    :param list[dict] remote_data: list of remote url and token
    :param dict[str, str] requires_data: root and sha246
    :return: A generator
    """
    # requires_data: dict[str, str],

    install_section = install_data["install_section"]
    install_root = install_data["install_root"]
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
                "Only tag or sha256 is supported in the [requires] section. "
                f"ie. {root} = sha256:AABBCC"
            )

        yield f"using cache_root: {cache_root}"
        already_downloaded = False
        try:
            cache_file, cache_id, tag = store_payload.find_file_from_headers(
                cache_root, root, headers
            )
            already_downloaded = True
            yield f"{root} already downloaded."
        except exceptions.CacheNotFound:
            cache_file, cache_id, tag = yield from downloaders.api_download(
                cache_root, remote_data, root, headers
            )
        except exceptions.Fail as err:
            raise exceptions.CommandFail(err)

        if not already_downloaded:
            if keep_on_disk > 0:
                yield from store_payload.auto_delete(cache_root, keep_on_disk, root)

            root_dir_name = unpack_payload.extract_root_dir_name(cache_file)
            if root in extra_data:
                zip_root = extra_data[root].get("Zip-Root", root_dir_name)
            else:
                zip_root = root_dir_name
            yield from verify_payload.verify_root(root_dir_name, root, zip_root)

            if tag:
                yield f"update tag: {tag}"
                tags.store(root, cache_id, tag, cache_root)

        yield f"using install_root: {install_root}"

        transform_root = hooks.transform_root(install_section, root, locals())
        transformed_root = transform_root if transform_root else root

        state_config, *_ = deploy_state.get_config(install_root)
        if state_config.has_option(transformed_root, "source_hash"):
            if state_config.get(transformed_root, "source_hash") == cache_id:
                if transform_root:
                    yield f"{root} already installed as {transformed_root}."
                else:
                    yield f"{root} already installed."
                continue

        yield from unpack_payload.unpack(cache_file, install_root, transformed_root)

        deploy_state.store(
            transformed_root,
            cache_file,
            cache_id,
            install_root,
        )
        yield f"{transformed_root} installation complete."
