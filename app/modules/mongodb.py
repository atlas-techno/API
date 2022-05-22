from hashlib import new
import pymongo
from pymongo import MongoClient

cluster = "mongodb+srv://atlas-techno:Atlas132@cluster0.wts6q.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(cluster)

AtlasDB = client["AtlasDB"]

users = AtlasDB["users"]
workspaces = AtlasDB["workspaces"]
vpcs = AtlasDB["vpcs"]
subnets = AtlasDB["subnets"]
instances = AtlasDB["instances"]

def create_workspace(id,name,region):
    try:
        user_schema = {
            "_id":f"{id}",
            "workspaces":[f"{id}"f"{name}"]
        }

        workspace_schema = { 
            "_id":f"{id}"f"{name}",
            "owner":f"{id}",
            "name":f"{name}",
            "region":f"{region}",
            "vpcs":[]
        }
        users.insert_one(user_schema)
        workspaces.insert_one(workspace_schema)
    except:
        workspace_schema = { 
            "_id":f"{id}"f"{name}",
            "owner":f"{id}",
            "name":f"{name}",
            "region":f"{region}",
            "vpcs":[]
        }
        workspaces.insert_one(workspace_schema)

def create_vpc(id,workspace,name,cidr_block):
    vpc_schema = {
        "_id":f"{workspace}"f"{name}",
        "owner":f"{workspace}",""
        "name":f"{name}",
        "cidr_block":f"{cidr_block}",
        "subnets": []
    }
    vpcs.insert_one(vpc_schema)
    workspaces.find_one_and_update(
        {
            "_id":f"{id}"f"{workspace}"
        },
        {
            "$push":
            {
                "vpcs":f"{workspace}"f"{name}"
            }
        }
    )

def create_subnet(id,workspace,resource_name,vpc_name,cidr_block):
    subnet_schema = {
        "_id":f"{vpc_name}"f"{resource_name}",
        "owner":f"{vpc_name}",
        "resource_name":f"{resource_name}",
        "cidr_block":f"{cidr_block}",
        "instances":[]
    }
    subnets.insert_one(subnet_schema)
    vpcs.find_one_and_update(
        {
            "_id":f"{workspace}"f"{vpc_name}"
        },
        {
            "$push":
            {
                "subnets":f"{vpc_name}"f"{resource_name}"
            }
        }
    )

def create_instance(resource_name,ami,type,count,volume_size,volume_type,delete_on_termination,subnet_name):
    instance_schema = {
        "_id":f"{subnet_name}"f"{resource_name}",
        "owner":f"{subnet_name}",
        "resource_name":f"{resource_name}",
        "ami":f"{ami}",
        "type":f"{type}",
        "count":f"{count}",
        "volume_size":f"{volume_size}",
        "volume_type":f"{volume_type}",
        "delete_on_termination":f"{delete_on_termination}"
    }
    instances.insert_one(instance_schema)
    vpc = subnets.find_one({"resource_name":f"{subnet_name}"})["owner"]
    subnets.find_one_and_update(
        {
            "_id":f"{vpc}"f"{subnet_name}"
        },
        {
            "$push":
            {
                "instances":f"{subnet_name}"f"{resource_name}"
            }
        }
    )

def query_workspaces(id):
    workspaces_list = workspaces.find({"owner":f"{id}"})
    return workspaces_list    

def query_vpcs(id,workspace):
    workspaces_list = workspaces.find_one({"_id":f"{id}"f"{workspace}"})["vpcs"]
    vpc_list = [vpcs.find_one({"_id":f"{x}"}) for x in workspaces_list]
    return vpc_list

def query_subnets(id,workspace,vpc_name):
    user = users.find_one({"_id":f"{id}"}) #Retorna um Dict
    #print(f"\n\n\n\n User: {user}\n\n\n\n\n")

    workspace_objs_list = [workspaces.find_one({"_id":f"{x}"}) for x in user["workspaces"]] # Retonar uma lista de workspaces em forma de objetos
    #print(f"\n\n\n\n Workspace_list: {workspace_objs_list}\n\n\n\n\n")

    selected_vpc = ""

    for x in workspace_objs_list:
        if x["name"] == workspace:
            for y in x["vpcs"]:
                if y == f"{workspace}"f"{vpc_name}":
                    selected_vpc = y 
  
    vpc = vpcs.find_one({"_id":f"{selected_vpc}"})
    subnet_list = vpc["subnets"]
    subnet_list_obj = []
    for x in subnet_list:
        subnet_obj = subnets.find_one({"_id":f"{x}"})
        subnet_list_obj.append(subnet_obj)
    return subnet_list_obj

def query_instance(user,workspace,vpc_name,subnet_id):
    subnet_list = query_subnets(user,workspace,vpc_name)

    for subnet in subnet_list:
        if subnet["resource_name"] == subnet_id:
            print(subnet_id)
            instance_list = []
            instance_list = subnet["instances"]
            instance_obj = [instances.find_one({"_id":f"{x}"}) for x in instance_list]
            return instance_obj
