from pydantic import BaseModel
from typing import Optional

class List_b(BaseModel):
    workspaces: list[str] = []

class Workspace(BaseModel):
    name:str
    region:str

class Vpc(BaseModel):
    resource_name:str
    cidr_block:int

class Subnet(BaseModel):
    vpc_id:str
    vpc_name:str
    resource_name:str 
    cidr_block:int 

class Ec2(BaseModel):
    subnet_id:str
    subnet_name:str
    resource_name:str
    ami:str
    type:str 
    count:str
    volume_size:str
    volume_type:str
    delete_on_termination:str


class Igw(BaseModel):
    vpc_id:str 
    tag_name:str 

class Natgw(BaseModel):
    subnet_id:str
