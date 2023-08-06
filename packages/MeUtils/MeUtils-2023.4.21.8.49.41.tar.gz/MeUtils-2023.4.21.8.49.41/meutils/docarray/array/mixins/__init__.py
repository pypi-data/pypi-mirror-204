from abc import ABC

from meutils.docarray.array.mixins.content import ContentPropertyMixin
from meutils.docarray.array.mixins.delitem import DelItemMixin
from meutils.docarray.array.mixins.embed import EmbedMixin
from meutils.docarray.array.mixins.empty import EmptyMixin
from meutils.docarray.array.mixins.evaluation import EvaluationMixin
from meutils.docarray.array.mixins.find import FindMixin
from meutils.docarray.array.mixins.getattr import GetAttributeMixin
from meutils.docarray.array.mixins.getitem import GetItemMixin
from meutils.docarray.array.mixins.group import GroupMixin
from meutils.docarray.array.mixins.io.binary import BinaryIOMixin
from meutils.docarray.array.mixins.io.common import CommonIOMixin
from meutils.docarray.array.mixins.io.csv import CsvIOMixin
from meutils.docarray.array.mixins.io.dataframe import DataframeIOMixin
from meutils.docarray.array.mixins.io.from_gen import FromGeneratorMixin
from meutils.docarray.array.mixins.io.json import JsonIOMixin
from meutils.docarray.array.mixins.io.pushpull import PushPullMixin
from meutils.docarray.array.mixins.match import MatchMixin
from meutils.docarray.array.mixins.parallel import ParallelMixin
from meutils.docarray.array.mixins.plot import PlotMixin
from meutils.docarray.array.mixins.post import PostMixin
from meutils.docarray.array.mixins.pydantic import PydanticMixin
from meutils.docarray.array.mixins.reduce import ReduceMixin
from meutils.docarray.array.mixins.sample import SampleMixin
from meutils.docarray.array.mixins.setitem import SetItemMixin
from meutils.docarray.array.mixins.strawberry import StrawberryMixin
from meutils.docarray.array.mixins.text import TextToolsMixin
from meutils.docarray.array.mixins.traverse import TraverseMixin
from meutils.docarray.array.mixins.dataloader import DataLoaderMixin


class AllMixins(
    GetAttributeMixin,
    GetItemMixin,
    SetItemMixin,
    DelItemMixin,
    ContentPropertyMixin,
    PydanticMixin,
    StrawberryMixin,
    GroupMixin,
    EmptyMixin,
    CsvIOMixin,
    JsonIOMixin,
    BinaryIOMixin,
    CommonIOMixin,
    EmbedMixin,
    PushPullMixin,
    FromGeneratorMixin,
    FindMixin,
    MatchMixin,
    TraverseMixin,
    PlotMixin,
    SampleMixin,
    PostMixin,
    TextToolsMixin,
    EvaluationMixin,
    ReduceMixin,
    ParallelMixin,
    DataframeIOMixin,
    DataLoaderMixin,
    ABC,
):
    """All plugins that can be used in :class:`DocumentArray`."""

    ...
