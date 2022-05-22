import re
from fastapi import FastAPI, File, UploadFile, status, Form
from fastapi.middleware.cors import CORSMiddleware
from modules.file_manager import *
from modules.script_structures import *
from modules.resources import *
from modules.terraform_controller import *
from modules.dirs_manager import *
from modules.s3 import *
from modules.mongodb import *

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
def create_workspace_http(user:str,workspace:Workspace):
    workspace = dictify(workspace)
    create_workspace_(user,workspace["name"])
    build_script("provider",user,workspace["name"],aws_provider("AKIA6FJTISO6YSYK7VZ2","XrVjyd1V9xjRd4hpBExfqdvL683q27EV06mw/PeT",workspace["region"]))
    build_script("var",user,workspace["name"],variables())
    create_workspace(user,workspace["name"],workspace["region"])

@app.post("/{user}/{workspace}/create_vpc", status_code=status.HTTP_201_CREATED)
def create_vpc_http(user:str,workspace:str,vpc:Vpc):
    goto(user,workspace)
    vpc = dictify(vpc)
    build_script(
        "main",
        user, 
        workspace,
        aws_vpc(vpc["resource_name"],vpc["cidr_block"])
    )
    create_vpc(user,workspace,vpc["resource_name"],vpc["cidr_block"])
    return {"Status":f'Your vpc was created with this configuration: {vpc}'}

@app.post("/{user}/{workspace}/create_ec2", status_code=status.HTTP_201_CREATED)
def create_ec2_http(user:str,workspace:str,ec2:Ec2):
    goto(user,workspace)
    ec2 = dictify(ec2)
    build_script(
        "main",
        user,
        workspace,
        aws_instance(ec2["resource_name"],ec2["ami"],ec2["type"],ec2["count"],ec2["volume_size"],ec2["volume_type"],ec2["delete_on_termination"], ec2["subnet_name"])
    )
    create_instance(ec2["resource_name"],ec2["ami"],ec2["type"],ec2["count"],ec2["volume_size"],ec2["volume_type"],ec2["delete_on_termination"], ec2["subnet_name"])
    return {"Status": f'Your EC2 has been created with this configuration: {ec2}'}

@app.post("/{user}/{workspace}/create_subpub")
def create_subpub_http(user:str,workspace:str,subnet:Subnet):
    goto(user,workspace)
    subnet = dictify(subnet)
    build_script(
        "main",
        user,
        workspace,
        aws_subnet_public(subnet["resource_name"],subnet["vpc_name"],subnet["cidr_block"])
    )
    create_subnet(user,workspace,subnet["resource_name"],subnet["vpc_name"],subnet["cidr_block"])
    return {"Status": f'Your subnet was created'}

@app.post("/{user}/{workspace}/create_subpriv")
def create_subpriv_http(user:str,workspace:str,subnet:Subnet):
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
def destroy_http(user:str,workspace:str):
    goto(user,workspace)
    pull_infra(user,workspace)
    destroy(user,workspace)
    push_infra(user,workspace)
    return {"Status":"Your infrastructure has been destroyed"}

@app.get("/{user}/query_workspaces")
def query_workspaces_http(user:str):
    workspaces = [x for x in query_workspaces(user)]
    return workspaces

@app.get("/{user}/{workspace}/query_vpcs")
def query_vpcs_http(user:str,workspace:str):
    return query_vpcs(user,workspace)

@app.get("/{user}/{workspace}/{vpc_name}/query_subnets")
def query_subnets_http(user,workspace:str,vpc_name:str):
    return query_subnets(user,workspace,vpc_name)

@app.get("/{user}/{workspace}/{vpc_name}/{subnet_id}/query_instances")
def query_instances_http(user:str,workspace:str,vpc_name:str,subnet_id:str):
    return query_instance(user,workspace,vpc_name,subnet_id)
