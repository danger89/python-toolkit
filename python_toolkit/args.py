import argparse
from .network import main_m3u8d, main_webimd


def get_args():
    parser = argparse.ArgumentParser(prog="python_toolkit",
        description="My customize tools in Python with love")
    subparsers = parser.add_subparsers()

    parser_m3u8d = subparsers.add_parser("m3u8d", help="Download videos with "
                                         "a single url to m3u8 file")
    parser_m3u8d.add_argument("url", type=str)
    parser_m3u8d.add_argument("-n", "--name", type=str)
    parser_m3u8d.add_argument("-t", "--threads", type=int, default=15)
    parser_m3u8d.set_defaults(callback=main_m3u8d)

    parser_webimd = subparsers.add_parser("webimd", help="Download all "
                                          "from an html document")
    parser_webimd.add_argument("-i", "--input", type=str, default="input.txt")
    parser_webimd.add_argument("-o", "--output", type=str, default="downloads")
    parser_webimd.add_argument("-t", "--threads", type=int, default=15)
    parser_webimd.add_argument("-p", "--prefix", type=str)
    parser_webimd.set_defaults(callback=main_webimd)

    return parser.parse_args()
