from pydantic import BaseModel

class Ec2(BaseModel):
    tag_name:str
    resource_name:str
    ami:str
    type:str 
    count:str 
    vpc:str
    subnet:str 
    delonterm:bool 