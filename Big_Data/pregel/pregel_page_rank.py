from pregel import Pregel, Vertex
from models import Document, DocumentLink

max_iter = 100

class NewVertex(Vertex):
    def update(self):
        if self.superstep < max_iter:


