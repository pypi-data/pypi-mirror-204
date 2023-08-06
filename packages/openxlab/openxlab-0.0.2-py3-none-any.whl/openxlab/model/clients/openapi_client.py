import requests

from openxlab.model.common.constants import paths
from openxlab.model.common.response_dto import ReturnDto
import os


class OpenapiClient(object):
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token

    # def get_dataset_files(self, dataset_name:str, prefix:str):
    def get_download_url(self, repository, file):
        """
        get file(model file|meta file|log file|readme file) download url
        """
        client_from = os.environ.get('CLIENT_FROM', '0')
        payload = {"repositoryName": repository, "fileName": file, "clientFrom": client_from}
        path = paths['file_download_path']
        response_dto = self.http_post_response_dto(path, payload)
        if response_dto.msg_code != '10000':
            raise ValueError(f"Get download url error:{response_dto.msg}, traceId:{response_dto.trace_id}")
        if response_dto.data['msgCode'] != '10000':
            raise ValueError(f"Get download url error:{response_dto.data['msg']}, "
                             f"traceId:{response_dto.data['traceId']}")
        return response_dto.data['data']['url']

    def get_metafile_template_download_url(self, file=None):
        """
        get metafile template download url
        """
        payload = {}
        path = paths['meta_file_template_download_path']
        response_dto = self.http_post_response_dto(path, payload)
        if response_dto.msg_code != '10000':
            raise ValueError(f"Get download url error:{response_dto.msg}, traceId:{response_dto.trace_id}")
        if response_dto.data['msgCode'] != '10000':
            raise ValueError(f"Get download url error:{response_dto.data['msg']}, "
                             f"traceId:{response_dto.data['traceId']}")
        return response_dto.data['data']['url']

    def http_post_response_dto(self, path, payload):
        headers = self.http_common_header()
        print(f"endpoint:{self.endpoint}{path}")
        response = requests.post(f"{self.endpoint}{path}", json=payload, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        response_dto = ReturnDto.from_camel_case(response_dict)
        return response_dto

    def http_common_header(self):
        header_dict = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        return header_dict
