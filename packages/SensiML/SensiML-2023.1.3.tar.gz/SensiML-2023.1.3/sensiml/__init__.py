from sensiml.client import Client
from sensiml.client import Client as SensiML
from sensiml.client import __version__

__all__ = ["SensiML", "Client"]


try:
    from IPython.core.display import HTML

    display(HTML("<style>.container { width:90% !important; }</style>"))
except:
    pass

name = "sensiml"
