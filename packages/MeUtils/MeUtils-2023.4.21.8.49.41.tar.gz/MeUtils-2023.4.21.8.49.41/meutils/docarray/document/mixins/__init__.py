from meutils.docarray.document.mixins.attribute import GetAttributesMixin
from meutils.docarray.document.mixins.audio import AudioDataMixin
from meutils.docarray.document.mixins.blob import BlobDataMixin
from meutils.docarray.document.mixins.content import ContentPropertyMixin
from meutils.docarray.document.mixins.convert import ConvertMixin
from meutils.docarray.document.mixins.dump import UriFileMixin
from meutils.docarray.document.mixins.featurehash import FeatureHashMixin
from meutils.docarray.document.mixins.image import ImageDataMixin
from meutils.docarray.document.mixins.mesh import MeshDataMixin
from meutils.docarray.document.mixins.multimodal import MultiModalMixin
from meutils.docarray.document.mixins.plot import PlotMixin
from meutils.docarray.document.mixins.porting import PortingMixin
from meutils.docarray.document.mixins.property import PropertyMixin
from meutils.docarray.document.mixins.protobuf import ProtobufMixin
from meutils.docarray.document.mixins.pydantic import PydanticMixin
from meutils.docarray.document.mixins.strawberry import StrawberryMixin
from meutils.docarray.document.mixins.sugar import SingletonSugarMixin
from meutils.docarray.document.mixins.text import TextDataMixin
from meutils.docarray.document.mixins.video import VideoDataMixin


class AllMixins(
    ProtobufMixin,
    PydanticMixin,
    StrawberryMixin,
    PropertyMixin,
    ContentPropertyMixin,
    ConvertMixin,
    AudioDataMixin,
    ImageDataMixin,
    TextDataMixin,
    MeshDataMixin,
    VideoDataMixin,
    BlobDataMixin,
    PlotMixin,
    UriFileMixin,
    SingletonSugarMixin,
    PortingMixin,
    FeatureHashMixin,
    GetAttributesMixin,
    MultiModalMixin,
):
    """All plugins that can be used in :class:`Document`."""

    ...
