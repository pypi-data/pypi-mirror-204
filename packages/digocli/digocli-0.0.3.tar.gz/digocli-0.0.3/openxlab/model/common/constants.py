"""
model module constant define
"""

model_openapi_url_prefix_dev = "https://dev.openapi.openxxlab.com/api/v1"
model_openapi_url_prefix_prod = "https://openapi.openxlab.org.cn/api/v1"
model_url_prefix_dev = "http://localhost:10019"
# temp token
token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI1OTcwOTEiLCJyb2wiOiJST0xFX0FETUlOIiwiaXNzIjoiT3BlblhMYWIiLCJpYXQiOjE2ODE5Njg4NzMsInBob25lIjoiIiwiYWsiOiI2cHFnOXprNmRteG9rZ2JnbHZvayIsImVtYWlsIjoiZG9uZ3hpYW96aHVhbmdAcGpsYWIub3JnLmNuIiwiZXhwIjoxNzEzNTA0ODczfQ.eFl8ZH9tDp-pcjY3wz6PeNBarJwhVx90qQ3h82Qvpf0hrcrdrQSBcI8AmEk2TZFpeViC6HBtXRxxGp2YLK1XkA"
endpoint = model_openapi_url_prefix_dev
paths = {
    'file_download_path': '/model-center/api/v1/cli/repository/getFileDownloadUrl',
    'meta_file_template_download_path': '/model-center/api/v1/cli/repository/getMetafileTemplateUrl',
}
default_metafile_template_name = 'metafile_template.yaml'
