from abc import ABC, abstractmethod
from json import JSONDecodeError

import requests

import ripio
from ripio.exceptions.auth import UnathorizedClient
from ripio.exceptions.response import NotSuccessfulResponse


class RipioClient(ABC):
    auth_mandatory = False

    def __init__(self, api_key=None):
        self.session = requests.Session()
        self.api_key = ripio.api_key if api_key is None else api_key

    """
    Client Manager Specific Methods
    """
    def get_params_from_locals(self, local_vars, exclude_vars=[]):
        return {
            key: local_vars[key]
            for key in local_vars
            if key != "self" and local_vars[key] is not None and key not in exclude_vars
        }

    def process_arguments(self, **kwargs):
        client_kwargs = {"success_status_code": kwargs["success_status_code"]}
        del kwargs["success_status_code"]
        request_kwargs = kwargs
        return request_kwargs, client_kwargs

    def process_response(self, response, client_kwargs):
        response_body = self.get_response_body(response)
        if "success_status_code" in client_kwargs:
            if response.status_code == client_kwargs["success_status_code"]:
                return response_body
            else:
                message = f"{response.status_code} : {response_body}"
                raise NotSuccessfulResponse(message)
        else:
            return response_body

    def get_response_body(self, response):
        try:
            json_body = response.json()
            if "data" in json_body:
                return json_body["data"]
            else:
                return json_body
        except JSONDecodeError:
            return response.text

    def remove_null_from_request_body(self, request_dict):
        return {
            key: value
            for key, value in request_dict.items()
            if value is not None
        }

    def check_api_key(func):
        def checker(self, *args, **kwargs):
            if self.api_key is None:
                raise UnathorizedClient("No credentials were passed")
            self.authenticate_session()
            return func(self, *args, **kwargs)

        return checker

    def check_api_auth(self):
        if self.api_key is None and self.auth_mandatory:
            message = "Auth credenatials are mandatory for this client"
            raise UnathorizedClient(message)
        elif self.auth_mandatory:
            self.authenticate_session()

    # Destructor method to free up resources
    def __del__(self):
        self.session.close()

    # Abstract method used to enabled children implent their own Authentication
    # Over the session
    @abstractmethod
    def authenticate_session(self):
        pass

    """
    HTTP supported methods handlers
    """

    def get(self, *args, **kwargs):
        request_kwargs, client_kwargs = self.process_arguments(**kwargs)
        response = self.session.get(*args, **request_kwargs)
        return self.process_response(response, client_kwargs)

    def put(self, *args, **kwargs):
        request_kwargs, client_kwargs = self.process_arguments(**kwargs)
        response = self.session.get(*args, **request_kwargs)
        return self.process_response(response, client_kwargs)

    def post(self, *args, **kwargs):
        request_kwargs, client_kwargs = self.process_arguments(**kwargs)
        response = self.session.post(*args, **request_kwargs)
        return self.process_response(response, client_kwargs)

    def delete(self, *args, **kwargs):
        request_kwargs, client_kwargs = self.process_arguments(**kwargs)
        response = self.session.delete(*args, **request_kwargs)
        return self.process_response(response, client_kwargs)
