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