import pathlib
import ssl
from urllib import error, request

from . import exceptions, store_payload, verify_payload


def api_download(
    cache_root: str, remote_data_list: list[dict], root: str, headers: dict
):
    """
    Yield the result from `simple_api_downloader`. Wraps errors into a
    `~.exceptions.CommandFail` exception.

    :param remote_data:
        A list of dicts. dict contains ``"url"``, ``"token"``, ``direct`` and ``"insecure"``.

    :returns: A generator
    """
    errors = []
    for remote_data in remote_data_list:
        try:
            payload_data, content_length = yield from simple_api_downloader(
                remote_data, root, headers
            )
            remote_info = {}
            tag = headers.get("Zip-Tag", "")
            cache_file, cache_id = store_payload.store(
                payload_data, cache_root, root, tag, remote_info
            )
            yield from verify_payload.verify_content(
                content_length,
                len(payload_data),
                cache_file.stat().st_size,
            )
            # clears previous error if one download succeeds
            errors.clear()
            break
        except exceptions.Fail as err:
            errors.append(f"{err}")
        except error.HTTPError as err:
            errors.append(
                f"{remote_data['url']}: {err}: {err.read().decode(errors='ignore')}"
            )
        except error.URLError as err:
            errors.append(f"{remote_data['url']}: {err}")
    if errors:
        raise exceptions.CommandFail(f"{','.join(errors)}")
    return cache_file, cache_id, tag


def simple_api_downloader(
    remote_data: dict, root: str, headers: dict
) -> "tuple[bytes, int]":
    """
    A simple downloader. No resume-support. Will not handle transfer errors.

        Yield protocol:

        - If type is `str`: log message
        - If type is `dict`: progress info

    This is a generator that returns a tuple. You have to call it with ``yield from``
    to receive the return value.

    Download will be skipped if the url starts with ``file://``; The given file will
    be returned instead. Use this trick if you want to import zip-files instead of
    downloading them.

    .. code-block:: pycon

        >>> def gen():
        ...   payload, contentlen = yield from simple_api_downloader(remote_data, root, headers)
        ...   yield from _handle_payload(payload, contentlen)

        >>> for res in gen()
        ...     print(res)


    :param dict[str, str, bool] remote_data:
        A dict containing ``"url"``, ``"token"`` and ``"insecure"``.

    :returns: A generator. ``yield from`` returns ``(payload, contentlen)``.
    """

    prefix = remote_data.get("url")
    token = remote_data.get("token")
    insecure = remote_data.get("insecure", False)
    direct = remote_data.get("direct", False)

    if prefix.startswith("file:///"):
        # file already downloaded.
        endpoint = request.url2pathname(prefix[5:])  # to normal filename
        endpoint_path = pathlib.Path(endpoint)
        if not endpoint_path.is_file():
            raise exceptions.Fail("File not found")
        payload = endpoint_path.read_bytes()
        return payload, len(payload)
    elif direct:
        endpoint = prefix
    else:
        endpoint = f"{prefix}/download/zip/{root}"

    if token:
        headers["Token"] = token
    req = request.Request(url=endpoint, headers=headers)

    context = ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    yield {"progress": 0}
    yield f"downloading {root} from {endpoint}"
    res = request.urlopen(req, context=context)
    info = res.info()
    if info.get("Content-Type", "") != "application/zip":
        raise exceptions.Fail("Only Content-Type: application/zip is supported")

    content_len = int(info.get("Content-Length", "0"))
    chunk = 1024 * 1024

    yield_progress = content_len > (chunk * 10)
    if yield_progress:
        chunk = content_len // 10

    progress = 0
    buffer = b" "
    payload = b""
    while buffer:
        info = res.info()
        buffer = res.read(chunk)
        payload += buffer
        progress = round(len(payload) / content_len * 100)
        if yield_progress:
            yield {"progress": progress}  # 0-100%
            if progress < 100:
                yield f"downloading {progress}%"  # 0-100%
    if yield_progress:
        yield f"downloading {progress}%"
    yield "download complete"
    return payload, content_len
