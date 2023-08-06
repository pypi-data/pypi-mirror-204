import requests
from requests.exceptions import HTTPError
from requests.adapters import HTTPAdapter, Retry

session = requests.Session()


def get_request(url, params=None, timeout=None, retries: int = None, retry_list: list = None, **kwargs):
    try:
        retry = __configure_retires(retries=retries, retry_list=retry_list)
        session.mount('http://', HTTPAdapter(max_retries=retry))
        response = session.get(url=url, params=params, headers=kwargs, timeout=timeout)
        return response

    except HTTPError as http_error:
        return http_error

    except Exception as error:
        return error


def delete_request(url, params, timeout=None, retries: int = None, retry_list: list = None, **kwargs):
    try:
        retry = __configure_retires(retries=retries, retry_list=retry_list)
        session.mount('http://', HTTPAdapter(max_retries=retry))
        response = session.delete(url=url, params=params, headers=kwargs, timeout=timeout)
        return response
    except HTTPError as http_error:
        return http_error
    except Exception as error:
        return error


def post_request(url, data, timeout=None, retries: int = None, retry_list: list = None, **kwargs):
    try:
        retry = __configure_retires(retries=retries, retry_list=retry_list)
        session.mount('http://', HTTPAdapter(max_retries=retry))
        response = session.post(url=url, json=data, params=kwargs, headers=kwargs, timeout=timeout)
        return response

    except HTTPError as http_error:
        return http_error
    except Exception as error:
        return error


def put_request(url, data, timeout=None, retries: int = None, retry_list: list = None, **kwargs):
    try:
        retry = __configure_retires(retries=retries, retry_list=retry_list)
        session.mount('http://', HTTPAdapter(max_retries=retry))
        response = session.put(url=url, json=data, params=kwargs, headers=kwargs, timeout=timeout)
        return response
    except HTTPError as http_error:
        return http_error
    except Exception as error:
        return error


def __configure_retires(retries: int, retry_list: list):
    retries = Retry(total=retries,
                    backoff_factor=0.1,
                    status_forcelist=retry_list)
    return retries
