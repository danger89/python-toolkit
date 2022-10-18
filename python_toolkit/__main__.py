import logging
from rich.logging import RichHandler
from rich.traceback import install
from .args import get_args


logger = logging.getLogger(__file__)


def setup():
    # setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    # setup traceback handler
    install(show_locals=True)


def main():
    args = get_args()
    logger.info(args)
    args.callback(args)


if __name__ == "__main__":
    setup()
    main()
