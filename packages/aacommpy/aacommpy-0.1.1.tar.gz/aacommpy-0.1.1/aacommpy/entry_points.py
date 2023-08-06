import argparse
import os
import requests
from zipfile import ZipFile


def install_template() -> None:
    msg = 'Download Python package template project to this directory (y/n)? '
    user_response = input(msg)
    if user_response != 'y':
        return None

    url = 'https://github.com/jamesbond90/aacommpyDownloader/archive/refs/heads/main.zip'
    r = requests.get(url)
    with open('temp.zip', 'wb') as f:
        f.write(r.content)

    with ZipFile('temp.zip', 'r') as repo_zip:
        repo_zip.extractall('.')

    os.remove('temp.zip')
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description='Download aacommpy package.')
    parser.add_argument('command', choices=['install'], help='Choose a command to execute.')
    args = parser.parse_args()

    if args.command == 'install':
        install_template()
    else:
        raise RuntimeError('Please supply a valid command for aacommpy - e.g. install.')

    return None


if __name__ == '__main__':
    main()
