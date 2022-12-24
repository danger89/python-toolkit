import bs4
import base64
import os
import requests
from functools import partial
from urllib.parse import urlparse
from ..util import fill_uri_prefix, duplicate_filename, TaskPool, random_agent


def save_base64_image(uri, output_dir, serial_number, args):
    ext = uri.split(";")[0].split("/")[-1]
    data = uri.split(",")[-1]
    decoded = base64.b64decode(data)
    filename = f"download.{ext}"
    if not args.no_serial_number:
        filename = f"{serial_number}_{filename}"
    path = os.path.join(output_dir, filename)
    while os.path.isfile(path):
        filename = duplicate_filename(filename)
        path = os.path.join(output_dir, filename)
    with open(path, "wb") as fout:
        fout.write(decoded)


def download_image(uri, output_dir, serial_number, args):
    r = requests.get(uri, headers={
        "User-Agent": random_agent(args.use_fake_agent),
    })
    if r.status_code == requests.codes.ok:
        filename = os.path.basename(urlparse(uri).path)
        if not args.no_serial_number:
            filename = f"{serial_number}_{filename}"
        path = os.path.join(output_dir, filename)
        while os.path.isfile(path):
            filename = duplicate_filename(filename)
            path = os.path.join(output_dir, filename)
        with open(path, "wb") as fout:
            fout.write(r.content)
    else:
        raise IOError(f"Unexpected status code {r.status_code} while "
                      f"requesting {uri}")


def main(args):
    with open(args.input, "r", encoding="utf-8") as fin:
        html = fin.read()
    os.makedirs(args.output, exist_ok=True)
    callables = []
    soup = bs4.BeautifulSoup(html, features="html.parser")
    images = soup.find_all("img")
    serial_number = 0
    for img_tag in images:
        if "src" in img_tag.attrs:
            if img_tag.attrs["src"].startswith("data:image"):
                func = save_base64_image
                uri = img_tag.attrs["src"]
            else:
                func = download_image
                uri = fill_uri_prefix(img_tag.attrs["src"], args.prefix)
            callables.append(partial(func, 
                                     uri=uri, 
                                     output_dir=args.output, 
                                     serial_number=serial_number,
                                     args=args))
            serial_number += 1
    TaskPool(callables, "Web Image Download", threads=args.threads).start()
