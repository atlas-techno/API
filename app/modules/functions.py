from random import randrange

def create_file(name="main.tf"):
    f = open(f'{name}',mode="x")
    return name

def edit_file(file):
    return open(f'{file}',mode="w")

def format_ec2(object):
    ec2 = object.dict()
    ec2["id"] = randrange(0,100000)
    create_ec2_file(ec2)
    return ec2

def create_ec2_file(ec2):
    file = edit_file(create_file())
    file.write(
    f'''
    provider aws {{
        region = "us-east-1"
        access_key = "AKIA6FJTISO64JMYRSFH"
        secret_key = "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"
    }}

    resource "aws_instance" "atlas_ec2" {{ 
        ami = "{ec2["ami"]}"
        instance_type = "{ec2["type"]}"
        count = "{ec2["count"]}"
        tags = {{
            Name = "{ec2["name"]}"
        }}
    }}
    ''')
    file.close()
