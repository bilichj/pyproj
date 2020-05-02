#!/usr/bin/env python

import subprocess
import os

REPO_ROOT = '/home/jordan/src/github.com/bilichj/'

os.chdir(REPO_ROOT)

project_name = input('Project name: ')


try:
    os.makedirs(f'{project_name}/{project_name}')
except:
    raise Exception('Project already exists locally.')

os.chdir(project_name)

subprocess.check_call(['git', 'init'])

project_description = input('Description: ')

readme = f'#{project_name}\n{project_description}'
print('Initializing repo...')

subprocess.check_call(['pipenv', 'install'])
with open('README.md', 'w') as f:
    f.write(readme)

subprocess.check_call(['touch', f'{project_name}/__init__.py'])

subprocess.check_call(['git', 'add', 'README.md'])
subprocess.check_call(['git', 'commit', '-m', '"initial commit"'])

subprocess.check_call(['hub', 'create'])
subprocess.check_call(['git', 'push', '--set-upstream', 'origin', 'master'])

print('Success!')
