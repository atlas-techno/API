from modules.dirs_manager import *
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

cluster = "mongodb+srv://atlas-techno:Atlas132@cluster0.wts6q.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(cluster)

AtlasDB = client["AtlasDB"]

users = AtlasDB["users"]
workspaces = AtlasDB["workspaces"]
vpcs = AtlasDB["vpcs"]
subnets = AtlasDB["subnets"]
instances = AtlasDB["instances"]

def create_workspace(id,name,region):
    if users.find_one({"_id":id}) == None:
        user_schema = {
            "_id":f"{id}"
        }

        workspace_schema = { 
            "user_id":f"{id}",
            "name":f"{name}",
            "region":f"{region}"
        }
        users.insert_one(user_schema)
        workspaces.insert_one(workspace_schema)
        workspace_id = f'{workspaces.find_one({"user_id":id,"name":name})["_id"]}'
        create_workspace_(id,workspace_id)
        return workspace_id
    else:
        workspace_schema = { 
            "user_id":f"{id}",
            "name":f"{name}",
            "region":f"{region}"
        }
        workspaces.insert_one(workspace_schema)
        workspace_id = f'{workspaces.find_one({"user_id":id,"name":name})["_id"]}'
        create_workspace_(id,workspace_id)
        return workspace_id

def create_vpc(workspace,name,cidr_block):
    vpc_schema = {
        "workspace_id":f"{workspace}",
        "resource_name":f"{name}",
        "cidr_block":f"{cidr_block}",
    }
    vpcs.insert_one(vpc_schema)
    vpc_id = f'{vpcs.find_one({"workspace_id":workspace,"resource_name":name})["_id"]}'
    return vpc_id

def create_subnet(vpc_id,resource_name,cidr_block):
    subnet_schema = {
        "vpc_id":f'{vpc_id}',
        "resource_name":f"{resource_name}",
        "cidr_block":f"{cidr_block}",
    }
    subnets.insert_one(subnet_schema)
    subnet_id = f'{subnets.find_one({"vpc_id":f"{vpc_id}","resource_name":f"{resource_name}"})["_id"]}'
    return subnet_id

def create_instance(subnet_id,resource_name,ami,type,count,volume_size,volume_type,delete_on_termination):
    instance_schema = {
        "subnet_id":f"{subnet_id}",
        "resource_name":f"{resource_name}",
        "ami":f"{ami}",
        "type":f"{type}",
        "count":f"{count}",
        "volume_size":f"{volume_size}",
        "volume_type":f"{volume_type}",
        "delete_on_termination":f"{delete_on_termination}"
    }
    instances.insert_one(instance_schema)
    instance = instances.find_one({"subnet_id":f"{subnet_id}","resource_name":f"{resource_name}"})
    instance["_id"] = f'{instance["_id"]}'
    return instance

def query_workspaces(id):
    user_id = {
        'user_id':f"{id}"
    }

    workspace_object_list = [
        {
            "user_id":x["user_id"],
            "_id":f'{x["_id"]}',
            "name":x["name"],
            "region":x["region"]
        }
        for x in workspaces.find(user_id)
    ]

    return workspace_object_list

def query_vpcs(workspace):
    workspace_id = {
        "workspace_id":f"{workspace}"
    }

    vpc_object_list = [
        {
            "workspace_id":f'{x["workspace_id"]}',
            "_id":f'{x["_id"]}',
            "resource_name":x["resource_name"],
            "cidr_block":x["cidr_block"]
        }
        for x in vpcs.find(workspace_id)
    ]

    return vpc_object_list

def query_subnets(workspace):
    workspace_id = {
        "workspace_id":f"{workspace}"
    }

    subnet_object_list = [] 

    for x in query_vpcs(workspace):
        for y in subnets.find({"vpc_id":f"{x['_id']}"}):
            y["_id"] = f'{y["_id"]}'
            subnet_object_list.append(y)
    return subnet_object_list



def query_instance(workspace):

    instances_object_list = []

    workspace_id = {
        "_id":f"{workspace}"
    }

    for x in query_subnets(workspace):
        for y in instances.find({"subnet_id":f'{x["_id"]}'}):
            y["_id"] = f'{y["_id"]}'
            instances_object_list.append(y)

    return instances_object_list
    