
def build_script(type:str,user:str,workspace:str,*args):
    script = open(f"/atlas/{user}/{workspace}/{type}.tf",mode="a")
    for arg in args:
        script.write(arg)
    script.close()

def aws_provider(access_key="AKIA6FJTISO64JMYRSFH",secret_key="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",region="us-east-1"):
    aws_provider = f'''
provider aws {{
    access_key = "{access_key}"
    secret_key = "{secret_key}"
    region = "{region}"
}}
'''
    return aws_provider

def aws_vpc(resource_name,cidr_block):
    aws_vpc = f'''
resource "aws_vpc" "{resource_name}" {{
    cidr_block  = "{cidr_block}"
    tags = {{
        Name = "{resource_name}"
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

def aws_instance(resource_name,ami,type="t2.micro",count=1,volume_size="8",volume_type="gp2",delete_on_termination="true"):
    aws_instance = f'''
resource "aws_instance" "{resource_name}" {{
    ami = "{ami}"
    instance_type = "{type}"
    count = "{count}"
    tags = {{
        Name = "{resource_name}"
    }}
    root_block_device {{
        volume_size = "{volume_size}"
        volume_type = "{volume_type}"
        delete_on_termination = "{str(delete_on_termination).lower()}"
    }}
}}
'''
    return aws_instance

