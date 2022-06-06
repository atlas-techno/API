from time import sleep
from modules.dirs_manager import *
from os import *
from modules.s3 import create_presigned_url, pull_key, push_key

def dictify(object):
    return object.dict()

def genkey(user,workspace,key_name):
    os.chdir(f'/atlas/{user}/{workspace}/keys')
    if not os.path.exists(f'/atlas/{user}/{workspace}/keys/{key_name}.pem'):
        os.chdir(f'/atlas/{user}/{workspace}/keys')
        os.system(f'ssh-keygen -t rsa -b 2048 -m PEM -f {key_name}.pem -N ""')
        sleep(2)
        os.system(f'chmod 400 {key_name}.pem')
        push_key(user,workspace,key_name)
        pull_key(user,workspace,key_name)
        create_presigned_url("atlas.storage",f'/atlas/{user}/{workspace}/keys/{key_name}.pem')
    else:
        os.chdir(f'/atlas/{user}/{workspace}/keys')
        pull_key(user,workspace,key_name)
        create_presigned_url("atlas.storage",f'/atlas/{user}/{workspace}/keys/{key_name}.pem')
