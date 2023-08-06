import json
import pathlib
import ssl
from urllib import error, request

from . import exceptions


def api_upload(
    cache_file: pathlib.Path, root: str, remote_data, headers: dict, deploy: bool
):
    """
    Yields the result from `simple_api_uploader`. Wraps errors into a
    `~.exceptions.CommandFail` exception.

    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

    :returns: A generator

    """
    try:
        yield from simple_api_uploader(cache_file, root, remote_data, headers, deploy)
    except exceptions.Fail as err:
        raise exceptions.CommandFail(err)
    except error.HTTPError as err:
        raise exceptions.CommandFail(
            f"{err}: {root}: {err.read().decode(errors='ignore')}"
        )
    except error.URLError as err:
        raise exceptions.CommandFail(f"{err}: {root}")


def simple_api_uploader(
    cache_file: pathlib.Path, root: str, remote_data, headers: dict, deploy: bool
):
    """
    A simple uploader. No resume-support. Will not handle transfer errors.

        Yield protocol:

        - If type is `str`: log message
        - If type is `dict`: progress info

    .. code-block:: pycon

        >>> def gen():
        ...   yield from simple_api_uploader(cache_file, remote_data, root, headers)

        >>> for res in gen()
        ...     print(res)

    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

    :returns: A generator
    """

    prefix = remote_data.get("url")
    token = remote_data.get("token")
    insecure = remote_data.get("insecure", False)

    if deploy:
        endpoint = f"{prefix}/deploy/zip/{root}"
    else:
        endpoint = f"{prefix}/upload/zip/{root}"

    headers["Token"] = token
    req = request.Request(url=endpoint, headers=headers, data=cache_file.read_bytes())

    context = ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    yield {"progress": 0}
    yield f"uploading {root}"
    res = request.urlopen(req, context=context)

    buffer = " "
    payload = ""
    yield f"response from {prefix}"
    while buffer:
        buffer = res.readline(1024).decode(errors="ignore")
        if buffer.startswith("//"):
            yield f"      {buffer[2:].strip()}"
        else:
            payload += buffer

    if not json.loads(payload)["result_code"] == 0:
        raise exceptions.CommandFail(f"Upload failed: {payload}")

    yield {"progress": 100}
    if deploy:
        yield "upload and deployment complete"
    else:
        yield "upload complete"


def api_check_is_uploaded(root: str, shasum: str, tag: str, remote_data) -> bool:
    """
    Calls `simple_api_check_is_uploaded` and returns the result. Wraps errors into a
    `~.exceptions.CommandFail` exception.

    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``.
    """
    try:
        return simple_api_check_is_uploaded(root, shasum, tag, remote_data)
    except exceptions.Fail as err:
        raise exceptions.CommandFail(err)
    except error.HTTPError as err:
        raise exceptions.CommandFail(
            f"{err}: {root}: {err.read().decode(errors='ignore')}"
        )
    except error.URLError as err:
        raise exceptions.CommandFail(f"{remote_data['url']}: {err}")
    except Exception as err:
        raise exceptions.CommandFail(f"{root}: {repr(err)}")


def simple_api_check_is_uploaded(root: str, shasum: str, tag: str, remote_data) -> bool:
    """
    Checks ``api/v1/list/zip/<root>`` for a matching shasum and tag value.

    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``

    :returns: `True` if both shasum and tag match.
    """
    prefix = remote_data.get("url")
    token = remote_data.get("token")
    insecure = remote_data.get("insecure", False)

    endpoint = f"{prefix}/list/zip/{root}"

    context = ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    headers = {"Token": token}
    req = request.Request(url=endpoint, headers=headers)
    with request.urlopen(req, context=context) as resp:
        result_str = resp.read()

    result = json.loads(result_str)

    if root not in result:
        return False

    if shasum not in result[root]:
        return False

    if tag:
        details = result[root][shasum]
        if "tag" not in details:
            return False
        if not tag == details["tag"]:
            return False
    return True


def api_deploy(root: str, remote_data, headers: dict):
    """
    Yields the result from `simple_api_deploy`. Wraps errors into a
    `~.exceptions.CommandFail` exception.

    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

    :returns: A generator

    """
    try:
        yield from simple_api_deploy(root, remote_data, headers)
    except exceptions.Fail as err:
        raise exceptions.CommandFail(err)
    except error.HTTPError as err:
        raise exceptions.CommandFail(
            f"{err}: {root}: {err.read().decode(errors='ignore')}"
        )
    except error.URLError as err:
        raise exceptions.CommandFail(f"{err}: {root}")


def simple_api_deploy(root: str, remote_data, headers: dict):
    """
    Send a GET request to ``/api/v1/deploy/zip/<root>`` to start a deploy.

        Yield protocol:

        - If type is `str`: log message
        - If type is `dict`: progress info

    .. code-block:: pycon

        >>> def gen():
        ...   yield from simple_api_deploy(remote_data, root, headers)

        >>> for res in gen()
        ...     print(res)

    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

    :returns: A generator
    """

    prefix = remote_data.get("url")
    token = remote_data.get("token")
    insecure = remote_data.get("insecure", False)

    endpoint = f"{prefix}/deploy/zip/{root}"

    headers["Token"] = token
    req = request.Request(url=endpoint, headers=headers)

    context = ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    yield {"progress": 0}
    yield f"deploying {root}"
    res = request.urlopen(req, context=context)

    buffer = " "
    payload = ""
    yield f"response from {prefix}"
    while buffer:
        buffer = res.readline(1024).decode(errors="ignore")
        if buffer.startswith("//"):
            yield f"      {buffer[2:].strip()}"
        else:
            payload += buffer

    if not json.loads(payload)["result_code"] == 0:
        raise exceptions.CommandFail(f"Deploy failed: {payload}")

    yield {"progress": 100}
    yield "deployment complete"
