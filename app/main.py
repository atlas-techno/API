from re import S
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.file_manager import dictify
from modules.script_structures import aws_provider, aws_instance, build_script
from modules.resources import Ec2
from modules.terraform_controller import plan_and_apply, destroy

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

@app.post("/create-ec2")
def create_ec2(ec2:Ec2):
    ec2 = dictify(ec2)
    build_script(
        aws_instance(ec2["resource_name"],ec2["ami"],ec2["type"],ec2["tag_name"])
    )
    return {"Status": f'Your EC2 has been created with this configuration: {ec2}'}

@app.get("/deploy")
def deploy():
    plan_and_apply()
    return {"Status":"Your infrastructure has been deployed"}

@app.get('/destroy')
def destroy():
    destroy()
    return {"Status":"Your infrastructure has been destroyed"}

@app.get('/inspect')
def inspect_code():
    f=open("main.tf",mode="r")
    text = f.read()
    return text
