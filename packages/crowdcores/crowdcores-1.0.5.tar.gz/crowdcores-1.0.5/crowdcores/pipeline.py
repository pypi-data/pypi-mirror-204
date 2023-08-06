import requests
import json
import os

def crowdcores_pipeline(*args,**kwargs):
    return CrowdCoresPipeline(*args, **kwargs);


class CrowdCoresPipeline:
    def __init__(self, *args,**kwargs):
        self.init_args = args
        self.init_kwargs = kwargs
    def __call__(self,*args,**kwargs):
        API_KEY = os.environ.get('CROWDCORES_API_KEY', 'demo_api_key')
        url="http://process.crowdcores.com";
        data = {'args':args,'kwargs':kwargs,'init_args':self.init_args,'init_kwargs':self.init_kwargs}
        json_data = json.dumps(data)
        headers = {
            'Content-type': 'application/json',
            'X-API-Key': API_KEY,
        }
        x = requests.post(url, headers=headers, data=json_data)
        
        data=x.json()
        if data["success"] == 1:
            return data["pipeline_response_result"]
        if data["success"] == 0:
            raise getattr(__builtins__, data["exception_name"])(data["exception_message"])
