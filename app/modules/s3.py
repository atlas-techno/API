import boto3
import os
from modules.mongodb import query_workspaces

BUCKET_NAME = "atlas.storage"

s3 = boto3.client("s3")


def push_infra(user,workspace):
    #with open(f"/atlas/{user}/{workspace}/terraform.tfstate","rb") as f:
     #   upload = s3.upload_fileobj(f,BUCKET_NAME,f"/atlas/{user}/{workspace}/terraform.tfstate")
    with open(f"/atlas/{user}/{workspace}/main.tf","rb") as f:
        upload = s3.upload_fileobj(f,BUCKET_NAME,f'/atlas/{user}/{workspace}/main.tf')

    with open(f"/atlas/{user}/{workspace}/provider.tf","rb") as f:
        upload = s3.upload_fileobj(f,BUCKET_NAME,f'/atlas/{user}/{workspace}/provider.tf')

    with open(f'/atlas/{user}/{workspace}/var.tf',"rb") as f:
        upload = s3.upload_fileobj(f,BUCKET_NAME,f'/atlas/{user}/{workspace}/var.tf')
        
    with open(f'/atlas/{user}/{workspace}/terraform.tfstate','rb') as f:
        upload = s3.upload_fileobj(f,BUCKET_NAME,f'/atlas/{user}/{workspace}/terraform.tfstate')

def pull_infra(user,workspace):
    main = s3.download_file(BUCKET_NAME,f'/atlas/{user}/{workspace}/main.tf',f'/atlas/{user}/{workspace}/main.tf')

    tfstate = s3.download_file(BUCKET_NAME,f'/atlas/{user}/{workspace}/terraform.tfstate',f'/atlas/{user}/{workspace}/terraform.tfstate')

    provider = s3.download_file(BUCKET_NAME,f'/atlas/{user}/{workspace}/provider.tf',f'/atlas/{user}/{workspace}/provider.tf')

    variables = s3.download_file(BUCKET_NAME,f'/atlas/{user}/{workspace}/var.tf',f'/atlas/{user}/{workspace}/var.tf')


def push_key(user,workspace,key_name):
    with open(f"/atlas/{user}/{workspace}/keys/{key_name}.pem","rb") as f:
        upload = s3.upload_fileobj(f,BUCKET_NAME,f'/atlas/{user}/{workspace}/keys/{key_name}.pem') 
    
def pull_key(user,workspace,key_name):
    main = s3.download_file(BUCKET_NAME,f'/atlas/{user}/{workspace}/keys/{key_name}.pem',f'/atlas/{user}/{workspace}/keys/{key_name}.pem')

def query_keys_s3(user,workspace):
    key_list = os.listdir(f"/atlas/{user}/{workspace}/keys")
    return key_list

def create_presigned_url(bucket_name, object_name, expiration=60):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    response = s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)

    return response


""" List All Buckets
buckets_list = s3.list_buckets()
for bucket in buckets_list["Buckets"]:
    print(bucket)
"""

""" List all Objects in a Bucket 
response = s3.list_objects_v2(Bucket=BUCKET_NAME)
"""

""" Upload Binary
with open("file","rb") as f:
    upload = s3.upload_fileobj(f,"BUCKET_NAME","file")
"""

""" Download
download = s3.download_file(BUCKET_NAME, "/atlas/weslley/ianzola/main.tf")
"""

""" Download Image Binay
with open("file","wb"):
    binary = s3.download_fileobj(f,BUCKET_NAME,"file")
"""