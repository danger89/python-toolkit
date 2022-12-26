import logging
import m3u8
import os
import requests
import shutil
from functools import partial
from urllib.parse import urlparse
from ..util import TaskPool, remove_filename_ext, random_agent


logger = logging.getLogger(__file__)


def download_slice(uri, video_name, args):
    r = requests.get(uri, headers={
        "User-Agent": random_agent(args.use_fake_agent),
    }, verify=not args.no_verify_ssl)
    if r.status_code == requests.codes.ok:
        filename = os.path.basename(urlparse(uri).path)
        path = os.path.join(video_name, filename)
        with open(path, "wb") as fout:
            fout.write(r.content)
    else:
        raise IOError(f"Unexpected status code {r.status_code} while "
                      f"requesting {uri}")


def main(args):
    playlist = m3u8.load(args.url, headers={
        "User-Agent": random_agent(args.use_fake_agent),
    }, verify_ssl=not args.no_verify_ssl)
    video_name = args.name or os.path.basename(urlparse(args.url).path)
    video_name = remove_filename_ext(video_name) or "video"
    if playlist.keys and playlist.keys[0]: # download encrypted stream with ffmpeg
        cmd = ["ffmpeg", "-allowed_extensions", "ALL", 
               "-protocol_whitelist", "file,http,https,httpproxy,crypto,tls,tcp",
               "-i", f'"{args.url}"',
               "-c", "copy",
               f'"{video_name}.mp4"']
        cmd_str = " ".join(cmd)
        logger.info(cmd_str)
        os.system(cmd_str)
    else:
        os.makedirs(video_name, exist_ok=True)
        callables = [
            partial(download_slice, uri=seg.absolute_uri, video_name=video_name, args=args)
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
