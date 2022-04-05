from dataclasses import field
from tkinter import E
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

def create_file(name="main.tf"):
    f = open(f'{name}',mode="x")
    return name

def edit_file(file):
    return open(f'{file}',mode="w")

def format_ec2(object):
    ec2 = object.dict()
    ec2["id"] = randrange(0,100000)
    create_ec2_file(ec2)
    return ec2

def create_ec2_file(ec2):
    file = edit_file(create_file())
    file.write(
    f'''
    provider aws {{
        region = "us-east-1"
        access_key = "AKIA6FJTISO64JMYRSFH"
        secret_key = "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"
    }}

    resource "aws_instance" "atlas_ec2" {{ 
        ami = "{ec2["ami"]}"
        instance_type = "{ec2["type"]}"
        count = "{ec2["count"]}"
        tags = {{
            Name = "{ec2["name"]}"
        }}
    }}
    ''')
    file.close()

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
    format_ec2(ec2)
    return {"Status":f'You EC2 was succesful created with this configuration:{ec2}'}

@app.get("/deploy")
def deploy():
    os.system("cd /home/cephalon/Desktop/atlas && source venv/bin/activate && terraform init && terraform fmt && terraform plan && terraform apply --auto-approve")

@app.get('/destroy')
def destroy():
    os.system("cd /home/cephalon/Desktop/atlas && source venv/bin/activate && terraform destroy --auto-approve")

