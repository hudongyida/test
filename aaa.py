# coding: utf-8

import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkecs.v2 import *

# 全局变量
SERVER_GROUP_NAME = "chinaskills_server_group"
PROJECT_ID = "test123456"  # 替换为您的项目ID

def get_credentials():
    ak = os.environ["CLOUD_SDK_AK"]
    sk = os.environ["CLOUD_SDK_SK"]
    return BasicCredentials(ak, sk, PROJECT_ID)

def create_ecs_client(credentials):
    return EcsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(EcsRegion.value_of("cn-north-4")) \
        .build()

def find_server_group_by_name(client, server_group_name):
    try:
        list_request = ListServerGroupsRequest()
        list_response = client.list_server_groups(list_request)
        for sg in list_response.server_groups:
            if sg.name == server_group_name:
                return sg
        return None
    except exceptions.ClientRequestException as e:
        print(f"Failed to list server groups: {e}")
        return None

def delete_server_group(client, server_group):
    try:
        delete_request = DeleteServerGroupRequest()
        delete_request.server_group_id = server_group.id
        delete_response = client.delete_server_group(delete_request)
        print(f"Deleted server group {server_group.name} with ID {server_group.id}")
    except exceptions.ClientRequestException as e:
        print(f"Failed to delete server group: {e}")

def create_server_group(client, server_group_name):
    try:
        listPoliciesServerGroup = ["anti-affinity"]
        serverGroupBody = CreateServerGroupOption(
            name=server_group_name,
            policies=listPoliciesServerGroup
        )
        request = CreateServerGroupRequest()
        request.body = CreateServerGroupRequestBody(
            server_group=serverGroupBody
        )
        response = client.create_server_group(request)
        print(f"Created server group {server_group_name} with ID {response.server_group.id}")
    except exceptions.ClientRequestException as e:
        print(f"Failed to create server group: {e}")

def show_server_group(client, server_group):
    try:
        show_request = ShowServerGroupRequest()
        show_request.server_group_id = server_group.id
        response = client.show_server_group(show_request)
        print(f"Details of server group {server_group.name}:")
        print(response)
    except exceptions.ClientRequestException as e:
        print(f"Failed to retrieve server group details: {e}")

if __name__ == "__main__":
    credentials = get_credentials()
    client = create_ecs_client(credentials)

    # 查找服务器组
    server_group = find_server_group_by_name(client, SERVER_GROUP_NAME)

    if server_group:
        # 如果服务器组存在，则删除它
        delete_server_group(client, server_group)
        # 重新创建服务器组
        create_server_group(client, SERVER_GROUP_NAME)
    else:
        # 如果服务器组不存在，则创建它
        create_server_group(client, SERVER_GROUP_NAME)

    # 查询并输出服务器组的详细信息
    server_group = find_server_group_by_name(client, SERVER_GROUP_NAME)
    if server_group:
        show_server_group(client, server_group)