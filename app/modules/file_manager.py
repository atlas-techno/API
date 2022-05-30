from modules.dirs_manager import *
from os import *

def dictify(object):
    return object.dict()

def genkey(user,workspace,key_name):
    if not os.path.isdir(f"/{user}/{workspace}/keys"):
        os.mkdir(f"/atlas/{user}/{workspace}/keys")
        os.chdir(f"/atlas/{user}/{workspace}/keys")
    else:
        os.chdir(f"/atlas/{user}/{workspace}/keys")
    if not os.path.exists(f"{key_name}.pem"):
        #os.system(f"/atlas/{user}/{workspace}/keys/ssh-keygen -t rsa -b 2048 -m PEM -f {key_name} -P 12345 && openssl rsa -in {key_name}.pub -outform pem -out {key_name}.pem -passin pass:12345")
        os.system(f'ssh-keygen -b 2048 -t rsa -f /atlas/{user}/{workspace}/keys/{key_name}.pem -q -N "" ')

