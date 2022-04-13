from pydantic import BaseModel

class Workspace(BaseModel):
    name:str
    region:str

class Ec2(BaseModel):
    resource_name:str
    ami:str
    type:str 
    count:str
    tag_name:str
    delete_on_termination:str 

class Vpc(BaseModel):
    resource_name:str
    cidr_block:str
    tag_name:str

class Subnet(BaseModel):
    resource_name:str 
    vpc_name:str 
    cidr_block:str 
    tag_name:str
