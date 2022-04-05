import os
def init_tf(access_key,secret_key,region="us-east-1"):
    return aws_provider(access_key,secret_key,region="us-east-1")

def build_script(file,*args):
    script = open(f'{file}',mode="a")
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

def aws_instance(resource_name,ami,type,tag_name):
    aws_instance = f'''
        resource "aws_instance" "{resource_name}" {{
            ami = "{ami}"
            type = "{type}"
            tags = {{
                Name = "{tag_name}"
            }}
        }}
    '''
    return aws_instance

def is_tf():
    return os.path.isfile("*.tf")