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
    workspace_id = create_workspace(user,workspace["name"],workspace["region"])
    build_script("provider",user,workspace_id,aws_provider("AKIA6FJTISO6YSYK7VZ2","XrVjyd1V9xjRd4hpBExfqdvL683q27EV06mw/PeT",workspace["region"]))
    build_script("var",user,workspace_id,variables())
    return {"workspace_id":workspace_id}

@app.post("/{user}/{workspace}/create_vpc", status_code=status.HTTP_201_CREATED)
def create_vpc_http(user:str,workspace:str,vpc:Vpc):
    goto(user,workspace)
    vpc = dictify(vpc)
    vpc_id = create_vpc(workspace,vpc["resource_name"],vpc["cidr_block"])
    build_script(
        "main",
        user, 
        workspace,
        aws_vpc(vpc["resource_name"],vpc["cidr_block"])
    )
    return {"vpc_id":vpc_id}

@app.post("/{user}/{workspace}/create_subpub")
def create_subpub_http(user:str,workspace:str,subnet:Subnet):
    goto(user,workspace)
    subnet = dictify(subnet)
    subnet_id = create_subnet(subnet["vpc_id"],subnet["resource_name"],subnet["cidr_block"])
    build_script(
        "main",
        user,
        workspace,
        aws_subnet_public(subnet["resource_name"],subnet["vpc_name"],subnet["cidr_block"])
    )
    return {"subnet_id":subnet_id}

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

@app.post("/{user}/{workspace}/create_ec2", status_code=status.HTTP_201_CREATED)
def create_ec2_http(user:str,workspace:str,ec2:Ec2):
    goto(user,workspace)
    ec2 = dictify(ec2)
    genkey(user,workspace,ec2["key_name"])
    build_script(
        "main",
        user,
        workspace,
        aws_key_pair(user,workspace,ec2["key_name"]),
        aws_instance(workspace,ec2["resource_name"],ec2["ami"],ec2["type"],ec2["count"],ec2["volume_size"],ec2["volume_type"],ec2["delete_on_termination"], ec2["subnet_name"],ec2["key_name"])
    )
    
    instance= create_instance(ec2["subnet_id"],ec2["resource_name"],ec2["ami"],ec2["type"],ec2["count"],ec2["volume_size"],ec2["volume_type"],ec2["delete_on_termination"])
    url = create_presigned_url("atlas.storage",f'/atlas/{user}/{workspace}/keys/{ec2["key_name"]}')
    return {"EC2 Info":instance, "URL":url}

@app.get("/{user}/{workspace}/deploy", status_code=status.HTTP_202_ACCEPTED)
def deploy(user:str,workspace:str):
    goto(user,workspace)
    try:
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
    delete_dir(user,workspace)
    return {"Status":"Your infrastructure has been destroyed"}

@app.get("/{user}/query_workspaces")
def query_workspaces_http(user:str):
    workspace_object_list = query_workspaces(user)
    return workspace_object_list

@app.get("/{workspace}/query_vpcs")
def query_vpcs_http(workspace:str):
    vpc_object_list = query_vpcs(workspace)
    return vpc_object_list

@app.get("/{workspace}/query_subnets")
def query_subnets_http(workspace:str):
    subnet_object_list = query_subnets(workspace)
    return subnet_object_list

@app.get("/{workspace}/query_instances")
def query_instances_http(workspace):
    instances_object_list = query_instance(workspace)
    return instances_object_list


@app.get("/{user}/{workspace}/query_keys")
def query_keys_http(user:str,workspace:str):
    keys_list = query_keys_s3(user,workspace)
    return keys_list

@app.get("/{user}/query_ssh_keys")
def query_ssh_keys_http(user:str):
    ssh_keys_list = query_ssh_keys_mongdb(user)
    return ssh_keys_list

