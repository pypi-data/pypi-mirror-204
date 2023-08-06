from collections.abc import Mapping
from enum import Enum
from types import SimpleNamespace

import rapidjson as rj  # noqa pycharm?

from .abc import SerializerInterface, Serializable
from .etc import MimeTypes

__all__ = ('dumps', 'dumps_bytes', 'loads', 'load', 'Serializer')


def _dumps_defaults(value):
    if isinstance(value, Serializable):
        return {k: _dumps_defaults(v) for k, v in value.repr().items()}
    elif isinstance(value, Mapping):
        return dict(value)
    elif type(value) == set or type(value) == frozenset:
        return list(value)
    elif type(value) == SimpleNamespace:
        return value.__dict__
    elif isinstance(value, Enum):
        return value.value
    elif type(value) is bytes:
        return '[BYTES]'
    else:
        return value


def dumps(
    value,
    *args,
    uuid_mode=rj.UM_CANONICAL,
    datetime_mode=rj.DM_ISO8601,
    ensure_ascii=False,
    number_mode=rj.NM_DECIMAL,
    allow_nan=False,
    default=_dumps_defaults,
    **kws,
):
    """Use `dumps`, but with useful default serialization settings."""
    return rj.dumps(
        value,
        *args,
        uuid_mode=uuid_mode,
        ensure_ascii=ensure_ascii,
        datetime_mode=datetime_mode,
        number_mode=number_mode,
        allow_nan=allow_nan,
        default=default,
        **kws,
    )


def dumps_bytes(
    value,
    *args,
    uuid_mode=rj.UM_CANONICAL,
    datetime_mode=rj.DM_ISO8601,
    ensure_ascii=False,
    number_mode=rj.NM_DECIMAL,
    allow_nan=False,
    default=_dumps_defaults,
    **kws,
):
    """Use `dumps`, but with useful default serialization settings."""
    return rj.dumps(
        value,
        *args,
        uuid_mode=uuid_mode,
        ensure_ascii=ensure_ascii,
        datetime_mode=datetime_mode,
        number_mode=number_mode,
        allow_nan=allow_nan,
        default=default,
        **kws,
    ).encode('utf-8')


def loads(
    value,
    *args,
    uuid_mode=rj.UM_CANONICAL,
    datetime_mode=rj.DM_ISO8601,
    number_mode=rj.NM_DECIMAL,
    allow_nan=False,
    **kws,
):
    """Use `loads`, but with useful default serialization settings."""
    return rj.loads(
        value,
        *args,
        uuid_mode=uuid_mode,
        datetime_mode=datetime_mode,
        number_mode=number_mode,
        allow_nan=allow_nan,
        **kws,
    )


def load(
    *args, uuid_mode=rj.UM_CANONICAL, datetime_mode=rj.DM_ISO8601, number_mode=rj.NM_DECIMAL, allow_nan=False, **kws
):
    """Use `load`, but with useful default serialization settings."""
    return rj.load(
        *args, uuid_mode=uuid_mode, datetime_mode=datetime_mode, number_mode=number_mode, allow_nan=allow_nan, **kws
    )


class Serializer(SerializerInterface):
    """Base serializer class."""

    mime_type = MimeTypes.json
    default = _dumps_defaults

    @classmethod
    def dumps(
        cls,
        *args,
        uuid_mode=rj.UM_CANONICAL,
        datetime_mode=rj.DM_ISO8601,
        ensure_ascii=False,
        number_mode=rj.NM_DECIMAL,
        allow_nan=False,
        default=_dumps_defaults,
        **kws,
    ):
        return rj.dumps(
            *args,
            uuid_mode=uuid_mode,
            ensure_ascii=ensure_ascii,
            datetime_mode=datetime_mode,
            number_mode=number_mode,
            allow_nan=allow_nan,
            default=cls.default,
            **kws,
        )

    @classmethod
    def dumps_bytes(
        cls,
        value,
        *args,
        uuid_mode=rj.UM_CANONICAL,
        datetime_mode=rj.DM_ISO8601,
        ensure_ascii=False,
        number_mode=rj.NM_DECIMAL,
        allow_nan=False,
        default=_dumps_defaults,
        **kws,
    ):
        """Use `dumps`, but with useful default serialization settings."""
        return rj.dumps(
            value,
            *args,
            uuid_mode=uuid_mode,
            ensure_ascii=ensure_ascii,
            datetime_mode=datetime_mode,
            number_mode=number_mode,
            allow_nan=allow_nan,
            default=cls.default,
            **kws,
        ).encode('utf-8')

    @classmethod
    def loads(
        cls,
        *args,
        uuid_mode=rj.UM_CANONICAL,
        datetime_mode=rj.DM_ISO8601,
        number_mode=rj.NM_DECIMAL,
        allow_nan=False,
        **kws,
    ):
        return rj.loads(
            *args, uuid_mode=uuid_mode, datetime_mode=datetime_mode, number_mode=number_mode, allow_nan=allow_nan, **kws
        )
