import m3u8
import os
import requests
import shutil
from fake_useragent import UserAgent
from functools import partial
from urllib.parse import urlparse
from ..util import TaskPool, remove_filename_ext


def download_slice(uri, video_name):
    r = requests.get(uri, headers={
        "User-Agent": str(UserAgent().random)
    })
    if r.status_code == requests.codes.ok:
        filename = os.path.basename(urlparse(uri).path)
        path = os.path.join(video_name, filename)
        with open(path, "wb") as fout:
            fout.write(r.content)
    else:
        raise IOError(f"Unexpected status code {r.status_code} while "
                      f"requesting {uri}")


def main(args):
    playlist = m3u8.load(args.url)
    video_name = args.name or os.path.basename(urlparse(args.url).path)
    video_name = remove_filename_ext(video_name) or "video"
    os.makedirs(video_name, exist_ok=True)
    callables = [
        partial(download_slice, uri=seg.absolute_uri, video_name=video_name)
        for seg in playlist.segments
    ]
    TaskPool(callables, video_name, threads=args.threads).start()
    with open(f"{video_name}.ts", "wb") as fout:
        for seg in playlist.segments:
            filename = os.path.basename(urlparse(seg.absolute_uri).path)
            path = os.path.join(video_name, filename)
            with open(path, "rb") as fin:
                fout.write(fin.read())
    video_name = video_name.replace("\"", r"\"")
    if os.system(f"ffmpeg -i \"{video_name}.ts\" \"{video_name}.mp4\"") == 0:
        shutil.rmtree(video_name)
        os.remove(f"{video_name}.ts")
