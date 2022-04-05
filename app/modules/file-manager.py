block = f'''
    provider aws {{
        region = "us-east-1"
        access_key = "AKIA6FJTISO64JMYRSFH"
        secret_key = "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"
    }}
'''

def create_file(name="main.tf"):
    f = open(f'{name}',mode="a")
    return name

def edit_file(file):
    return open(f'{file}',mode="a")

def dictify(object):
    return object.dict()
    

def create_ec2_file(ec2,validator):
    file = edit_file(create_file())
    file.write(
    f'''
    resource "aws_instance" "{ec2["resource_name"]}" {{ 
        ami = "{ec2["ami"]}"
        instance_type = "{ec2["type"]}"
        count = "{ec2["count"]}"
        tags = {{
            Name = "{ec2["tag_name"]}"
        }}
    }}
    ''')
    file.close()
