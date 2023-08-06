import configparser
import json
import os
import pathlib
from argparse import ArgumentParser

from .. import __version__, logging


def main():
    "Entrypoint for the ``python -m adop.tool.hg`` command"
    logging.setup_logging()
    tool_parser = ArgumentParser(add_help=True)
    tool_parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"adop.tool.hg {__version__}",
        help="print version and exit",
    )
    tool_parser.add_argument("-r", "--get-remote", action="store_true")
    args = tool_parser.parse_args()

    if args.get_remote:
        print(get_remote_from_hg())
    else:
        tool_parser.print_help()


def get_destination() -> str:
    """
    Reads the environment variable HG_PATS and parses it to a list.
    return the first element in the list, or the word ``default``
    if the list is empty. HG_PATS is set by the ``hg push`` command.

    :returns: the destination of the ``hg push`` command
    """
    remote_string = os.environ.get("HG_PATS", "[]")
    remotes = json.loads(remote_string.replace("'", '"'))
    if remotes and isinstance(remotes, list):
        remote = remotes[0]
        return remote
    return "default"


def get_hgrc() -> configparser.ConfigParser:
    """
    Parses the ``.hg/hgrc`` file into a configparser if it exists.

    :returns: a configparser of the ``hgrc`` file
    """
    cp = configparser.ConfigParser()
    hgrc_file = pathlib.Path(".hg/hgrc")
    if hgrc_file.is_file():
        cp.read_string(hgrc_file.read_text())
    return cp


def get_remote_from_hg() -> str:
    """
    Translates a hg destination path to a adop remote.
    Useful in combination with the ``hg pre-push`` hook.

    A new section ``[adop:remotes]`` is needed in the ``hgrc``
    file for this translation to work.

    Example of hgrc:

    - Windows

      .. code-block:: ini

        [paths]
        default = https://hg.server1.local
        server1 = https://hg.server1.local
        server2 = https://hg.server2.local

        [adop:remotes]
        default = remote1
        server1 = remote1
        server2 = remote2

        [hooks]
        update.adop = py -um adop zip install requires.ini -r remote1 -r remote2
        pre-push.adop = for /f %i in ('py -um adop.tool.hg -r') do py -um adop zip upload requires.ini -r %i


    - Linux

      .. code-block:: ini

        [paths]
        default = https://hg.server1.local
        server1 = https://hg.server1.local
        server2 = https://hg.server2.local

        [adop:remotes]
        default = remote1
        server1 = remote1
        server2 = remote2

        [hooks]
        update.adop = python -m adop zip install requires.ini -r remote1 -r remote2
        pre-push.adop = python -m adop zip upload requires.ini -r $(python3 -m adop.tool.hg -r)

    """
    dest = get_destination()
    hgrc = get_hgrc()
    remote_map = {}
    if hgrc.has_section("adop:remotes"):
        for option_name, option in hgrc["adop:remotes"].items():
            remote_map[option_name] = option
    if hgrc.has_section("paths"):
        for option_name, option in hgrc["paths"].items():
            if dest in (option_name, option):
                return remote_map.get(option_name, option_name)
    return remote_map.get(dest, dest)


if __name__ == "__main__":
    main()
