from collections import OrderedDict

from NodeEditorNewCode.N_node_edge import Edge
from NodeEditorNewCode.N_node_graphics_edge import QDMGraphicsEdge
from NodeEditorNewCode.N_node_node import Node

DEBUG =True

class SceneClipboard:
    def __init__(self,scene):
        self.scene=scene

    def serializeSelected(self,delete=True):
        if DEBUG: print("Copy to clipboard")
        sel = self.scene.grScene.selectedItems()
        sel_nodes,sel_edges,sel_sockets=[],[],{}

        # sort nodes and edges
        for item in self.scene.grScene.selectedItems():
            if hasattr(item,'node'):
                sel_nodes.append(item.node.serialize())
                for socket in (item.node.inputs + item.node.outputs):
                    sel_sockets[socket.id] = socket
            elif isinstance(item,QDMGraphicsEdge):
                sel_edges.append(item.edge)


        # debug
        if DEBUG :
            print(" Nodes\n   ",sel_nodes)
            print(" edges\n    ", sel_edges)
            print(" Sockets\n    ", sel_sockets)

        # remove all edges which are not connected to node in our list
        edge_to_remove=[]

        for edge in sel_edges:
            if edge.start_socket.id in sel_sockets and edge.end_socket.id in sel_sockets:
                if DEBUG: print("edge is ok ,connected with both sides")
                pass
            else:
                if DEBUG:print("edge",edge," is not connected with both sides")
                edge_to_remove.append(edge)

        for edge in edge_to_remove:
            sel_edges.remove(edge)

        # make final list of edges:
        edges_final= []
        for edge in sel_edges:
            edges_final.append(edge.serialize())


        data =  OrderedDict([('nodes',sel_nodes),
                             ('edges',edges_final)
                             ]
                            )

        # if cut (aka delete) remove selected items
        if delete:
            self.scene.grScene.views()[0].deleteSelected()
            # store our history
            self.scene.history.storeHistory("Cut out elements from scene",setModified=True)

        return data


    def deserializeFromClipboard(self,data):
        if DEBUG:print("deserialize from clipboard, data : ",data)
        hashmap={}

        # calculate mouse pointer - scene position
        view = self.scene.grScene.views()[0]
        mouse_scene_pos = view.last_scene_mouse_position

        # calculate selected objects hbox and centre
        minx,maxx,miny,maxy=0,0,0,0
        for node_data in data['nodes']:
            x,y = node_data['pos_x'],node_data['pos_y']
            if x<minx: minx=x
            if x>maxx: maxx=x

            if y<miny: miny = y
            if y>maxy: maxy = y

        bbox_centre_x = (minx+maxx)/2
        bbox_centre_y = (miny+maxy)/2

        centre = view.mapToScene(view.rect().center())
        # calculate the offset of the newly treatig node
        offset_x= mouse_scene_pos.x()- bbox_centre_x
        offset_y= mouse_scene_pos.y()- bbox_centre_y

        # create each node
        for node_data in data['nodes']:
            # new_node = Node(self.scene)
            new_node = self.scene.getNodeClassFromData(node_data)(self.scene)
            new_node.deserialize(node_data,hashmap,restore_id=False)

            # readjust the new node
            pos = new_node.pos
            new_node.setPos(pos.x()+offset_x,pos.y()+offset_y)

        # create each edge
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap,restore_id=False)

        # store history
        self.scene.history.storeHistory("Pasted elements in scene",setModified=True)
        #
