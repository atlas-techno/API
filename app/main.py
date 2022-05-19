from fastapi import FastAPI, File, UploadFile, status, Form
from fastapi.middleware.cors import CORSMiddleware
from modules.file_manager import *
from modules.script_structures import *
from modules.resources import *
from modules.terraform_controller import *
from modules.dirs_manager import *
from modules.s3 import *

s3 = boto3.client("s3")
BUCKET_NAME = "atlas.storage"

access_key = str("AKIA6FJTISO6YSYK7VZ2")
secret_key = str("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")

app = FastAPI()

origins = ["origins"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/{user}/create_workspace", status_code=status.HTTP_201_CREATED)
def create_workspace(user:str,workspace:Workspace):
    workspace = dictify(workspace)
    create_workspace_(user,workspace["name"])
    build_script("provider",user,workspace["name"],aws_provider("AKIA6FJTISO6YSYK7VZ2","XrVjyd1V9xjRd4hpBExfqdvL683q27EV06mw/PeT",workspace["region"]))
    build_script("var",user,workspace["name"],variables())

@app.post("/{user}/{workspace}/create_vpc", status_code=status.HTTP_201_CREATED)
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

@app.post("/{user}/{workspace}/create_ec2", status_code=status.HTTP_201_CREATED)
def create_ec2(user:str,workspace:str,ec2:Ec2):
    goto(user,workspace)
    ec2 = dictify(ec2)
    build_script(
        "main",
        user,
        workspace,
        aws_instance(ec2["resource_name"],ec2["ami"],ec2["type"],ec2["count"],ec2["volume_size"],ec2["volume_type"],ec2["delete_on_termination"], ec2["subnet_name"])
    )
    return {"Status": f'Your EC2 has been created with this configuration: {ec2}'}

@app.post("/{user}/{workspace}/create_subpub")
def create_subpub(user:str,workspace:str,subnet:Subnet):
    goto(user,workspace)
    subnet = dictify(subnet)
    build_script(
        "main",
        user,
        workspace,
        aws_subnet_public(subnet["resource_name"],subnet["vpc_name"],subnet["cidr_block"])
    )
    return {"Status": f'Your subnet was created'}

@app.post("/{user}/{workspace}/create_subpriv")
def create_subpriv(user:str,workspace:str,subnet:Subnet):
    goto(user,workspace)
    subnet = dictify(subnet)
    build_script(
        "main",
        user,
        workspace,
        aws_subnet_private(subnet["resource_name"],subnet["vpc_name"],subnet["cidr_block"],subnet["tag_name"])
    )
    return {"Status": f'Your subnet was created'}

@app.get("/{user}/{workspace}/deploy", status_code=status.HTTP_202_ACCEPTED)
def deploy(user:str,workspace:str):
    goto(user,workspace)
    try:
        pull_infra(user,workspace)
        plan_and_apply(user,workspace)
        push_infra(user,workspace)
    except: 
        plan_and_apply(user,workspace)
        push_infra(user,workspace)
    return {"Status":"Your infrastructure has been deployed"}

@app.get('/{user}/{workspace}/destroy', status_code=status.HTTP_202_ACCEPTED)
def destroy(user:str,workspace:str):
    goto(user,workspace)
    pull_infra(user,workspace)
    destroy_(user,workspace)
    push_infra(user,workspace)
    return {"Status":"Your infrastructure has been destroyed"}



