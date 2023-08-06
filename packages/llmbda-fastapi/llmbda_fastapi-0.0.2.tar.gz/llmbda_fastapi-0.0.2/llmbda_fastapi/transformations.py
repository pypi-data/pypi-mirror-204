import os
import json
import atexit
import requests
from fastapi.routing import APIRoute

RELEVANCE_AUTH_TOKEN = os.getenv("RELEVANCE_AUTH_TOKEN")

def routes_to_transformations(api_routes, url, id_suffix=""):
    tfs_list = []
    id_list = []
    for route in api_routes:
        if isinstance(route, APIRoute):
            id_list.append(route.unique_id + id_suffix)
            input_schema = {}
            if route.body_field:
                input_schema = json.loads(route.body_field.type_.schema_json())
                        
            output_schema = {}
            if route.response_field:
                output_schema = json.loads(route.response_field.type_.schema_json())

            if url.endswith("/"):
                full_path = url + route.path
            else:
                full_path = url + "/" + route.path

            tfs_list.append({
                "transformation_id" : route.unique_id + id_suffix,
                "name" : route.summary if route.summary else route.name,
                "description" : route.description,
                "studio_api_path" : full_path,
                "execution_type" : "studio-api",
                "tags" : route.tags,
                "input_schema" : input_schema,
                "output_schema" : output_schema,
            })
    return tfs_list, id_list

def list_transformations():
    url = f"https://api-{RELEVANCE_AUTH_TOKEN.split(':')[2]}.stack.tryrelevance.com"
    results = requests.post(
        f"{url}/latest/studios/transformations/custom/list",
        headers={
            "Authorization" : RELEVANCE_AUTH_TOKEN
        },
        json={
            "page" : 1,
            "page_size" : 10
        }
    )
    print("List of transformations: ", results.json())
    print("Trace-id ", results.headers.get("x-trace-id"))

def cleanup_transformations(transformation_id_list):
    url = f"https://api-{RELEVANCE_AUTH_TOKEN.split(':')[2]}.stack.tryrelevance.com"
    results = requests.post(
        f"{url}/latest/studios/transformations/custom/bulk_delete",
        headers={
            "Authorization" : RELEVANCE_AUTH_TOKEN
        },
        json={"ids": transformation_id_list}
    )
    print("Successfully deleted transformations from cloud: ", results.json())
    print("Trace-id ", results.headers.get("x-trace-id"))

def upload_transformations(tfs):
    url = f"https://api-{RELEVANCE_AUTH_TOKEN.split(':')[2]}.stack.tryrelevance.com"
    results = requests.post(
        f"{url}/latest/studios/transformations/custom/bulk_update",
        headers={
            "Authorization" : RELEVANCE_AUTH_TOKEN
        },
        json={
            "updates": tfs
        }
    )
    print("Uploaded transformations: ", results.json())
    print("Trace-id ", results.headers.get("x-trace-id"))

def create_transformations(api_routes, url, id_suffix=""):
    tfs_list, id_list = routes_to_transformations(api_routes, url, id_suffix=id_suffix)
    upload_transformations(tfs_list)
    atexit.register(cleanup_transformations, id_list)
    return tfs_list