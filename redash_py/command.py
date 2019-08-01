import json
import sys
import os
import argparse
from logging import getLogger, Formatter, StreamHandler, DEBUG

from .client import RedashAPIClient

logger = getLogger(__name__)
formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.setLevel(DEBUG)
logger.addHandler(handler)


COMMAND_DESCRIPTION = """\
-----------------------------------------------------------------------
redashpy:

-----------------------------------------------------------------------
"""


def init():
    """
    arguments.
    """
    parser = argparse.ArgumentParser(description=COMMAND_DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-H',
        '--host',
        type=str,
        required=False,
        dest='service_host',
        help='service_host.'
    )

    parser.add_argument(
        '-k',
        '--api-key',
        type=str,
        required=False,
        dest='api_key',
        help='api_key.'
    )

    parser.add_argument(
        '-c',
        '--command',
        type=str,
        required=True,
        dest='command',
        help='command'
    )
    parser.add_argument(
        'command_args',
        nargs='*',
    )
    return parser.parse_args()


def main():
    args = init()
    if not args.service_host:
        service_url = os.environ.get('REDASH_SERVICE_URL', 'http://localhost:5000')
    else:
        service_url = args.service_host
    if not args.api_key:
        api_key = os.environ.get('REDASH_API_KEY')
    else:
        api_key = args.api_key

    client = RedashAPIClient(
        api_key=api_key,
        host=service_url,
    )
    if hasattr(client, args.command):
        result = getattr(client, args.command)(*args.command_args)
        sys.stdout.write(json.dumps(result, indent=4))
    else:
        sys.stderr.write(f'{args.command} is not valid command\n')
        sys.exit(1)


if __name__ in '__main__':
    main()


