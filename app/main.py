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

@app.post("/img")
def img(file:bytes = File(default="a")):
    return {"file_size": len(file)}

@app.post("/upload_img")
def img(file:UploadFile):
    return {"file_name": file.filename}

    
    