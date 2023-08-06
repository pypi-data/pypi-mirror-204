from typing import get_args

from rudi_node_read.utils.type_string import slash_join


class MissingEnvironmentVariableException(Exception):
    def __init__(self, var_name: str, var_use: str = ''):
        super().__init__(f'an environment variable should be defined {var_use}: {var_name}')


class IniMissingValueException(Exception):
    def __init__(self, ini_section: str, ini_subsection: str, err_msg: str):
        super().__init__(f'Missing value in INI config file for parameter {ini_section}.{ini_subsection}: {err_msg}')


class IniUnexpectedValueException(Exception):
    def __init__(self, ini_section: str, ini_subsection: str, err_msg: str):
        super().__init__(f'Unexpected value in INI config file for parameter {ini_section}.{ini_subsection}: {err_msg}')


class UnexpectedValueException(Exception):
    def __init__(self, param_name: str, expected_val, received_val):
        super().__init__(
            f"Unexpected value for parameter '{param_name}': expected '{expected_val}', got '{received_val}'")


class LiteralUnexpectedValueException(Exception):
    def __init__(self, err_msg, expected_literal, received_val):
        super().__init__(f"{err_msg}. Expected {get_args(expected_literal)}, got '{received_val}'")


def rudi_api_http_error_to_string(status, err_type, err_msg):
    return f"ERR {status} {err_type}: {err_msg}"


class HttpError(Exception):
    def __init__(self, err, req_method=None, base_url=None, url=None):
        err_msg = f"{err}"
        if type(err) is dict and 'error' in err and 'message' in err:
            if 'status' in err:
                err_msg = rudi_api_http_error_to_string(err['status'], err['error'], err['message'])
            elif 'statusCode' in err:
                err_msg = rudi_api_http_error_to_string(err['statusCode'], err['error'], err['message'])
        if req_method and base_url:
            err_msg = f"for request '{req_method} {slash_join(base_url, url)}' -> {err_msg}"
        super().__init__(f'HTTP ERR {err_msg}')
