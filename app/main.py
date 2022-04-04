from dataclasses import field
from fastapi import FastAPI
from pydantic import BaseModel
from re import A
from random import randrange 
import os
from fastapi.middleware.cors import CORSMiddleware

access_key = str("AKIA6FJTISO64JMYRSFH")
secret_key = str("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")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ec2_list = []

def create_file(ec2):
    file = open("main.tf",mode="w")
    """
    file.write(ec2["ami"])
    file.write(ec2["type"])
    file.write(ec2["count"])
    file.write(ec2["name"])
    """
    file.write(
'''
resource "aws_instance" "atlas_ec2" {{ 
    ami = "{}"
    instance_type = "{}"
    count = "{}"
    Name = "{}"
}}
'''.format(ec2["ami"],ec2["type"],ec2["count"],ec2["name"]))
    file.close()
    #os.system("cd /home/cephalon/Desktop/atlas/ && source venv/bin/activate && terraform init && terraform plan && terraform apply --auto-approve")


def find_ec2(id):
    for ec2 in ec2_list:
        if ec2["id"] == id:
            return ec2

class Ec2(BaseModel):
    name:str
    ami:str
    type:str 
    count:str 
    vpc:str
    subnet:str 
    delonterm:bool 

@app.post("/create-ec2")
def create_ec2(ec2:Ec2):
    ec2 = ec2.dict()
    ec2["id"] = randrange(0,10000)
    create_file(ec2)
    ec2_list.append(ec2)
    return {"Status":f'You EC2 was succesful created with this configuration: {ec2}'}

@app.get("/ec2/{id}")
def inspect_ec2(id:int):
    ec2 = find_ec2(id)
    return {"Status": f'EC2 founded: {ec2}'} 

@app.get("/ec2")
def show_all_ec2():
    return ec2_list

@app.delete('/delete-ec2/{id}')
def delete_ec2(id:int):
    ec2 = ec2_list.index(find_ec2(id))
    ec2_list.pop(ec2)
    return {"Message":f'{ec2_list}'}

@app.get('/destroy')
def destroy():
    os.system("cd /home/cephalon/Desktop/atlas && source venv/bin/activate && terraform destroy --auto-approve")

@app.put('/ec2/{id}')
def update_ec2(id:int,ec2:Ec2):
    pass 
