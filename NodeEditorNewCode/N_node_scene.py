import json
import os.path

from NodeEditorNewCode.N_node_edge import Edge
# from NodeEditorNewCode.N_node_edge import Edge
from NodeEditorNewCode.N_node_graphics_scene import QDMGraphicsScene
from NodeEditorNewCode.N_node_node import Node
from NodeEditorNewCode.N_node_scene_clipboard import SceneClipboard
from NodeEditorNewCode.N_node_serializable import Serializable
from NodeEditorNewCode.node_scene_history import SceneHistory
from NodeEditorNewCode.utils import dumpException


class InvalidFile(Exception):
    pass
DEBUG = False
class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes= []
        self.edges= []
        self.scene_width, self.scene_height = 64000, 64000

        self._last_selected_items = []
        self._has_been_modified =  False

        # initialise all listners
        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._item_deselected_listeners = []

        # here we can store callback for retriving the class for Nodes
        self.node_class_selector = None

        # self.scene_width, self.scene_height = 1000, 1000
        self.history=SceneHistory(self)
        self.clipboard = SceneClipboard(self)
        self.initUI()
        self.grScene.itemSelected.connect(self.onItemSelected)
        self.grScene.itemDeselected.connect(self.onItemDeselected)

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width,self.scene_height)

    def onItemSelected(self):
        if DEBUG:
            print("Scene :: - onSelectedItem")
            print("-- last:",self._last_selected_items)
            print(" -- Now: ",self.getSelectedItems())
        current_selected_items = self.getSelectedItems()
        if current_selected_items != self._last_selected_items:
            self._last_selected_items = current_selected_items
            self.history.storeHistory("Selection changed")
            for callback in self._item_selected_listeners:
                callback()

    def onItemDeselected(self):
        if DEBUG:
            print("Scene :: - onDeselectedItem")
            print("-- last:", self._last_selected_items)
            print(" -- Now: ", self.getSelectedItems())

        self.resetLastSelectedStates()
        if self._last_selected_items != [] :
            self._last_selected_items=[]
            self.history.storeHistory("Deselected Everything")
            for callback in self._item_deselected_listeners: callback()





    def isModified(self):
        return self.has_been_modified

    def getSelectedItems(self):
        return self.grScene.selectedItems()

    @property
    def has_been_modified(self):
        # return False
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self,value):
        if DEBUG:
            print("MODIFIED TRIGGERED")
            print("Called from:")
        # import traceback
        # traceback.print_tb()

        if not self._has_been_modified and value:
            # set it now, because we will be reading it soon
            self._has_been_modified=value

            # call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified=value

    # our helper listener functions
    def addHasBeenModifierdListeners(self,callback):
        self._has_been_modified_listeners.append(callback)

    def addItemSelectedListeners(self,callback):
        self._item_selected_listeners.append(callback)

    def addItemDeselectedListeners(self,callback):
        self._item_deselected_listeners.append(callback)

    def addDragEnterListener(self, callback):
        self.grScene.views()[0].addDragEnterListener(callback)

    def addDropListener(self, callback):
        self.grScene.views()[0].addDropListener(callback)

    # custom flag to detect node or edge has been selected
    def resetLastSelectedStates(self):
        for node in self.nodes:
            node.grNode._last_selected_state = False
        for edge in self.edges:
            edge.grEdge._last_selected_state =False


    def addNode(self,node):
        self.nodes.append(node)
        # # if node in self.nodes: self.nodes.remove(node)
        # if node in self.nodes:
        #     self.nodes.remove(node)
        # else: print("!W:","Sceen :: removeNode"," Wanna remove node:",node,"from self.nodes but it's not in the list!")



    def addEdge(self,edge):
        self.edges.append(edge)
        # if edge in self.edges: self.edges.remove(edge)
        # else: print("!W:","Scene :: removeEdge"," Wanna remove edge:",edge,"from self.edges but it's not in the list!")


    def removeNode(self,node):
        # self.nodes.remove(node)
        if node in self.nodes:
            self.nodes.remove(node)
        else:
            if DEBUG:print("!W:","Scene :: removeNode"," Wanna remove node:",node,"from self.nodes but it's not in the list!")


    def removeEdge(self,edge):
        # self.edges.remove(edge)
        if edge in self.edges: self.edges.remove(edge)
        else:
            if DEBUG:
                print("!W:","Scene :: removeEdge"," Wanna remove edge:",edge,"from self.edges but it's not in the list!")


    def clear(self):

        print(self.nodes)

        while len(self.nodes)>0:
            self.nodes[0].remove()

        self.has_been_modified =False


    def saveToFile(self,filename):
        with open(filename,"w") as file:
            file.write(json.dumps(self.serialize(),indent=4))
            self.has_been_modified =False
        if DEBUG:
            print('saving to ',filename,' was successfully.')

    def loadFromFile(self,filename):
        # with open(filename,"r") as file:
        #     raw_data = file.read()
        #     data = json.loads(raw_data,encodings='utf-8')
        #     self.deserialize(data)
        # with open(filename, "r", encoding="utf-8") as file:
        # with open(filename, "r") as file:
        #     raw_data = file.read()
        #     try:
        #             data = json.loads(raw_data)
        #             # data = json.load(file)
        #             self.deserialize(data)
        #             self.has_been_modified = False
        #     except json.JSONDecodeError:
        #         raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))

        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.deserialize(data)
                self.has_been_modified = False
        except json.JSONDecodeError as e:
            raise InvalidFile(
                f"{os.path.basename(filename)} is not valid JSON\n\n{e}"
            )
        except Exception as e: dumpException(e)

    def setNodeClassSelector(self,class_selecting_function):
        """ when the function self.node_class_selector is set, we can use different Node Classes"""
        self.node_class_selector = class_selecting_function


    def getNodeClassFromData(self,data):
        return Node if self.node_class_selector is None else self.node_class_selector(data)

    def serialize(self):
        nodes,edges=[],[]
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())

        return {
            'id':self.id,
            'scene_width':self.scene_width,
            'scene_height':self.scene_height,
            'nodes':nodes,
            'edges':edges

        }


    def deserialize(self,data,hashmap={}, restore_id=False):
        if DEBUG:
            print('deserialization data',data)
        self.clear()
        hashmap = {}
        if restore_id:
            self.id = data['id']

        # create nodes
        for node_data in data['nodes']:
            # Node(self).deserialize(node_data,hashmap,restore_id)
            self.getNodeClassFromData(node_data)(self).deserialize(node_data,hashmap,restore_id)

        # create edges
        for edge_data in data['edges']:
            # new_edge = Edge(self)
            Edge(self).deserialize(edge_data,hashmap)

        return True