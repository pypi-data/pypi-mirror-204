import requests, time
import core.sdk.helper as Helper
from models.shared.shared_pb2 import RunnerInput
from core.types import Finding, Configuration

class TythonApiService:
    '''
    Provides access to the tython api
    '''
    def get_default_environment(config: Configuration):
        '''
        Gets the default environment_id
        '''
        url = f"{config.data_endpoint}{config.org_id}/projectEnvironment/{config.project_id}/default"
        response = requests.get(url, auth=(config.org_id, config.api_key))

        if response.status_code != 200:
            raise Exception("Unable to get default environment, verify your credentials.")
        
        environment_result = response.json()
        environment_id = "" if "projectId" not in environment_result else environment_result["projectId"]

        if not environment_id:
            raise Exception("Unable to get default environment, verify your credentials.")

        return environment_id


    def build_app(config: Configuration, environment_id: str):
        '''
        Triggers build app endpoint
        '''
        url = f"{config.data_endpoint}{config.org_id}/sac/{config.project_id}/build/{environment_id}"
        response = requests.post(url, auth=(config.org_id, config.api_key))

        if response.status_code != 200:
            raise Exception("Unable to trigger build app, verify your credentials.")
        
        build_app_result = response.json()
        request_id = "" if "requestId" not in build_app_result else build_app_result["requestId"]

        return request_id


    def fetch_graph_data(config: Configuration, environment_id: str, request_id: str):
        '''
        Fetch projects graph data
        '''
        url = f"{config.data_endpoint}{config.org_id}/sac/{config.project_id}/resourcegraph/{environment_id}/{request_id}"
        timeout=600
        poll_interval=15
        start_time = time.time()
        while True:
            response = requests.get(url, auth=(config.org_id, config.api_key))
            if response.status_code == 200:
                break
            elif time.time() - start_time > timeout:
                raise Exception(f"Unable to fetch {config.project_id} data, please verify your credentials.")
            time.sleep(poll_interval)

        runner_inputs = []

        raw_snake_case_input = Helper.snake_case_json(response.json())

        for raw_item in raw_snake_case_input:
            item = raw_item['item1']
            for root_node in item['graph']['root_nodes']:
                root_node['node']['resource']['data']['value'] = bytes(root_node['node']['resource']['data']['value'])
            Helper.remove_attributes(item, "has_")
            runner_inputs.append(RunnerInput(**item))

        return runner_inputs


    def apply_findings(config: Configuration, findings: list[Finding], environment_id: str, request_id : str):
        '''
        Apply a findings list to the oak9 project
        '''
        design_gaps = []
        capability_number = 1

        for finding in findings:
            if finding:
                design_gaps.append(
                    {
                        "capabilityId": f"{config.org_id}.{capability_number}",
                        "capabilityName": finding.desc,
                        "source": "",
                        "resourceName": finding.resource_metadata.resource_name,
                        "resourceId": finding.resource_metadata.resource_id,
                        "resourceType": finding.resource_metadata.resource_type,
                        "resourceGap": "",
                        "resourceImpact": "",
                        "violations": [finding.to_violation().__json__()],
                        "oak9Guidance": "",
                        "mappedIndustryFrameworks": []
                    }
                )
                capability_number += 1

        payload = {
            "runtime": "Python",
            "author": "",
            "designGaps": design_gaps
        }

        url = f"{config.data_endpoint}{config.org_id}/sac/{config.project_id}/apply/{environment_id}/{request_id}"
        response = requests.post(url, auth=(config.org_id, config.api_key), json=payload)

        if response.status_code != 200:
            raise Exception(f"Unable to apply {config.project_id} findings, please verify your credentials.")
        
        #TODO: handle response details
    
