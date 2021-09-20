class Track:

    def __init__(self, name, artiste, timesplayed):
        if type(name) != str:
            print("The name must be a string!")
        else:
            self.name = name
        if type(artiste) != str:
            print("The artiste must be a string!")
        else:
            self.artiste = artiste
        if type(timesplayed) != int or timesplayed < 0:
            print("Times played must be a positive integer or 0")
        else:
            self.timesplayed = timesplayed

    def get_name(self):
        return self.name

    def get_artiste(self):
        return self.artiste

    def play(self):
        self.timesplayed += 1
        return self

    def __str__(self):
        return ("%s, %s, %d" % (self.name, self.artiste, self.timesplayed))


class DLLNode:
    def __init__(self, prevnode, item, nextnode):
        self.item = item
        self.nextnode = nextnode
        self.prevnode = prevnode



class PyToonz:
    def __init__(self):
        self.head = DLLNode(None, None, None)
        self.tail = DLLNode(self.head, None, None)
        self.head.nextnode = self.tail
        self.size = 0
        self.first = None
        self.last = None
        self.current = None

    def length(self):
        return self.size

    def add_track(self, track):
        if self.size == 0:
            new_node = DLLNode(self.head, track, self.tail)
            self.first = new_node
            self.current = new_node
        else:
            old_last = self.last
            new_node = DLLNode(self.last, track, self.tail)
            old_last.nextnode = new_node
        self.tail.prevnode = new_node
        self.last = new_node
        self.size += 1

    def get_current(self):
        return self.current.item.__str__()

    def add_after(self, track):
        if self.current == None:
            return "There are no tracks in the list!"
        else:
            if self.current != self.last:
                next = self.current.nextnode
                new_node = DLLNode(self.current, track, next)
                next.prevnode = new_node
                self.current.nextnode = new_node
                self.size += 1

            else:
                old_last = self.last
                new_node = DLLNode(self.last, track, self.tail)
                old_last.nextnode = new_node
                self.tail.prevnode = new_node
                self.last = new_node
                self.size += 1


    def next_track(self):
        if self.current == self.last:
            self.current = self.first

        else:
            self.current = self.current.nextnode

    def prev_track(self):
        if self.current == self.first:
            self.current = self.last

        else:
            self.current = self.current.prevnode

    def reset(self):
        if self.current != None:
            self.current = self.first

    def play(self):
        return self.current.item.play()

    def remove_current(self):
        if self.current:
            prev = self.current.prevnode
            next = self.current.nextnode
            prev.nextnode = next
            next.prevnode = prev
            del self.current
            if next != self.tail:
                self.current = next
            else:
                self.current = prev
        else:
            return "The list is empty, removing was unsuccessful"

    def __str__(self):
        if self.size == 0:
            return "The list is empty!"
        temp_current = self.first
        empty_str = "Playlist: \n"
        while temp_current != self.tail:
            if temp_current == self.current:
                empty_str += "--> "
            empty_str += temp_current.item.__str__()
            empty_str += "\n"
            temp_current = temp_current.nextnode
        return empty_str












