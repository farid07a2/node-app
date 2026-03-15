from collections import OrderedDict
from tkinter.constants import CENTER

from NodeEditorNewCode.N_TestGrapghicItem import GraphicsTestItem
from NodeEditorNewCode.N_node_content_widget import QDMNodeContentWidget
from NodeEditorNewCode.N_node_graphics_node import QDMGraphicsNode
from NodeEditorNewCode.N_node_serializable import Serializable
from NodeEditorNewCode.N_node_socket import Socket, LEFT_TOP, RIGHT_TOP, LEFT_BOTTOM, RIGHT_BOTTOM, LEFT_CENTER, \
    RIGHT_CENTER
from NodeEditorNewCode.utils import dumpException

DEBUG = False

class Node(Serializable):

    def __init__(self,scene,title='Undefined Node',inputs=[],outputs=[]):
        super().__init__()
        self.scene=scene
        self._title=title

        self.initInnerClasses()
        self.initSettings()

        self.grtestItem=GraphicsTestItem()
        self.grtestItem.setPos(300, 300)
        self.grNode.title="test New Title"
        self.grNode.title = title
        self.scene.addNode(self) # add in list

        self.scene.grScene.addItem(self.grNode)
        self.scene.grScene.addItem(self.grtestItem)
        # self.scene.grScene.addRect(-100,-100,80,100,outerlinePen,greenBrush)
        # text = self.scene.grScene.addText("Hello for this text", QFont("Ubuntu"))
        # create Socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        self.initSockets(inputs,outputs)


    def initInnerClasses(self):
        self.content = QDMNodeContentWidget(self)
        self.grNode = QDMGraphicsNode(self)


    def initSettings(self):
        self.socket_spacing = 22
        self.input_socket_position = LEFT_BOTTOM
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = False
        self.output_multi_edged = True

    def initSockets(self,inputs,outputs,reset = True):
        if reset:
            # clear old sockets
            if hasattr(self,'inputs') and hasattr(self,'outputs'):
                for socket in (self.inputs + self.outputs):
                    self.scene.grScene.removeItem(socket.grSocket)
                self.inputs = []
                self.outputs = []

        # create new sockets
        counter = 0
        # use item for colors in table colors in grSocket
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item,
                            multi_edges=self.input_multi_edged,count_on_this_node_side=len(inputs),is_input=True)
            counter += 1
            self.inputs.append(socket)
        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_BOTTOM, socket_type=item,
                            multi_edges=self.output_multi_edged,count_on_this_node_side=len(outputs),is_input=False)
            counter += 1
            self.outputs.append(socket)


    def __str__(self):
        # return  "<Node %s>"+(hex(id(self)))
        return "<Node %s....%s>" % ((hex(id(self)))[2:5] , hex(id(self))[-3:])

    def updateConnectedEdges(self):
        if DEBUG:print(" Node :: Start updating")
        for socket in self.inputs + self.outputs:
            # if socket.hasEdge():
            if DEBUG:print("Socket for updating position when change Node",socket)

            for edge in socket.edges:
                if DEBUG:print('edge',edge,' for updating...')
                # socket.edge.updatePositions()
                edge.updatePositions()

            else:
                if DEBUG: print('Noop')

    def remove(self):
            if DEBUG:
                print("> removing Node",self)
            if DEBUG:
                print("> -- Remove all edges from sockets")

            print("Input Socket %s",self.inputs)
            print("Output Socket %s",self.outputs)

            for socket in (self.inputs+self.outputs):
                # if socket.hasEdge():
                for edge in socket.edges:
                    if DEBUG: print("    -removing from socket:",socket , "edge:",edge)
                    edge.remove()
            if DEBUG:
                print("> -- remove grNode")
            self.scene.grScene.removeItem(self.grNode)
            if DEBUG:
                print("> remove Node from the scene",self)
            self.scene.removeNode(self)
            if DEBUG:
                print("> everything was done ",self)


    @property
    def pos(self):
        return self.grNode.pos()   #QPointF

    def setPos(self,x,y):
        self.grNode.setPos(x,y)

    @property
    def title(self): return self._title

    @title.setter
    def title(self,title):
        self._title=title
        self.grNode.title=self._title


    def getSocketPositionRefacoredForCalcBaseNode(self,index,position):
        """ here return x , y for rectangle parent = node  that means x start with edge of Graphics node"""
        x =  0 if position in (LEFT_TOP,LEFT_BOTTOM) else self.grNode.width

        if position in (LEFT_BOTTOM,RIGHT_BOTTOM):
            # start from to bottom
            y = self.grNode.height - self.grNode.edge_roundness - self.grNode.title_horizontal_padding - index * self.socket_spacing
            if not DEBUG: print("self.grNode.height= ", self.grNode.height, " - ", " self.grNode.edge_size :", self.grNode.edge_roundness,
                      " - ",
                      "self.grNode._padding = ", self.grNode.title_horizontal_padding, " - ", "index", index, " * ",
                      " self.socket_spacing = ", self.socket_spacing,
                      "===", y)
        else:
            # start from the top
            y = self.grNode.title_height + self.grNode.title_horizontal_padding + self.grNode.edge_roundness + index * self.socket_spacing
            if DEBUG: print("self.grNode.height= ", self.grNode.height, " + ", " self.grNode._padding :", self.grNode.title_horizontal_padding,
                  " + ",
                  "self.grNode.edge_size = ", self.grNode.edge_roundness, " + ", "index", index, " * ",
                  " self.socket_spacing = ", self.socket_spacing,
                  "===", y)


        # y=index * 20

        # print("self.grNode.height= ",self.grNode.height," - "," self.grNode.edge_size :",self.grNode.edge_size," - ",
        #       "self.grNode._padding = ",self.grNode._padding," - ","index",index," * "," self.socket_spacing = ",self.socket_spacing,
        #       "===",y )

        if DEBUG:
            print("X in calculate x in Node Class x=",x)
            print("X in calculate x in Node Class y=", y)

        return [x,y]


    def getSocketPosition(self,index,position,num_out_of=1):
        """ here return x , y for rectangle parent = node  that means x start with edge of Graphics node"""
        x =  0 if position in (LEFT_TOP,LEFT_CENTER,LEFT_BOTTOM) else self.grNode.width

        if position in (LEFT_BOTTOM,RIGHT_BOTTOM):
            # start from to bottom
            y = self.grNode.height - self.grNode.edge_roundness - self.grNode.title_horizontal_padding - index * self.socket_spacing
            if not DEBUG: print("self.grNode.height= ", self.grNode.height, " - ", " self.grNode.edge_size :", self.grNode.edge_roundness,
                      " - ",
                      "self.grNode._padding = ", self.grNode.title_horizontal_padding, " - ", "index", index, " * ",
                      " self.socket_spacing = ", self.socket_spacing,
                      "===", y)
        elif position in (LEFT_CENTER,RIGHT_CENTER):
            num_socket = num_out_of
            node_height = self.grNode.height
            top_offSet = self.grNode.title_height + 2 * self.grNode.title_vertical_padding + self.grNode.edge_padding
            available_height = node_height-top_offSet
            total_height_off_all_socket = num_socket * self.socket_spacing
            new_top = available_height - total_height_off_all_socket

            # y=top_offSet + index * self.socket_spacing + new_top / 2
            y = top_offSet + available_height / 2.0 + (index -0.5) * self.socket_spacing
            if num_socket > 1:
                y-= self.socket_spacing * (num_socket-1)/2


        elif position in (LEFT_TOP,RIGHT_TOP):
            # start from the top
            # y = self.grNode.title_height + self.grNode.title_horizontal_padding + self.grNode.edge_roundness + index * self.socket_spacing
            y = self.grNode.title_height + self.grNode.title_vertical_padding + self.grNode.edge_roundness + index * self.socket_spacing
            if DEBUG: print("self.grNode.height= ", self.grNode.height, " + ", " self.grNode._padding :", self.grNode.title_horizontal_padding,
                  " + ",
                  "self.grNode.edge_size = ", self.grNode.edge_roundness, " + ", "index", index, " * ",
                  " self.socket_spacing = ", self.socket_spacing,
                  "===", y)
        else:
            y = 0

        # y=index * 20

        # print("self.grNode.height= ",self.grNode.height," - "," self.grNode.edge_size :",self.grNode.edge_size," - ",
        #       "self.grNode._padding = ",self.grNode._padding," - ","index",index," * "," self.socket_spacing = ",self.socket_spacing,
        #       "===",y )

        if DEBUG:
            print("X in calculate x in Node Class x=",x)
            print("X in calculate x in Node Class y=", y)


        return [x,y]

    def initInputsOutputs(self):
        self.inputs = []
        self.outputs = []

    def serialize(self):
        inputs,outputs=[],[]
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())

        # return {
        #     'id':self.id,
        #     'title':self.title,
        #     'pos_x':self.grNode.scenePos().x(),
        #     'pos_y':self.grNode.scenePos().y(),
        #     'inputs':inputs,
        #     'outputs':outputs,
        #     'content':self.content.serialize(),
        # }

        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.grNode.scenePos().x()),
            ('pos_y', self.grNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize()),
        ])

    def deserialize(self,data,hashmap={},restore_id=False):
        try:
            if DEBUG:
                print('deserialization data',data)
            if restore_id:
                self.id= data['id']

            hashmap[data['id']]=self
            self.setPos(data['pos_x'],data['pos_y'])
            self.title = data['title']
            data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
            data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
            num_inputs = len(data['inputs'])
            num_outputs = len(data['outputs'])

            self.inputs=[]
            for socket_data in data['inputs']:
                new_socket=Socket(node=self,index=socket_data['index'],position=socket_data['position'],
                                  socket_type=socket_data['socket_type'],count_on_this_node_side= num_inputs,is_input=True)

                new_socket.deserialize(socket_data,hashmap,restore_id)
                self.inputs.append(new_socket)

            self.outputs = []
            for socket_data in data['outputs']:
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                    socket_type=socket_data['socket_type'],count_on_this_node_side=num_outputs,is_input=False)
                new_socket.deserialize(socket_data, hashmap,restore_id)
                self.outputs.append(new_socket)

            if DEBUG:
                print(hashmap)


        except Exception as e: dumpException(e)

        # also deserialize the content of the node
        res = self.content.deserialize(data['content'],hashmap)

        return True & res