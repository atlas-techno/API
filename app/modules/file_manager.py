from app.modules.script_structures import *
from modules.dirs_manager import *
def dictify(object):
    return object.dict()

"""
def check_igw():
    with open("main.tf",mode="r") as f:
        if 'resource "aws_internet_gateway"' in f.read():    
            return aws_subnet_public
        else:
            return aws_subnet_public_igw
"""
def cat_igw():
    with open("main.tf",mode="r") as f:
        pass