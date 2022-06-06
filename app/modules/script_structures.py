from modules.mongodb import query_subnets, query_vpcs
def build_script(type:str,user:str,workspace:str,*args):
    script = open(f"/atlas/{user}/{workspace}/{type}.tf",mode="a")
    for arg in args:
        script.write(arg)
    script.close()

def aws_provider(access_key="AKIA6FJTISO6YSYK7VZ2",secret_key="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",region="us-east-1"):
    aws_provider = f'''
provider aws {{
    access_key = "{access_key}"
    secret_key = "{secret_key}"
    region = "{region}"
}}
'''
    return aws_provider

def variables():
    variables = f'''
#Blocos de ip:

variable "blocos" {{
  type = list(string)
  default = [
    "10.0.0.0/16",
    "172.16.0.0/16",
    "192.168.0.0/24"
  ]
  description = "Blocos de IPS para serem usados na VPC"
}}

#Regiões de vpc

variable "regions" {{
  type = list(string)
  default = [
    "us-east-1",
    "us-east-2",
    "sa-east-1"
  ]
  description = "Regioes para serem usadas em VPCs"
}}

#Ips de subnet

variable "Range" {{
  type = list(string)
  default = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24",
    "10.0.4.0/24",
    "172.16.1.0/24",
    "172.16.2.0/24",
    "172.16.3.0/24",
    "172.16.4.0/24",
    "192.168.1.0/24",
    "192.168.2.0/24",
    "192.168.3.0/24",
    "192.168.4.0/24"

  ]
  description = "Intervalo de IPs para Subnets"
}}

variable "Zonas" {{
  type = list(string)
  default = [
    "us-east-1a",
    "us-east-1b",
    "us-east-1c",
    "us-east-2a",
    "us-east-2b",
    "us-east-2c",
    "sa-east-1a",
    "sa-east-1b",
    "sa-east-1c"
  ]

}}

#EC2

#AMIs:

variable "amis" {{
  type = list(string)
  default = [
    "ami-04505e74c0741db8d",
    "ami-07d02ee1eeb0c996c",
    "ami-0f9a92942448ac56f",
    "ami-0745142a642f5af3a"
  ]
}}


variable "groupnumber" {{
  type = list(string)
  default = [
    "22",
    "tcp",
    "443",
    "80",
    "udp",
    "0.0.0.0/0"
  ]
}}
'''
    return variables

def aws_vpc(resource_name,cidr_block=0):
    aws_vpc = f'''
resource "aws_vpc" "{resource_name}_vpc" {{
    cidr_block  = var.blocos[{cidr_block}]
    enable_dns_hostnames = true
    tags = {{
        Name = "{resource_name}"
    }}
}}

resource "aws_internet_gateway" "{resource_name}_igw" {{
  vpc_id = aws_vpc.{resource_name}_vpc.id
}}
'''
    return aws_vpc

def aws_subnet_public(resource_name,vpc_name,cidr_block=0):
    aws_subnet = f'''
#{resource_name}_igw
resource "aws_subnet" "{resource_name}_subnet" {{
    vpc_id = aws_vpc.{vpc_name}_vpc.id
    cidr_block = var.Range[{cidr_block}]
    tags = {{
        Name = "{resource_name}"
    }}
}}   

resource "aws_route_table" "{resource_name}_route" {{
  vpc_id = aws_vpc.{vpc_name}_vpc.id

  route {{
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.{vpc_name}_igw.id
  }}
}}

resource "aws_route_table_association" "{resource_name}_assoc" {{
  subnet_id      = aws_subnet.{resource_name}_subnet.id
  route_table_id = aws_route_table.{resource_name}_route.id
}}

'''
    return aws_subnet


def aws_subnet_private(resource_name,vpc_name,cidr_block=0):
  aws_subnet_private = f'''
resource "aws_subnet" "{resource_name}_subnet" {{
    vpc_id = aws_vpc.{vpc_name}_vpc.id
    cidr_block = var.Range[{cidr_block}]
    tags = {{
        Name = "{resource_name}"
    }}
}} 


resource "aws_eip" "{resource_name}_eip" {{
  vpc = true
}}

resource "aws_nat_gateway" "{resource_name}_nat_gw" {{
  allocation_id = aws_eip.{resource_name}_eip.id
  subnet_id     = aws_subnet.{resource_name}_subnet.id
}}

resource "aws_route_table" "{resource_name}_route" {{
  vpc_id = aws_vpc.{vpc_name}_vpc.id


  route {{
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.{resource_name}_nat_gw.id
  }}
}}

resource "aws_route_table_association" "private-assoc" {{
  subnet_id      = aws_subnet.{resource_name}_subnet.id
  route_table_id = aws_route_table.{resource_name}_route.id
}}  
'''
  return aws_subnet_private

def aws_instance(workspace,resource_name,ami,type="t2.micro",count=1,volume_size="8",volume_type="gp2",delete_on_termination="true",subnet_name="",key_name=""):
  vpc_id = ""
  vpc_name = ""
  for x in query_subnets(workspace):
    if x["resource_name"] == subnet_name:
      vpc_id = x["vpc_id"]
  for x in query_vpcs(workspace):
    if x["_id"] == vpc_id:
      vpc_name = x["resource_name"]
      
    aws_instance = f'''
resource "aws_instance" "{resource_name}_instance" {{
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
    subnet_id = aws_subnet.{subnet_name}_subnet.id
    associate_public_ip_address = true
    key_name = aws_key_pair.{key_name}_key.id
    security_groups = [aws_security_group.{resource_name}_sg.id]
}}

resource aws_security_group "{resource_name}_sg" {{
  vpc_id = aws_vpc.{vpc_name}_vpc.id
  ingress {{
    cidr_blocks = ["0.0.0.0/0"]
    protocol = "-1"
    from_port = 0
    to_port = 0
  }}
  egress {{
    cidr_blocks = ["0.0.0.0/0"]
    protocol = "-1"
    to_port = 0
    from_port = 0
  }}
}}
'''
    return aws_instance

def aws_key_pair(user,workspace,key_name):
  aws_key_pair = f'''
resource "aws_key_pair" "{key_name}_key" {{
  key_name   = "{key_name}"
  public_key = file("/atlas/{user}/{workspace}/keys/{key_name}.pem.pub")
}}
'''
  return aws_key_pair

