from fastapi import FastAPI, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from modules.file_manager import *
from modules.script_structures import *
from modules.resources import *
from modules.terraform_controller import *
from modules.dirs_manager import *

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

@app.post("/{user}/create_workspace", status_code=status.HTTP_201_CREATED)
def create_workspace(user:str,workspace:Workspace):
    workspace = dictify(workspace)
    create_workspace_(user,workspace["name"])
    build_script("provider",user,workspace["name"],aws_provider("AKIA6FJTISO64JMYRSFH","0QGgdoYa4BLIoHDNirG5T36ax8YWArFA3b+WKNVs",workspace["region"]))

@app.post("/{user}/{workspace}/create-vpc", status_code=status.HTTP_201_CREATED)
def create_vpc(user:str,workspace:str,vpc:Vpc):
    goto(user,workspace)
    vpc = dictify(vpc)
    build_script(
        "main",
        user, 
        workspace,
        aws_vpc(vpc["resource_name"],vpc["cidr_block"])
    )
    return {"Status":f'Your vpc was created with this configuration: {vpc}'}

@app.post("/{user}/{workspace}/create-ec2", status_code=status.HTTP_201_CREATED)
def create_ec2(user:str,workspace:str,ec2:Ec2):
    goto(user,workspace)
    ec2 = dictify(ec2)
    build_script(
        "main",
        user,
        workspace,
        aws_instance(ec2["resource_name"],ec2["ami"],ec2["type"],ec2["count"],ec2["volume_size"],ec2["volume_type"],ec2["delete_on_termination"])
    )
    return {"Status": f'Your EC2 has been created with this configuration: {ec2}'}

@app.get("/{user}/{workspace}/deploy", status_code=status.HTTP_202_ACCEPTED)
def deploy(user:str,workspace:str):
    plan_and_apply(user,workspace)
    return {"Status":"Your infrastructure has been deployed"}

@app.get('/{user}/{workspace}/destroy', status_code=status.HTTP_202_ACCEPTED)
def destroy(user:str,workspace:str):
    goto(user,workspace)
    destroy_()
    return {"Status":"Your infrastructure has been destroyed"}
