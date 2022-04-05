from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.file_manager import create_file, dictify
from modules.script_structures import is_tf, init_tf, aws_provider, aws_instance, build_script
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

@app.post("/create-ec2")
def create_ec2(ec2:Ec2):
    if is_tf() == False: 
        init_tf()
    ec2 = dictify(ec2)
    build_script(
        create_file(),
        aws_provider(access_key, secret_key),
        aws_instance(ec2["resource_name"],ec2["ami"],ec2["type"],ec2["tag_name"])
    )
    return ec2

@app.get("/deploy")
def deploy():
    pass
@app.get('/destroy')
def destroy():
    pass
@app.get('/inspect')
def inspect_code():
    f=open("main.tf",mode="r")
    text = f.read()
    return text
