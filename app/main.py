from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from modules.file_manager import create_ec2_file, dictify
from modules.resources import Ec2

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

def validate():
    validator = 1
    return validate
@app.post("/create-ec2")
def create_ec2(ec2:Ec2):
    create_ec2_file(dictify(ec2),validate())
    return (ec2, validate())

@app.get("/deploy")
def deploy():
    os.system("cd /home/cephalon/Desktop/atlas && source venv/bin/activate && terraform init && terraform fmt && terraform plan && terraform apply --auto-approve")

@app.get('/destroy')
def destroy():
    os.system("cd /home/cephalon/Desktop/atlas && source venv/bin/activate && terraform destroy --auto-approve")

@app.get('/inspect')
def inspect_code():
    f=open("main.tf",mode="r")
    text = f.read()
    return text
