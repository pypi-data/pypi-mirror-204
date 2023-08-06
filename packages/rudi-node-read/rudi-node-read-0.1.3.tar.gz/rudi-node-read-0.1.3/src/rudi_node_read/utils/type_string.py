from re import compile
from uuid import UUID

from rudi_node_read.utils.log import log_d
from rudi_node_read.utils.types import is_type


def is_string(s):
    return is_type(s, 'str')


ISO_FULL_DATE_REGEX = compile(
    r'^([+-]?[1-9]\d{3})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12]\d)T(2[0-3]|[01]\d):([0-5]\d):([0-5]\d)(?:\.(\d{3}))?('
    r'?:Z|[+-](?:1[0-2]|0\d):[03]0)$')


def is_iso_full_date(date_str):
    return bool(ISO_FULL_DATE_REGEX.match(date_str))


# REGEX_UUID = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')


def is_uuid_v4(uuid: str):
    if uuid is None:
        return False
    try:
        uuid_v4 = UUID(str(uuid))
        if uuid_v4.version == 4:
            return uuid_v4
        else:
            return False
    except ValueError as e:
        return False


def validate_uuid_v4(uuid: str):
    try:
        if uuid is not None:
            uuid_v4 = UUID(str(uuid))
            if uuid_v4.version == 4:
                return str(uuid_v4)
    except ValueError:
        pass
    raise ValueError('System ID should be a UUIDv4')


def slash_join(*args):
    """
    Joins a set of strings with a slash (/) between them (useful for merging URLs or paths fragments)
    """
    non_null_args = []
    for frag in args:
        if frag is None or frag == '':
            pass
        elif not is_string(frag):
            raise AttributeError('input parameters must be strings')
        else:
            non_null_args.append(frag.strip('/'))
    joined_str = '/'.join(non_null_args)
    return joined_str
