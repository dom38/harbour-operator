import kopf
import logging
import os
import requests

harbour_url = os.getenv("HARBOUR_URL")
harbour_password = os.getenv("HARBOUR_PASSWORD")
harbour_username = os.getenv("HARBOUR_USERNAME")

# TODO: sort auth

# Projects

@kopf.on.create('harbourprojects')
@kopf.on.update('harbourprojects')
def create_fn(spec, **kwargs):

  logging.debug(f"A creation handler is called with spec: {spec}")

  result = requests.head(f"{harbour_url}/api/v2.0/projects?project_name={spec.name}", auth=(harbour_username, harbour_password))

  logging.debug(f"Result: {result}")

  if result.status_code == 404:
    logging.info(f"Creating new project {spec.name} with visibility {spec.public}")
    data = {
      "project_name": spec.name,
      "public": spec.public
    }
    create_result = requests.post(f"{harbour_url}/api/v2.0/projects", auth=(harbour_username, harbour_password), data=data)
    
  else:
    logging.info(f"Updating existing project {spec.name} with visibility {spec.public}")
    data = {
      "project_name": spec.name,
      "public": spec.public
    }
    create_result = requests.put(f"{harbour_url}/api/v2.0/projects/{spec.name}", auth=(harbour_username, harbour_password), data=data)

  logging.debug(f"Create result: {create_result}")


@kopf.on.delete('harbourprojects')
def create_fn(spec, **kwargs):

  logging.debug(f"A deletion handler is called with spec: {spec}")

  result = requests.delete(f"{harbour_url}/api/v2.0/projects/{spec.name}", auth=(harbour_username, harbour_password))

  logging.debug(f"Delete result: {result}")
