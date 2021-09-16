""" Sample solutions for first lab on graphs.

    Implements the graph as a map of (vertex,edge-map) pairs.
"""

class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, element, coordinates):
        """ Create a vertex, with a data element.

        Args:
            element - the data or label to be associated with the vertex
            coordinates - tuple containing latitude and longitude
        """
        self._element = element
        self._coordinates = coordinates


    def __str__(self):
        """ Return a string representation of the vertex. """
        return f"{self._element}, {self._coordinates[0]}, {self._coordinates[1]}"

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()

    def latitude(self):
        """Return latitude of vertex"""
        return self._coordinates[0]

    def longitude(self):
        """Return longitude of vertex"""
        return self._coordinates[1]

    def coordinates(self):
        """Return coordinates of vertex"""
        return self._coordinates

    def element(self):
        """ Return the data for the vertex. """
        return self._element


class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class RouteMap:
    """ Represent a simple graph.

    This version maintains only undirected graphs, and assumes no
    self loops.

    Implements the Adjacency Map style. Also maintains a top level
    dictionary of vertices.

    It also implements a method that reads input data for street
    maps. Dijkstra's algorithm is also built in as a method
    """

    # Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the sets of edges for the corresponding vertex.
    #    Each edge set is also maintained as a dictionary,
    #    with the opposite vertex as the key and the edge object as the value.

    def __init__(self, file):
        """ Create an initial empty graph., and a reference dictionary
         to speed up finding vertices by their labels.

         Additionally, store the name of the file that was given by the
         user, and run the graphreader function which adds the graph
         from the text file into the structure"""
        self._structure = dict()
        self._reference = dict()
        self._file = file
        self.graphreader()

    def __str__(self):
        """ Return a string representation of the graph, if the graph has
         less than 100 vertices and edges"""
        if self.num_vertices() < 100:
            if self.num_edges() < 100:
                hstr = ('|V| = ' + str(self.num_vertices())
                        + '; |E| = ' + str(self.num_edges()))
                vstr = '\nVertices: '
                for v in self._structure:
                    vstr += str(v) + '-'
                edges = self.edges()
                estr = '\nEdges: '
                for e in edges:
                    estr += str(e) + ' '
                return hstr + vstr + estr
        return None
    # -----------------------------------------------------------------------#

    # ADT methods to query the graph

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])  # the dict of edges for v
        return num // 2  # divide by 2, since each edege appears in the
        # vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        if element in self._reference:
            return self._reference[element]
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v - a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

        Args:
            v - a vertex object
            w - a vertex object
        """
        if (self._structure is not None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.

        Args:
            v - a vertex object
        """
        return len(self._structure[v])

    # ----------------------------------------------------------------------#

    # ADT methods to modify the graph

    def add_vertex(self, element, coordinates):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.

        Additionally, make a reference to the vertex by its label
        in the reference dictionary
        """
        v = Vertex(element, coordinates)
        self._structure[v] = dict()
        self._reference[element] = v
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.

        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements.

        Args:
            elist - a list of pairs of vertex objects
        """
        for (v, w) in elist:
            self.add_edge(v, w, None)

    # ---------------------------------------------------------------------#

    # Additional methods to explore the graph

    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv


    def Dijkstra(self,s):
        """Find all the shortest paths to each vertex from the vertex s"""
        # The following is pretty much the exact same as pseudocode in lecture 14, thus no comments
        open = APQ()
        locs = {}
        closed = {}
        preds = {}
        preds[s] = None

        elt = open.add(0, s)
        locs[s] = elt
        while open.length() > 0:
            v = open.remove_min()
            locs.pop(v._value)
            predecessor = preds.pop(v._value)
            closed[v._value] = v._key, predecessor
            edges_incident = self.get_edges(v._value)
            for e in edges_incident:
                w = e.opposite(v._value)
                if w not in closed:
                    newcost = v._key + e._element
                    if w not in locs:
                        preds[w] = v
                        new_elt = open.add(newcost, w)
                        locs[w] = new_elt
                    elif newcost < open.get_key_by_value(w):
                        w_elt = open.get_element_by_value(w)
                        preds[w] = v
                        open.update_key(w_elt, newcost)

        return closed

    def sp(self, v, w):
        """Given a start vertex v, and an end vertex v, find the shortest path from
        v to w. Returns it as a list"""
        all_paths = self.Dijkstra(v)
        w_path = all_paths[w]   # get path from w to v
        current_vertex = w      # store w as current vertex
        my_list = []
        while w_path != None: # while the value isn't none
            vertex_element = str(current_vertex._element)
            if len(str(vertex_element)) < 7:    # if element is < 7 chars, add extra tab to fix output format
                vertex_element += "\t"
            # **NOTE commas are added in next line because GPS visualiser didn't work for me with just tabs.
            my_list.append(f"W,\t{current_vertex.latitude()},\t{current_vertex.longitude()},\t{vertex_element},\t{w_path[0]}")
            # If the predecessor isn't None (i.e. if current value is not the last value in path)
            if w_path[1] != None:
                current_vertex = w_path[1]._value   # set current vertex as predecessor
                w_path = all_paths[w_path[1]._value]    # set the new path as path from v to predecessor of w
            else:
                break
        # Next piece of code reverses list
        newlist = []
        i = len(my_list) - 1
        while i > -1:
            newlist.append(my_list[i])
            i -= 1
        my_list = []
        return newlist


    def printvlist(self, my_list):
        """Print a list of vertices in the format stated below"""
        print("type,\tlatitude,\tlongitude,\telement,\tcost\n")
        for i in my_list:
            print(i)

    def graphreader(self):
        """ Read and return the route map in filename. """
        file = open(self._file, 'r')
        entry = file.readline()  # either 'Node' or 'Edge'
        num = 0
        while entry == 'Node\n':
            num += 1
            nodeid = int(file.readline().split()[1])
            gps_line = file.readline()
            c1 = float(gps_line.split()[1])
            c2 = float(gps_line.split()[2])  # Read coordinates
            vertex = self.add_vertex(nodeid, (c1, c2))
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'vertices and added into the graph')
        num = 0
        while entry == 'Edge\n':
            num += 1
            source = int(file.readline().split()[1])
            sv = self.get_vertex_by_label(source)
            target = int(file.readline().split()[1])
            tv = self.get_vertex_by_label(target)
            file.readline()  # read the length data
            time = float(file.readline().split()[1])
            edge = self.add_edge(sv, tv, time)
            file.readline()  # read the one-way data
            entry = file.readline()  # either 'Node' or 'Edge'
        print('Read', num, 'edges and added into the graph')

    # End of class definition


class Element:
    """Creates individual element for the APQ"""
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __eq__(self, other):
        if other != None:
            return self._key == other._key
        else:
            return False

    def __lt__(self, other):
        return self._key < other._key

    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None

    def __str__(self):
        return f"{self._key} = key, {self._value} = value, {self._index} = index"


class APQ:
    """Creates an Adaptable Priority Queue"""

    def __init__(self):
        self.queue = []


    def add(self,key,item):
        """Add given key and item to the APQ"""
        e = Element(key, item, self.length())
        self.queue.append(e)
        self.bubble_up(e._index)
        return e

    def min(self):
        """Return the minimum key its value in the APQ"""
        return self.queue[0]._value, self.queue[0]._key

    def remove_min(self):
        """Remove the minimum element from the APQ"""
        if self.length() > 1: # If there are at least 2 elts in APQ, swap first with last, pop last, bubble down first
            self.queue[0], self.queue[self.length() - 1] = self.queue[self.length() - 1], self.queue[0]
            self.queue[0]._index = 0
            self.queue[self.length() - 1]._index = self.length() - 1
            removed_elt = self.queue.pop(self.length() - 1)
            self.bubble_down(0)
            return removed_elt
        elif self.length() == 1: # if only one elt in APQ, dont bother bubbling, just remove it
            removed_elt = self.queue.pop(0)
            return removed_elt
        else:   # otherwise do nothing as APQ is empty
            return None

    def length(self):
        """Return the length of the APQ"""
        return len(self.queue)

    def update_key(self, element, newkey):
        """Update the key of a specific element, then fix its position in APQ"""
        element._key = newkey
        if element._index != 0:  # If element is not first element, check if it should bubble up or down
            if self.queue[self.get_parent(element._index)]._key > self.queue[element._index]._key:
                self.bubble_up(element._index)
            elif self.get_rchild(element._index) < self.length():
                if self.queue[self.get_rchild(element._index)]._key < self.queue[element._index]._key:
                    self.bubble_down(element._index)
            elif self.get_lchild(element._index) < self.length():
                if self.queue[self.get_lchild(element._index)]._key < self.queue[element._index]._key:
                    self.bubble_down(element._index)
        else:   # if element is the first element, check whether it bubbles down to left or right child
            if self.get_rchild(element._index) < self.length():
                if self.queue[self.get_rchild(element._index)]._key < self.queue[element._index]._key:
                    self.bubble_down(element._index)
            elif self.get_lchild(element._index) < self.length():
                if self.queue[self.get_lchild(element._index)]._key < self.queue[element._index]._key:
                    self.bubble_down(element._index)
        return element


    def get_parent(self, index):
        """Return parent of given index"""
        return (index-1) // 2

    def get_lchild(self, index):
        """Return left child of given index"""
        return (index*2) + 1

    def get_rchild(self, index):
        """Return right child of given index"""
        return (index*2) + 2

    def get_key(self, element):
        """Get key by element"""
        return element._key

    def get_element_by_value(self, value):
        """Get the element object by value"""
        for i in self.queue:
            if i._value == value:
                return i
        return None

    def get_key_by_value(self, value):
        """Get the key of an element by its balue"""
        for i in self.queue:
            if i._value == value:
                return i._key
        return None

    def remove(self, element):
        """Remove element from APQ by element reference"""
        if element._index == 0:  # If elt is in first index, use remove_min code
            ret_elt = self.remove_min()
            return ret_elt
        else:  # Otherwise, swap with last elt and pop, Since last elt has to be biggest, it will always use bubble down
            self.queue[element._index], self.queue[self.length() - 1] =  self.queue[self.length() - 1], self.queue[element._index]
            self.queue[element._index]._index = element._index
            self.bubble_down(element._index)
            removed_elt = self.queue.pop(self.length() - 1)
            return removed_elt

    def bubble_up(self, index):
        """Helper function to maintain position in APQ. Bubbles up
        the element to its correct place in the binary heap"""
        # while parent > child and current elt isn't first elt, bubble up current elt
        while index > 0 and self.queue[index]._key < self.queue[self.get_parent(index)]._key:
            self.queue[self.get_parent(index)]._index = index
            self.queue[index], self.queue[self.get_parent(index)] = self.queue[self.get_parent(index)], self.queue[index]
            index = self.get_parent(index)
            self.queue[index]._index = index

    def bubble_down(self, index):
        """Helper function to maintain position in APQ. Bubbles down
        the element to its correct place in the binary heap"""
        # While there is a left child (if there's a child, there will always be a left child, not always right)
        while self.get_lchild(index) < self.length():
            min_val = self.get_lchild(index)
            # If there is a right child (doesn't fall off list index)
            if self.get_rchild(index) < self.length():
                # Compare keys, set the smaller one as minimum value
                if self.queue[self.get_rchild(index)]._key < self.queue[self.get_lchild(index)]._key:
                    min_val = self.get_rchild(index)
            # If current key > minimum child, swap them around
            if self.queue[index]._key > self.queue[min_val]._key:
                self.queue[min_val]._index = index
                self.queue[index], self.queue[min_val] = self.queue[min_val], self.queue[index]
                index = min_val
                self.queue[index]._index = index
            else:
                break

    def __str__(self):
        mystr = ""
        for i in self.queue:
            mystr += f"{i._key}, {i._value}, {i._index} \n"
            mystr += "1 \n"
        return mystr



routemap = RouteMap('corkCityData.txt')

ids = {}

ids['wgb'] = 1669466540

ids['turnerscross'] = 348809726

ids['neptune'] = 1147697924

ids['cuh'] = 860206013

ids['oldoak'] = 358357

ids['gaol'] = 3777201945

ids['mahonpoint'] = 330068634

sourcestr = 'wgb'

deststr='mahonpoint'

source = routemap.get_vertex_by_label(ids[sourcestr])

dest = routemap.get_vertex_by_label(ids[deststr])

tree = routemap.sp(source,dest)

routemap.printvlist(tree)

