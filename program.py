from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging
from engine import engine_process
from web_server import web_server_process


def setup_parser(parser):
    subparsers = parser.add_subparsers(help="Choose command to run")

    engine_parser = subparsers.add_parser("engine", help="Create Indexes")
    engine_parser.set_defaults(callback=engine_process)

    web_server_parser = subparsers.add_parser("index_merger", help="Serve Web Application")
    web_server_parser.add_argument(
        "--redis-ip", required=True, dest="redis_ip",
        help="IP address of the Redis server",
    )
    web_server_parser.add_argument(
        "--gluster-ip", required=True, dest="gluster_ip",
        help="IP address of the GlusterFS server",
    )
    web_server_parser.set_defaults(callback=web_server_process)


def setup_logging():
    logging.basicConfig(
        filename='logs/search-engine.log', level=logging.DEBUG,
        format="%(levelname)s: %(message)s"
    )


def main():
    parser = ArgumentParser(
        prog="search-engine",
        description="This is the search engine.",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    setup_logging()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
