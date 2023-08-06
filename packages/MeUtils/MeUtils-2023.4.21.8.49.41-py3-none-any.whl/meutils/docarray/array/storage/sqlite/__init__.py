from abc import ABC

from meutils.docarray.array.storage.sqlite.backend import BackendMixin, SqliteConfig
from meutils.docarray.array.storage.sqlite.getsetdel import GetSetDelMixin
from meutils.docarray.array.storage.sqlite.seqlike import SequenceLikeMixin
from meutils.docarray.array.storage.memory.find import (
    FindMixin,
)  # temporary delegate to in-memory find API

__all__ = ['StorageMixins', 'SqliteConfig']


class StorageMixins(FindMixin, BackendMixin, GetSetDelMixin, SequenceLikeMixin, ABC):
    ...
