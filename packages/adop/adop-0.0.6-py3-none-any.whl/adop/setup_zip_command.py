import argparse

from . import zip_import, zip_install, zip_upload


class register:
    """
    A simple decorator to register sub parsers, but also
    acts as a singelton. Get a list of sub parsers by
    calling `register.subparsers` from the `main` function
    """

    subparsers = []
    "List of registered subparsers"

    @classmethod
    def subparser(cls, w):
        "Register sub parser"
        cls.subparsers.append(w)
        return w


def setup(subparsers: argparse.Action):
    """
    Sub parser for the ``zip`` argument.
    """
    setup_v1(subparsers, "zip", "Zip commands, latest version")
    setup_v1(subparsers, "zip-v1", "Zip commands v1 (this is the latest version)")


def setup_v1(subparsers: argparse.Action, name: str, help: str):
    """
    Sub parser for the ``zip-v1`` argument.
    """
    parser = subparsers.add_parser(name, help=help)

    subparsers = parser.add_subparsers(
        title="Commands", description="Additional help for commands: {command} --help"
    )

    # get all registered sub parsers and call its function
    for setup in register.subparsers:
        setup(subparsers)


@register.subparser
def setup_install_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``zip install`` argument.
    """
    parser = subparsers.add_parser("install", help="Install zip-packages")
    # path_or_file
    parser.add_argument(
        "file",
        type=str,
        default="./requires.ini",
        nargs="?",
        help="Install from the given requires.ini file",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.add_argument(
        "-r",
        "--remote",
        dest="remote",
        type=str,
        action="append",
        help="""Install from the given remote.
        Remotes have to be configured in adop.ini. [default: local]""",
    )
    parser.add_argument(
        "-i",
        "--install",
        dest="install",
        type=str,
        default="",
        help="""Install to the given location.
        Locations have to be configured in adop.ini. [default: basedir]""",
    )
    parser.set_defaults(func=zip_install.install)


@register.subparser
def setup_upload_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``zip upload`` argument.
    """
    parser = subparsers.add_parser("upload", help="Upload zip-packages")
    # path_or_file
    parser.add_argument(
        "file",
        type=str,
        default="./requires.ini",
        nargs="?",
        help="Upload from the given requires.ini file to REMOTE",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.add_argument(
        "-d",
        "--deploy",
        dest="deploy",
        action="store_true",
        help="Upload and deploy the zipfile on REMOTE. Do not deploy if "
        "already uploaded.",
    )
    parser.add_argument(
        "--force-upload",
        dest="force_upload",
        action="store_true",
        help="Force upload zipfile to REMOTE. Deploy on REMOTE if --deploy is set.",
    )
    parser.add_argument(
        "--force-deploy",
        dest="force_deploy",
        action="store_true",
        help="Force a deploy request on REMOTE. Only upload zipfile "
        "if missing on REMOTE",
    )
    parser.add_argument(
        "-r",
        "--remote",
        dest="remote",
        type=str,
        action="append",
        help="""Upload from the given remote.
        Remotes have to be configured in adop.ini. [default: local]""",
    )
    parser.add_argument(
        "-i",
        "--install",
        dest="install",
        type=str,
        default="",
        help="""Upload from the given location.
        Locations have to be configured in adop.ini. [default: basedir]""",
    )
    parser.set_defaults(func=zip_upload.upload)


@register.subparser
def setup_import_v1(subparsers: argparse.Action):
    """
    Sub parser for the ``zip import`` argument.
    """
    parser = subparsers.add_parser(
        "import", help="Import zip-packages into the local cache"
    )
    # path_or_file
    parser.add_argument(
        "requiresfile",
        type=str,
        default="./requires.ini",
        nargs="?",
        help="Update the given requires.ini file with imported zip package",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        type=str,
        default="~/.adop/adop.ini",
        help="Path to config [default: ~/.adop/adop.ini]",
    )
    parser.add_argument(
        "--cwd",
        dest="cwd",
        type=str,
        default=".",
        help="Work dir [default: .]",
    )
    parser.add_argument(
        "-i",
        "--install",
        dest="install",
        type=str,
        default="",
        help="""Import into to the given "install-location"-cache.
        Locations have to be configured in adop.ini. [default: basedir]""",
    )
    parser.add_argument(
        "-r",
        "--remote",
        dest="remote",
        type=str,
        action="append",
        help="""Import from the given remote.
        Remotes have to be configured in adop.ini. [default: local]""",
    )
    parser.add_argument(
        "-p",
        "--package",
        dest="root",
        type=str,
        required=True,
        default="root",
        help="The root name of the import",
    )
    parser.add_argument(
        "-f",
        "--zip-file",
        dest="zipfile",
        type=str,
        default="",
        help="Path or URL of the zip-file to be imported. This option "
        "overrides the --remote option",
    )
    parser.add_argument(
        "--insecure",
        dest="insecure",
        action="store_true",
        help="Skip SSL verification for the --zip-file option.",
    )
    parser.add_argument(
        "-t",
        "--zip-tag",
        dest="ziptag",
        type=str,
        required=True,
        default="latest",
        help="A tag to associate with the import",
    )
    parser.add_argument(
        "-z",
        "--zip-root",
        dest="ziproot",
        type=str,
        default="",
        help="Name of the root dir in zip-file. Use if dir name differs"
        " from --package name.",
    )
    parser.set_defaults(func=zip_import.zip_import)
