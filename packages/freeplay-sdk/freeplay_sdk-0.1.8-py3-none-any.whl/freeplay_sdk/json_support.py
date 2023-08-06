import json
import logging
import typing as t

import dacite

T = t.TypeVar("T")

__logger = logging.getLogger(__name__)


def force_decode(target_type: t.Type[T], data: bytes) -> T:
    parsed_json = json.loads(data)
    return dacite.from_dict(target_type, parsed_json)


def try_decode(target_type: t.Type[T], data: bytes) -> t.Optional[T]:
    try:
        return force_decode(target_type, data)
    except Exception as e:
        __logger.error(f'There was an error decoding the json, {e}')
        return None
