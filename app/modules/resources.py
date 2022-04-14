from pydantic import BaseModel

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

class Vpc(BaseModel):
    resource_name:str
    cidr_block:str
    enable_dns:str

class Subnet(BaseModel):
    resource_name:str 
    vpc_id:str 
    cidr_block:str 
    az:str

class Igw(BaseModel):
    vpc_id:str 
    tag_name:str 

class Natgw(BaseModel):
    subnet_id:str
