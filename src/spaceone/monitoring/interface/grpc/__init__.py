from spaceone.core.pygrpc.server import GRPCServer
from .event import Event
from .webhook import Webhook

_all_ = ['app']

app = GRPCServer()
app.add_service(Event)
app.add_service(Webhook)

