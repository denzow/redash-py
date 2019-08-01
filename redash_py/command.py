import fire

from redash_py.client import RedashAPIClient


def main():
    fire.Fire(RedashAPIClient)


if __name__ in '__main__':
    main()


