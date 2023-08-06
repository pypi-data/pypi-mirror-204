import argparse
import os
import requests
from zipfile import ZipFile
import subprocess


def install_template() -> None:
    msg = 'Download Python package template project to this directory (y/n)? '
    user_response = input(msg)
    if user_response != 'y':
        return None

    url = 'https://github.com/jamesbond90/aacommpyDownloader/archive/refs/heads/main.zip'
    r = requests.get(url)
    with open(os.path.join(os.path.dirname(__file__), 'main.zip'), 'wb') as f:
        f.write(r.content)

    with ZipFile(os.path.join(os.path.dirname(__file__), 'main.zip'), 'r') as repo_zip:
        repo_zip.extractall(os.path.dirname(__file__))

    os.remove(os.path.join(os.path.dirname(__file__), 'main.zip'))
    return None

def download_nuget() -> None:
    nuget_path = os.path.join(os.path.dirname(__file__), 'aacommpyDownloader-main', 'nuget.exe')
    nuget_cmd = [nuget_path, 'install', 'Agito.AAComm', '-OutputDirectory', os.path.join(os.path.dirname(nuget_path)), '-Source', 'https://api.nuget.org/v3/index.json']
    subprocess.run(nuget_cmd, check=True)
    return None
def nuget_version() -> None:
    nuget_path = os.path.join(os.path.dirname(__file__), 'aacommpyDownloader-main', 'nuget.exe')
    nuget_cmd = [nuget_path, 'list', 'Agito.AAComm']
    result = subprocess.run(nuget_cmd, check=True, stdout=subprocess.PIPE, text=True)
    version = None
    for line in result.stdout.splitlines():
        if 'Agito.AAComm ' in line:
            version = line.split(' ')[-1]
            break
    if version is not None:
        print(f'The installed version of Agito.AAComm is {version}.')
    else:
        print('Agito.AAComm package is not installed.')
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description='Download aacommpy package.')
    parser.add_argument('command', choices=['install', 'downloadnuget', 'version'], help='Choose a command to execute.')
    args = parser.parse_args()

    if args.command == 'install':
        install_template()
    elif args.command == 'downloadnuget':
        download_nuget()
    elif args.command == 'version':
        nuget_version()
    else:
        raise RuntimeError('Please supply a valid command for aacommpy - e.g. install.')

    return None


if __name__ == '__main__':
    main()
