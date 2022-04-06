from re import S
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.file_manager import dictify
from modules.script_structures import aws_provider, aws_vpc, aws_instance, build_script
from modules.resources import Ec2, Vpc
from modules.terraform_controller import plan_and_apply, destroy_

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

@app.get("/")
def init():
    build_script(
        aws_provider(access_key,secret_key)
    )
    return {"Status": "Script Initialized"}

@app.post("/create-vpc")
def create_vpc(vpc:Vpc):
    vpc = dictify(vpc)
    build_script(
        aws_vpc(vpc["resource_name"],vpc["cidr_block"],vpc["tag_name"])
    )
    return {"Status":f'Your vpc was created with this configuration: {vpc}'}

@app.post("/create-ec2")
def create_ec2(ec2:Ec2):
    ec2 = dictify(ec2)
    build_script(
        aws_instance(ec2["resource_name"],ec2["ami"],ec2["type"],ec2["count"],ec2["tag_name"],ec2["delete_on_termination"])
    )
    return {"Status": f'Your EC2 has been created with this configuration: {ec2}'}

@app.get("/deploy")
def deploy():
    plan_and_apply()
    return {"Status":"Your infrastructure has been deployed"}

@app.get('/destroy')
def destroy():
    destroy_()
    return {"Status":"Your infrastructure has been destroyed"}

@app.get('/inspect')
def inspect_code():
    f=open("main.tf",mode="r")
    text = f.read()
    return text
