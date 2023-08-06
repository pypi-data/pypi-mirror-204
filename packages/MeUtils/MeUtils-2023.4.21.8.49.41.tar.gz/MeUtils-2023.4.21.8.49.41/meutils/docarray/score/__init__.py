from meutils.docarray.score.data import NamedScoreData
from meutils.docarray.score.mixins import AllMixins
from meutils.docarray.base import BaseDCType


class NamedScore(AllMixins, BaseDCType):
    _data_class = NamedScoreData
    _post_init_fields = ()
