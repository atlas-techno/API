from fastapi import FastAPI, File, UploadFile
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

@app.post("/create_workspace")
def create_workspace(workspace:Workspace):
    workspace = dictify(workspace)
    create_dir(workspace["name"])
    build_script("provider",workspace["name"],aws_provider("","",workspace["region"]))

@app.post("/{workspace}/create-vpc")
def create_vpc(workspace:str,vpc:Vpc):
    goto(workspace)
    print(workspace)
    vpc = dictify(vpc)
    build_script(
        "main",
        workspace,
        aws_vpc(vpc["resource_name"],vpc["cidr_block"])
    )
    return {"Status":f'Your vpc was created with this configuration: {vpc}'}

@app.post("/{workspace}/create-ec2")
def create_ec2(workspace:str,ec2:Ec2):
    goto(workspace)
    ec2 = dictify(ec2)
    build_script(
        "main",
        workspace,
        aws_instance(ec2["resource_name"],ec2["ami"],ec2["type"],ec2["count"],ec2["volume_size"],ec2["volume_type"],ec2["delete_on_termination"])
    )
    return {"Status": f'Your EC2 has been created with this configuration: {ec2}'}

@app.get("/{workspace}/deploy")
def deploy(workspace:str):
    plan_and_apply(workspace)
    return {"Status":"Your infrastructure has been deployed"}

@app.get('/{workspace}/destroy')
def destroy(workspace:str):
    goto(workspace)
    destroy_()
    return {"Status":"Your infrastructure has been destroyed"}
