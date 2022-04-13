import os
from pydantic import BaseModel

class Dir(BaseModel):
    dir_name:str
    
def create_dir(dirname):
    os.system(f'cd /atlas && mkdir /atlas/{dirname} && cd /atlas/{dirname}')

def delete_dir(dirname):
    os.system(f'cd /atlas && rm -rf /atlas/{dirname}')

def rename_dir(dirname):
    os.system(f'cd /atlas && mv /atlas/{dirname}')