import abc

__all__ = ['SerializerInterface', 'Serializable']


class Serializable(abc.ABC):
    """Class which supports serialization of its attributes."""

    serializable_attrs = None  #: Should be a frozenset or None. If None, then all will be used for serialization.
    include_null_values = True  #: include null values in a representation

    def __getitem__(self, item):
        return getattr(self, item, None)

    def repr(self) -> dict:
        """Must return a representation of object __init__ arguments."""
        _repr = {}
        if self.serializable_attrs is None:
            if self.__slots__:
                for slot in self.__slots__:
                    if not slot.startswith('_') and hasattr(self, slot):
                        v = getattr(self, slot)
                        if not self.include_null_values and v is None:
                            continue
                        if isinstance(v, Serializable):
                            _repr[slot] = v.repr()
                        else:
                            _repr[slot] = v
            else:
                for k, v in self.__dict__.items():
                    if not self.include_null_values and v is None:
                        continue
                    if not k.startswith('_'):
                        if isinstance(v, Serializable):
                            _repr[k] = v.repr()
                        else:
                            _repr[k] = v
        else:
            if self.__slots__:
                for slot in self.__slots__:
                    if slot in self.serializable_attrs and hasattr(self, slot):
                        v = getattr(self, slot)
                        if not self.include_null_values and v is None:
                            continue
                        if isinstance(v, Serializable):
                            _repr[slot] = v.repr()
                        else:
                            _repr[slot] = v
            else:
                for k, v in self.__dict__.items():
                    if not self.include_null_values and v is None:
                        continue
                    if k in self.serializable_attrs:
                        if isinstance(v, Serializable):
                            _repr[k] = v.repr()
                        else:
                            _repr[k] = v

        return _repr

    def __repr__(self):
        return f'{self.__class__.__name__}(**{self.repr()})'


class SerializerInterface(abc.ABC):
    """Abstract serializer interface that should be used by clients/servers to process raw messages."""

    mime_type = None  # you should define an appropriate mime type here

    @classmethod
    @abc.abstractmethod
    def loads(cls, data, *args, **kws):
        pass

    @classmethod
    @abc.abstractmethod
    def dumps(cls, data, *args, **kws) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def dumps_bytes(cls, data, *args, **kws) -> bytes:
        pass
