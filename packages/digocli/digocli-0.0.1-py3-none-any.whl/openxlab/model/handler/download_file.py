"""
Download function for related files in the reality model library
"""
import logging
import re
from tqdm import tqdm
import requests

from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.common.constants import endpoint, token, default_metafile_template_name

logger = logging.getLogger("openxlab.model")


def _download(model_repo, file) -> None:
    """
    download model file|meta file|log filee|readme file
    usage: cli & sdk
    """
    try:
        # split params
        username, repository = _split_repo(model_repo)
        client = OpenapiClient(endpoint, token)
        url = client.get_download_url(repository, file)
    except ValueError as e:
        print(f"Error: {e}")
        return
    _download_to_local(url, file)
    print("download model repo:{}, file:{}".format(model_repo, file))


def _download_metafile_template(file=None) -> None:
    """
    download metafile template file
    """
    try:
        # split params
        client = OpenapiClient(endpoint, token)
        url = client.get_metafile_template_download_url()
    except ValueError as e:
        print(f"Error: {e}")
        return
    file = file if file is not None else default_metafile_template_name
    _download_to_local(url, file)
    print("download metafile file:{}".format(file))


def _split_repo(model_repo) -> (str, str):
    """
    Split a full repository name into two separate strings: the username and the repository name.
    """
    # username/repository format check
    pattern = r'^[a-zA-Z0-9]+\/[a-zA-Z0-9\-_]+$'
    if not re.match(pattern, model_repo):
        raise ValueError("The input string must be in the format 'didi12/test-d-1'")

    values = model_repo.split('/')
    return values[0], values[1]


def _download_to_local(url, file) -> None:
    """
    download file to local with progress_bar
    """
    response = requests.get(url, stream=True)

    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    with open(file, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

# def _get_download_url(url, payload) -> dict:
#     """
#     获取文件下载路径
#     """
#     response = requests.post(url, json=payload)
#     response.raise_for_status()  # 抛出异常如果状态码不是200
#     response_dict = response.json()  # 转换为Python字典格式
#     response_dto = ReturnDto.from_camel_case(response_dict)
#     if response_dto.msg_code != '10000':
#         raise ValueError(f"Get download url error:{response_dto.msg}, traceId:{response_dto.trace_id}")
#     return response_dto.data['url']
