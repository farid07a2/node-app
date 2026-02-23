from NodeEditorNewCode.N_node_graphics_socket import QDMGraphicsSocket
from NodeEditorNewCode.N_node_serializable import Serializable

LEFT_TOP=1
LEFT_BOTTOM=2
RIGHT_TOP=3
RIGHT_BOTTOM=4

DEBUG = False

class Socket(Serializable):
    def __init__(self,node,index=0,position=LEFT_TOP,socket_type=None,multi_edges = True ):
        super().__init__()
        self.node=node
        self.index=index
        self.position=position

        self.socket_type=socket_type
        self.is_multi_edges=multi_edges

        if DEBUG: print("socket== creating with :", self.index, self.position, "for node : ", self.node)
        self.grSocket=QDMGraphicsSocket(self,self.socket_type)
        self.grSocket.setPos(*self.node.getSocketPosition(index,position))
        # before Multiple Edge
        # self.edge=None
        self.edges=[]


    def __str__(self):
        return "<Socket %s %s..%s>" % ("ME" if self.is_multi_edges else "SE", hex(id(self))[2:5], hex(id(self))[-3:])

    def getSocketPosition(self):
        # print("GSP: ",self.index,self.position," Node: ",self.node)
        res = self.node.getSocketPosition(index=self.index,position=self.position)
        # print(" res :",res)
        return res

    # def setConnectedEdge(self, edge=None):
    def addEdge(self, edge):
        self.edges.append(edge)


    def removeEdge(self,edge):
        if edge in self.edges: self.edges.remove(edge)
        else: print("!W:","Socket :: removeEdge"," Wanna remove edge:",edge,"from self.edges but it's not in the list!")

    def removeAllEdges(self):
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()
        # or
        # self.edges.clear()

    # def hasEdge(self):
    #     return self.edge is not None


    def serialize(self):
        return {
            'id':self.id,
            'index':self.index,
            'multi_edges':self.is_multi_edges,
            'position':self.position,
            'socket_type':self.socket_type
        }


    def deserialize(self,data,hashmap={},restore_id=True):
        print('deserialization data',data)
        if restore_id:
            self.id = data['id']

        # self.is_multi_edges = data['multi_edges']
        self.is_multi_edges = self.determineMultiEdges(data)
        hashmap[data['id']] = self

        return False

    def determineMultiEdges(self,data):
        if 'multi_edges' in data:
            return data['multi_edges']
        else:
            # probably older version of file, make right socket multiedged by default
            return data['position'] in (RIGHT_BOTTOM,RIGHT_TOP)
