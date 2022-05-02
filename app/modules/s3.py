import boto3

BUCKET_NAME = "atlas.storage"

s3 = boto3.client("s3")


def push_infra(user,workspace):
    with open(f"/atlas/{user}/{workspace}/terraform.tfstate","rb") as f:
        upload = s3.upload_fileobj(f,BUCKET_NAME,f"/atlas/{user}/{workspace}/terraform.tfstate")
    with open(f"/atlas/{user}/{workspace}/main.tf","rb") as f:
        upload = s3.upload_fileobj(f,BUCKET_NAME,f'/atlas/{user}/{workspace}/main.tf')
    with open(f"/atlas/{user}/{workspace}/provider.tf","rb") as f:
        upload = s3.upload_fileobj(f,BUCKET_NAME,f'/atlas/{user}/{workspace}/provider.tf')

def pull_infra(user,workspace):
    main = s3.download_file(BUCKET_NAME, f'/atlas/{user}/{workspace}/main.tf')
    tfstate = s3.download_file(BUCKET_NAME, f'/atlas/{user}/{workspace}/tfstate.tf')
    provider = s3.download_file(BUCKET_NAME, f'/atlas/{user}/{workspace}/provider.tf')


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