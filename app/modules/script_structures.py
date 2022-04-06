def build_script(*args):
    script = open("main.tf",mode="a")
    for arg in args:
        script.write(arg)
    script.close()

def aws_provider(access_key,secret_key,region="us-east-1"):
    aws_provider = f'''
provider aws {{
    access_key = "{access_key}"
    secret_key = "{secret_key}"
    region = "{region}"
}}
'''
    return aws_provider

def aws_instance(resource_name,ami,type="t2.micro",count=1,tag_name=""):
    aws_instance = f'''
resource "aws_instance" "{resource_name}" {{
    ami = "{ami}"
    instance_type = "{type}"
    count = "{count}"
    tags = {{
        Name = "{tag_name}"
    }}
}}
'''
    return aws_instance

