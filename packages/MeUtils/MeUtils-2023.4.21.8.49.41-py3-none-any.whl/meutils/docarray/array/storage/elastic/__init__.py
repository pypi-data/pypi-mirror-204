from abc import ABC

from meutils.docarray.array.storage.elastic.backend import BackendMixin, ElasticConfig
from meutils.docarray.array.storage.elastic.find import FindMixin
from meutils.docarray.array.storage.elastic.getsetdel import GetSetDelMixin
from meutils.docarray.array.storage.elastic.seqlike import SequenceLikeMixin

__all__ = ['StorageMixins', 'ElasticConfig']


class StorageMixins(FindMixin, BackendMixin, GetSetDelMixin, SequenceLikeMixin, ABC):
    ...
