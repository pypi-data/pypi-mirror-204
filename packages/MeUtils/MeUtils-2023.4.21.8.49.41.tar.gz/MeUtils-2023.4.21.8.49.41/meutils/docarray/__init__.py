__version__ = '0.21.0'

import os

from meutils.docarray.document import Document
from meutils.docarray.array import DocumentArray
from meutils.docarray.dataclasses import dataclass, field
from meutils.docarray.helper import login, logout

if 'DA_RICH_HANDLER' in os.environ:
    from rich.traceback import install

    install()
