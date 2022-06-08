from time import sleep
from modules.dirs_manager import *
from os import *
from modules.s3 import create_presigned_url, pull_key, push_key

def dictify(object):
    return object.dict()

def genkey(user,key_name):
    os.chdir(f'/atlas/{user}/keys')
    if not os.path.exists(f'/atlas/{user}/keys/{key_name}.pem'):
        os.chdir(f'/atlas/{user}/keys')
        os.system(f'ssh-keygen -t rsa -b 2048 -m PEM -f {key_name}.pem -N ""')
        sleep(2)
        os.system(f'chmod 400 {key_name}.pem')
        push_key(user,key_name)
        pull_key(user,key_name)
    else:
        os.chdir(f'/atlas/{user}/keys')
        pull_key(user,key_name)
