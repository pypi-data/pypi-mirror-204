import configparser
import os
import pathlib

from . import parse_config, zip_install

LINE_IDENT = "         "


def zip_import(
    requiresfile: str,
    config: str,
    cwd: str,
    remote: list[str],
    install: str,
    root: str,
    zipfile: str,
    ziptag: str,
    ziproot: str,
    insecure: bool,
):
    """
    Get a :term:`root` and zip-file from args and imports it into the given install location.
    Updates the given requires-file with the imported file.
    """
    if cwd and not cwd == ".":
        os.chdir(os.path.expanduser(cwd))

    abs_conf_path = os.path.abspath(os.path.expanduser(config))
    local_config = parse_config.parse(abs_conf_path, "", "")

    importer = Importer(local_config)

    try:
        print(f"Verify import: {root}")
        requires_file_data = importer.parse_requires_file(requiresfile)
        install_data = importer.parse_install_to(install, requires_file_data)
        remote_data = importer.parse_remotes(remote, requires_file_data)
        if zipfile:
            # replace remote data with direct import
            remote_data = importer.create_remote_data(zipfile, insecure)
        requires_data = importer.create_requires_data(root, ziptag)
        extra_data = importer.create_extra_data(root, ziproot)

        importer.install(install_data, remote_data, requires_data, extra_data)
        importer.update_requires_file(pathlib.Path(requiresfile), requires_data)
    except Exception as err:
        raise SystemExit(f"{LINE_IDENT} {err}")


class Importer(zip_install.Installer):
    """
    A subclass of `.zip_install.RequireFile` that add a method for importing
    zip-files into given `install` location.
    """

    @staticmethod
    def create_remote_data(zip_file: str, insecure: bool) -> list[dict]:
        zip_path = pathlib.Path(zip_file)
        if zip_path.is_file():
            url = zip_path.absolute().as_uri()
        else:
            url = zip_file
        return [{"url": url, "insecure": insecure, "token": "", "direct": True}]

    @staticmethod
    def create_requires_data(root: str, zip_tag: str) -> dict:
        return {root: f"tag:{zip_tag}"}

    @staticmethod
    def create_extra_data(root: str, zip_root: str) -> dict:
        return {root: {"Zip-Root": zip_root}}

    def update_requires_file(self, requires_file: pathlib.Path, requires_data: dict):
        """
        add/update a line to the requires section
        """
        if not requires_file.is_file():
            return

        config = configparser.ConfigParser(
            allow_no_value=True,
            comment_prefixes=["/"],
            delimiters=["="],
        )
        config.optionxform = lambda option: option

        config.read_string(requires_file.read_text())
        config.read_dict({"requires": requires_data})
        with requires_file.open("w") as f:
            config.write(f)
            print(f"{LINE_IDENT} update {requires_file}")
