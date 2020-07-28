#!/usr/bin/env python

import subprocess
import os
import argparse
from pathlib import Path
import requests
import sys
import webbrowser

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('name', type=str, default=None, help='a name for the project')
parser.add_argument('description', type=str, default=None, help='a brief description')
parser.add_argument('--public', dest='public', action='store_const',
                    const=True, default=False,
                    help='make repository public (default: private)')


USERNAME = 'bilichj'
REPO_ROOT = Path('/home/jordan/src/github.com/bilichj/')

class RepositoryExistsError(Exception):
    pass


def get_remote_repo_names(username):
    response = requests.get(f'https://api.github.com/users/{username}/repos')
    return [repo['name'] for repo in response.json()]

args = parser.parse_args()
os.chdir(REPO_ROOT)
path = REPO_ROOT.joinpath(args.name)

if path.exists():
    raise FileExistsError('Directory with that project name already exists locally.')

if args.name in get_remote_repo_names(USERNAME):
    raise RepositoryExistsError('Repository with that name already exists remotely.')

path.mkdir()
path.joinpath(args.name).mkdir()
os.chdir(args.name)

print('Initializing repo...')\

try:
    subprocess.check_call(['git', 'init'])
except subprocess.CalledProcessError:
    print('git init failed, cleaning up...')
    subprocess.check_call(['rm', '-rf', path])()
    sys.exit(1)

readme = f'# {args.name}\n{args.description}'

try:
    subprocess.check_call(['pipenv', 'install'])
except subprocess.CalledProcessError:
    print('pipenv install failed, cleaning up...')
    subprocess.check_call(['rm', '-rf', path])()
    sys.exit(1)


with open('README.md', 'w') as f:
    f.write(readme)

try:
    subprocess.check_call(['touch', f'{args.name}/__init__.py'])

except subprocess.CalledProcessError:
    print('pipenv install failed, cleaning up...')
    subprocess.check_call(['rm', '-rf', path])()
    sys.exit(1)

try:
    subprocess.check_call(['git', 'add', 'README.md'])
except subprocess.CalledProcessError:
    print('adding README failed, cleaning up...')
    subprocess.check_call(['rm', '-rf', path])()
    sys.exit(1)

try:
    subprocess.check_call(['git', 'add', f'{args.name}/__init__.py'])
except subprocess.CalledProcessError:
    print('adding README failed, cleaning up...')
    subprocess.check_call(['rm', '-rf', path])()
    sys.exit(1)

try:
    subprocess.check_call(['git', 'commit', '-m', '"initial commit"'])

except subprocess.CalledProcessError:
    print('commit failed, cleaning up...')
    subprocess.check_call(['rm', '-rf', path])()
    sys.exit(1)

create_command = ['hub', 'create'] + ( [] if args.public else ['-p'])

try:
    subprocess.check_call(create_command)

except subprocess.CalledProcessError:
    print('github repo creation failed, cleaning up...')
    subprocess.check_call(['rm', '-rf', path])()
    sys.exit(1)

try:
    subprocess.check_call(['git', 'push', '--set-upstream', 'origin', 'master'])
except subprocess.CalledProcessError:
    print('Push failed. Remote repo still exists, keeping local files.')
    sys.exit(1)

print('Success! Opening VSCode...')
subprocess.check_call(['open-project', 'args.name'])
