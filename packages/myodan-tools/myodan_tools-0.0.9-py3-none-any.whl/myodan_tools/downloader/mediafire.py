import os
import os.path as osp
import re
import shutil
import sys
import tempfile
import requests
import six

CHUNK_SIZE = 512 * 1024  # 512KB

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36"


def extract_download_link(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((?:http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]


def download(url, output):
    url_origin = url
    sess = requests.session()
    sess.headers = {"User-Agent": USER_AGENT}

    while True:
        res = sess.get(url, stream=True)
        if "Content-Disposition" in res.headers:
            break

        url = extract_download_link(res.text)

        if url is None:
            print("Permission denied: %s" % url_origin, file=sys.stderr)
            print(
                "Maybe you need to change permission over "
                "'Anyone with the link'?",
                file=sys.stderr,
            )

            return

    if output is None:
        origin_filename = re.search(
            'filename="(.*)"',
            res.headers["Content-Disposition"],
        )
        output = origin_filename.groups()[0]
        output = output.encode("iso8859").decode("utf-8")

    output_is_path = isinstance(output, six.string_types)

    print("Downloading...", file=sys.stderr)
    print("From:", url_origin, file=sys.stderr)
    print(
        "To:",
        osp.abspath(output) if output_is_path else output,
        file=sys.stderr,
    )

    if output_is_path:
        temp_file = tempfile.mktemp(
            suffix=tempfile.template,
            prefix=osp.basename(output),
            dir=osp.dirname(output),
        )
        temp_file_buffer = open(temp_file, "wb")

    else:
        temp_file = None
        temp_file_buffer = output

    try:
        total = res.headers.get("Content-Length")

        if total is not None:
            total = int(total)

        for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
            temp_file_buffer.write(chunk)

        if temp_file:
            temp_file_buffer.close()
            shutil.move(temp_file, output)

    except IOError as error:
        print(error, file=sys.stderr)
        return

    finally:
        try:
            if temp_file:
                os.remove(temp_file)

        except OSError:
            pass

    return output
