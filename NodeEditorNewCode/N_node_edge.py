from NodeEditorNewCode.N_node_graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier
from NodeEditorNewCode.N_node_graphics_node import QDMGraphicsNode
# from NodeEditorNewCode.N_node_scene import Scene
from NodeEditorNewCode.N_node_serializable import Serializable

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False
class Edge(Serializable):
    def __init__(self, scene, start_socket=None, end_socket=None, type_edge=EDGE_TYPE_DIRECT):
        super().__init__()

        self.scene = scene

        # Default init
        self._start_socket = None
        self._end_socket = None

        # Edge knows:
        # Where it begins
        self.start_socket = start_socket
        # Where it ends
        self.end_socket = end_socket

        # this method setter for set type edge in this method make update position
        self.edge_type = type_edge
        """ Now:
        Socket knows Edge
        Edge knows Socket
        This later allows:
        Deleting Edge from Socket
        Updating Edge when moving Node"""

        # self.start_socket.edge=self
        # if self.end_socket is not None:
        #     self.end_socket.edge=self

        # self.grEdge=QDMGraphicsEdgeDirect(self) if type_edge == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)
        # self.updatePositions()

        if DEBUG:
            print("Edge: ",self.grEdge.posSource," to ",self.grEdge.posDestination)
        # self.scene.grScene.addItem(self.grEdge)

        self.scene.addEdge(self)


    def __str__(self):
        # return  "<Node %s>"+(hex(id(self)))
        return "<Edge %s....%s>" % ((hex(id(self)))[2:5] , hex(id(self))[-3:])

    @property
    def start_socket(self): return self._start_socket

    @start_socket.setter
    def start_socket(self,value):
        # if we were assigned to some socket before, delete us from the socket
        if self._start_socket is not None:
            self._start_socket.removeEdge(self)

        # assign new start socket
        self._start_socket = value
        # addEdge to the socket class
        if self.start_socket is not None:
            # self.start_socket.edge = self
            self.start_socket.addEdge(self)

    @property
    def end_socket(self):
        return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._end_socket is not None:
            self._end_socket.removeEdge(self)

        # assign new end socket
        self._end_socket = value
        # addEdge to the socket class
        if self.end_socket is not None:
            # self.end_socket.edge = self
            self.end_socket.addEdge(self)

    @property
    def edge_type(self):
        return self._edge_type

    @edge_type.setter
    def edge_type(self,value):
        if hasattr(self,'grEdge') and self.grEdge is not None:
            self.scene.grScene.removeItem(self.grEdge)

        self._edge_type=value
        if self.edge_type == EDGE_TYPE_DIRECT:
            self.grEdge = QDMGraphicsEdgeDirect(self)
        elif self.edge_type == EDGE_TYPE_BEZIER:
            self.grEdge = QDMGraphicsEdgeBezier(self)
        else:
            self.grEdge = QDMGraphicsEdgeBezier(self)

        self.scene.grScene.addItem(self.grEdge)
        if self.start_socket is not None:
            self.updatePositions()


    def updatePositions(self):
        """
        socket.getSocketPosition()
        here get coordinate from node by grNode with width and height
        x =  0 if position in (LEFT_TOP,LEFT_BOTTOM) else self.grNode.width
        if position in (LEFT_BOTTOM,RIGHT_BOTTOM):
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing
        """
        source_pos = self.start_socket.getSocketPosition()
        if DEBUG:
            print("Node X: ",self.start_socket.node.grNode.pos().x())
            print("Node Y: ", self.start_socket.node.grNode.pos().y())

            print("start_socket:X",source_pos[0]," in grNode")
            print("start_socket: Y", source_pos[1]," in grNode")

        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        # print("start_socket:X ", source_pos[0]," in scene")
        # print("start_socket: Y", source_pos[1]," in scene")


        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()

            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)

        # self.grEdge.setSource(*self.start_socket.getSocketPosition())
        #
        # if self.end_socket is not None:
        #     self.grEdge.setDestination(*self.end_socket.getSocketPosition())
        #
        if DEBUG:
            print("SS: ",self.start_socket)
        if DEBUG:
            print("ES :",self.end_socket)
        self.grEdge.update()


    def remove_from_socket(self):
        # TODO:Fix Me!!
        # if self.start_socket is not None:
        #     # self.start_socket.edge=None
        #     # self.start_socket.addEdge(None)
        #     self.start_socket.removeEdge(None)
        # if self.end_socket is not None:
        #     # self.end_socket.edge=None
        #     # self.end_socket.addEdge(None)
        #     self.end_socket.removeEdge(None)
        self.end_socket=None
        self.start_socket=None

    def remove(self):
        if DEBUG: print("# Removing Edge")
        if DEBUG: print(" - remove edge from all sockets")
        self.remove_from_socket()
        if DEBUG: print(" - remove grEdge")
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge=None
        if DEBUG: print("Remove edge from scene")
        try:
            self.scene.removeEdge(self)
        except ValueError :
            pass
        # except Exception as e:
        #     print("EXCEPTION:",e,type(e))
        if DEBUG: print(" -- everything is done")

    def serialize(self):
        return {
            'id':self.id,
            'edge_type':self.edge_type,
            'start':self.start_socket.id,
            'end':self.end_socket.id,

        }


    def deserialize(self,data,hashmap={},restore_id=True):
        print('deserialization data',data)
        if restore_id:
            self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type'] # this setter for create edge (Bezier or direct and update)
        return False