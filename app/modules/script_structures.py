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

def aws_vpc(resource_name,cidr_block,tag_name=""):
    aws_vpc = f'''
resource "aws_vpc" "{resource_name}" {{
    cidr_block  = "{cidr_block}"
    tags = {{
        Name = "{tag_name}"
    }}
}}
'''
    return aws_vpc

def aws_subnet(resource_name,vpc_name,cidr_block,tag_name=""):
    aws_subnet = f'''
resource "aws_subnet" "{resource_name}" {{
    vpc_id = aws_vpc.{vpc_name}.id
    cidr_block = "{cidr_block}"
    tags = {{
        Name = "{tag_name}"
    }}
}}    
'''
    return aws_subnet

def aws_instance(resource_name,ami,type="t2.micro",count=1,tag_name="",delete_on_termination="true"):
    aws_instance = f'''
resource "aws_instance" "{resource_name}" {{
    ami = "{ami}"
    instance_type = "{type}"
    count = "{count}"
    tags = {{
        Name = "{tag_name}"
    }}
    root_block_device {{
        delete_on_termination = "{delete_on_termination}"
    }}
}}
'''
    return aws_instance
