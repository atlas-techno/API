from pydantic import BaseModel
from typing import Optional

class Workspace(BaseModel):
    name:str
    region:str

class Ec2(BaseModel):
    resource_name:str
    ami:str
    type:str 
    count:str
    volume_size:str
    volume_type:str
    delete_on_termination:str
    subnet_id: Optional[str]  

class Vpc(BaseModel):
    resource_name:str
    cidr_block:int

class Subnet(BaseModel):
    resource_name:str 
    vpc_name:str 
    cidr_block:int 
    access:bool

class Igw(BaseModel):
    vpc_id:str 
    tag_name:str 

class Natgw(BaseModel):
    subnet_id:str
