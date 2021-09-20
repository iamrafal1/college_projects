import random


class Block:
    """Class for each individual block of memory. Contains number of pages in block, ID of process, and
       size of block in KB"""
    def __init__(self, pages, pID = 0):
        self.pages = pages
        self.size = 4 * pages
        self.pID = pID

    def __str__(self):
        return f"{self.pages} pages, {self.size} KB, {self.pID} pID"


class ProcessRequest:
    """Class for each individual memory request made by processes. Contains id of the process and size
       required by the request in KB"""
    def __init__(self, pID, size):
        self.pID = pID
        self.size = size

    def __str__(self):
        return f"pID = {self.pID}, size = {self.size} KB"

class SLLNode:
    """Single linked list node -  helper class for Single linked list data type"""
    def __init__(self, item, nextnode):
        self.item = item
        self.nextnode = nextnode


class SLL:
    """Single linked list data structure for keeping track of free memory"""
    def __init__(self):
        self.head = SLLNode(None, None )
        self.tail = SLLNode(self.head, None)
        self.head.nextnode = self.tail
        self.size = 0
        self.first = None
        self.last = None
        self.current = None
        self.previous = self.head

    """Add node (in this case Block object) to the SLL"""
    def add_node(self, node):
        if self.size == 0:
            new_node = SLLNode(node, self.tail)
            self.first = new_node
            self.current = new_node
            self.head.nextnode = new_node
        else:
            old_last = self.last
            new_node = SLLNode(node, self.tail)
            old_last.nextnode = new_node
        self.last = new_node
        self.size += 1

    def get_current(self):
        """returns the currently selected next_node. Useful for my next fit implementation"""
        return self.current.item.__str__()

    def next_node(self):
        """Move the single linked list cursor to the next node (in order)"""
        if self.current == self.last:
            self.previous = self.current
            self.current = self.first

        else:
            self.previous = self.current
            self.current = self.current.nextnode

    def remove_current(self):
        """Remove the current node (node which is being indicated by the linked list cursor)"""
        if self.current:
            if self.size == 1:
                toRemove = self.current
                self.previous = self.head
                del self.current
                self.current = None
            else:
                toRemove = self.current
                next = self.current.nextnode
                prev = self.previous
                if prev != self.last:
                    prev.nextnode = next
                if self.current == self.first:
                    self.head.nextnode = next
                    self.first = next
                if self.current == self.last:
                    self.last = prev
                del self.current
                if next != self.tail:
                    self.current = next
                else:
                    self.current = self.first
            self.size -= 1
            return toRemove
        else:
            return None

    def __str__(self):
        if self.size == 0:
            return "The list is empty!"
        temp_current = self.first
        empty_str = "SLL: \n"
        while temp_current != self.tail:
            if temp_current == self.current:
                empty_str += "--> "
            empty_str += temp_current.item.__str__()
            empty_str += "\n"
            temp_current = temp_current.nextnode
        return empty_str


class Queue:
    """ADT for a Queue, used for page replacement (FIFO)"""
    def __init__(self):
        """Construct empty list that serves as queue"""
        self.queue = []

    def add(self, node):
        """Append process to end of queue"""
        self.queue.append(node)

    def queueLength(self):
        """Return length of queue"""
        return len(self.queue)

    def remove(self):
        """Remove the first item from the queue"""
        self.queue.pop(0)

    def removeReturn(self):
        """Removes first item from queue and returns it"""
        item = self.queue.pop(0)
        return item

    def removeIndex(self, index):
        """Removes item at index and returns it"""
        item = self.queue.pop(index)
        return item

    def checkLength(self):
        """Check amount of items in queue"""
        return len(self.queue)

    def __str__(self):
        empty_str = ""
        for i in self.queue:
             empty_str += i.item.__str__()
             empty_str += "\n"
        return empty_str


class MainMemory:
    """Core class where all other ADTs are implemented to create the main memory. Main memory consists of
       freeMemory - Single linked list with all free blocks of memory
       occupiedMemory - Dictionary of queues which stores all occupied blocks of memory. The keys in the dictionary
                        are all the different pages per block e.g.
                        {2: Queue(), 4: Queue(), 8: Queue() etc.}
       processQueue - Queue of processes requiring memory allocation
       hardDrive - Pages that have been replaced are stored in the hard drive (a list in my implementation)"""

    def __init__(self):
        self.freeMemory = SLL()
        self.occupiedMemory = {}
        self.processQueue = Queue()
        self.createBlocks()
        self.hardDrive = []

    def createBlocks(self):
        """Initialise all the required blocks:
           32 blocks of 2 pages
           16 blocks of 4 pages
           16 blocks of 8 pages
           16 blocks of 16 pages
           16 blocks of 32 pages
           Also, occupiedMemory dictionary keys are initialised """
        i = 0
        while i < 32:
            newBlock = Block(2)
            self.freeMemory.add_node(newBlock)
            i += 1
        q = Queue()
        self.occupiedMemory[2] = q
        j = 4
        while True:
            q = Queue()
            self.occupiedMemory[j] = q
            k = 0
            while k < 16:
                newBlock = Block(j)
                self.freeMemory.add_node(newBlock)
                k += 1
            j = j*2
            if j > 32:
                break
        self.freeBlocks = self.freeMemory.size


    def addRequest(self, request):
        """Add memory request to the processQueue"""
        self.processQueue.add(request)

    def addRequestList(self, requestList):
        """Add list of memory requests to the processQueue (more convenient than above method)"""
        for i in requestList:
            self.processQueue.add(i)

    def executeRequests(self):
        """Method that executes memory allocation for all items in processQueue"""
        for i in self.processQueue.queue:
            self.allocateMemory(i.pID, i.size//4)
        self.processQueue.queue = []

    def allocateMemory(self, pID, pages):
        """Core method of the class - allocates all the memory requests to the main memory using next fit."""

        #create pointer to check if entire memory was already checked
        current_value = self.freeMemory.previous
        #get the correct key for occupied dictionary
        if pages < 33:
            if pages <= 2:
                pgReq = 2
            elif pages > 2 and pages < 4:
                pgReq = 4
            elif pages > 4 and pages < 8:
                pgReq = 8
            elif pages > 8 and pages < 16:
                pgReq = 16
            else:
                pgReq = 32
            while True:
                #loop that iterates through freeMemory blocks(Starting at block that was next for the last iteration
                # i.e. Next Fit) until appropriate size is encountered
                if self.freeMemory.current.item.pages >= pages:
                    #If block is big enough, allocate current request to it and break to move to next request
                    pageCount = self.freeMemory.current.item.pages
                    allocatedBlock = self.freeMemory.remove_current()
                    allocatedBlock.item.pID = pID
                    self.occupiedMemory[pageCount].add(allocatedBlock)
                    break
                elif self.freeMemory.current.item.pages < pages:
                    #Otherwise, move pointer to next
                    self.freeMemory.next_node()
                if self.freeMemory.current == current_value:
                    #If pointer looped through entire memory without allocating the request, run page replacement.
                    #Then allocate it to the occupiedMemory and give it the correct process id
                    freeBlock = self.memoryReplacement(pgReq)
                    freeBlock.item.pID = pID
                    self.occupiedMemory[freeBlock.item.pages].add(freeBlock)
                    break
        #If the request size is larger than biggest block, don't allocate it
        elif pages >= 33:
            print("Process", pID, "is too large (", pages, "pages)")



    def memoryReplacement(self, pages):
        """Given the required amount of pages in block for memory request, remove a page from occupiedMemory,
           store it in the hard drive, make it free, and return the free block"""
        freeBlock = self.occupiedMemory[pages].removeReturn()
        self.hardDrive.append(freeBlock)
        freeBlock.item.pID = 0
        return freeBlock


    def printFreeMemory(self):
        """Method that prints out the state of freeMemory"""
        print("Free Memory Blocks:")
        print(self.freeMemory.__str__())
        print("Free memory size:", self.freeMemory.size, "blocks \n")

    def printOccupiedMemory(self):
        """Method that prints out the state of occupiedMemory"""
        print("Occupied Memory Blocks")
        for key in self.occupiedMemory:
            print(self.occupiedMemory[key].__str__())

    def printHardDrive(self):
        """Method that prints out the state of hardDrive"""
        print("Hard drive blocks:")
        for i in self.hardDrive:
            print(i.item.__str__())



def looper():
    i = 0
    myl = []
    while i < 90:
        rand = random.randint(1, 140)
        p = ProcessRequest(i, rand)
        myl.append(p)
        i += 1
    return myl


ram = MainMemory()
mylist = looper()

ram.addRequestList(mylist)
ram.executeRequests()
ram.printOccupiedMemory()
ram.printFreeMemory()
ram.printHardDrive()
