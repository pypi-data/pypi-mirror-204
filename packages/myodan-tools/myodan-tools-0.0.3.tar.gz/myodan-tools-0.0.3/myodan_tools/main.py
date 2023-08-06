from urllib.parse import urlparse
import typer

from .downloader import mediafire
from .extractor import mrcong

app = typer.Typer()


@app.callback()
def callback(url_str: str):
    url = urlparse(url_str)

    download_links = []

    if "mrcong.com" in url.netloc:
        if "/tag" in url.path:
            post_links = mrcong.extract_post_links(url_str)

            for post_link in post_links:
                download_links += mrcong.extract_download_links(
                    post_link["href"])

        else:
            download_links += mrcong.extract_download_links(url_str)

        for download_link in download_links:
            mediafire.download(download_link["href"], None, quiet=False)


if __name__ == "__main__":
    app()
