Rafal Harasienski

#Assignment 1


class queue:
    """Helper class for creating instances of queues for each level"""

    def __init__(self, quantum):
        """Construct empty list that serves as queue"""
        self.queue = []
        self.quantum = quantum

    def add(self, process):
        """Append process to end of queue"""
        self.queue.append(process)

    def queueLength(self):
        return len(self.queue)

    def remove(self):
        """Remove the first process from the queue"""
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
        """Check amount of processes in queue"""
        return len(self.queue)

    def clear(self):
        """Empty the queue, implemented during idle phase when nothing is to be done"""
        self.queue = []


class process:
    """Class to create instances of processes. Set inout to True to make process an I/O process.
       Set ioLimit to desired amount of time to be waited before I/O operation is completed"""
    def __init__(self, time, inout=False, ioLimit=10):
        self.time = time
        self.status = "Ready"
        self.inout = inout
        self.ioDuration = 0
        self.ioLimit = ioLimit

    def setStatus(self, status):
        self.status = status


class MFQ:
    """Multi-level Feedback Queue. Schedule implemented using list of queues.
       Index of the queue serves as indicator of the level. Essentially this
       implementation is just a list of lists"""
    def __init__(self):
        self.schedule = []
        self.blockList = []
        self.processCount = 0

    def scheduleLength(self):
        return len(self.schedule)

    def newLevel(self):
        """Create new level of priority (new queue). Quantum is made up of
           (2**i)*q  ---> whereby i is the priority (depending on amount of
           items already in the schedule) and q is just a constant of 2 in
           my implementation"""
        newQuantum = (2 ** self.scheduleLength()) * 2
        newQueue = queue(newQuantum)
        self.schedule.append(newQueue)


    def addProcess(self, process, level = 0):
        """Add process to schedule, to first queue (priority 0) if exists. If doesn't
           exist then create the queue and then add process. Can also specify what level to add process
           to if needed (implemented automatically, preferrably not by user)"""
        if self.scheduleLength() != 0 and self.scheduleLength() < 8:
            self.schedule[level].add(process)
        else:
            self.newLevel()
            self.schedule[level].add(process)
        self.processCount += 1

    def moveDown(self, queue):
        """Move process down to next priority level if it exists. If not, create it and then
        add process if the priority isn't too low. The parameter queue is the index
        number of the queue in the schedule"""
        if queue < self.scheduleLength() - 1 and self.scheduleLength() < 8:
            temp = self.schedule[queue].removeReturn()
            self.schedule[queue + 1].add(temp)
        elif self.scheduleLength() < 8:
            self.newLevel()
            temp = self.schedule[queue].removeReturn()
            self.schedule[queue + 1].add(temp)
        else:
            print("Lowest priority reached, FCFS occurs in this level")

    def execute(self):
        """Most complex method. Loop that executes all the processes following MFQ rules, will
           implement several helper methods to make the code more clear to follow. This method assumes
           that all the desired processes have already been added to the schedule."""

        while self.scheduleLength() > 0 or len(self.blockList) > 0:
            i = 0
            while i < self.scheduleLength():

                '''every iteration print whole schedule to keep track of processes'''
                self.timeForAll()
                quantum = self.schedule[i].quantum
                j = 0

                '''In case there are no more iterations to be done in the next loop, then make sure that
                   blocked processes don't stay blocked forever.'''
                if len(self.blockList) > 0:
                    self.io(self.blockList, i)

                '''Power saver mode in case few processes left in schedule'''
                if self.processCount + len(self.blockList) < 4:
                    print("There are not many processes remaining in the queue, entering power saver mode")

                while j < self.schedule[i].queueLength():

                    '''Every iteration is one unit of time for I/O operation in my implementation. Here
                       The next lines of code add 1, for each iteration, to the duration of I/O operation.
                       If the process to be executed is an I/O process, it is removed from its queue and put
                       into a list of blocked processes, where it waits for the time specified in the process.
                       Additionaly its state is changed'''
                    if len(self.blockList) > 0:
                        self.io(self.blockList, i)
                        print("Blocked list", self.blockList)
                    if self.schedule[i].queue[j].inout is True and self.schedule[i].queue[j].status == "Ready":
                        self.schedule[i].queue[j].status = "Blocked"
                        self.blockList.append(self.schedule[i].queue[j])
                        print(self.schedule[i].queue[j], "added to block list")
                        self.schedule[i].remove()
                        self.processCount -= 1
                        continue

                    print("Before quantum subtraction", self.schedule[i].queue[j].time)
                    self.schedule[i].queue[j].time -= quantum
                    print("After quantum subtraction", self.schedule[i].queue[j].time)
                    if self.schedule[i].queue[j].time <= 0:
                        print("Process", self.schedule[i].queue[j], "is finished")
                        self.schedule[i].remove()
                        self.processCount -= 1
                    else:
                        self.moveDown(i)
                i += 1
            '''Check to see if there are any processes that were omitted, if so continue loop. Otherwise,
               end the MFQ loop by initiating idle process and then using break'''
            aggregator = 0
            for i in self.schedule:
                aggregator += len(i.queue)
            if aggregator != 0:
                continue
            else:
                self.idle()
                break

    def timeForAll(self):
        """Displays whole MFQ with all levels and processes, with the processes being shown by their
           remaining time slice. MFQ represented by list of lists"""
        output = []
        for x in self.schedule:
            new_list = []
            z = 0
            while z < len(x.queue):
                new_list.append(x.queue[z].time)
                z += 1
            output.append(new_list)
        print(output)

    def idle(self):
        """Idle process that does cleaning up and then puts CPU into sleep mode"""
        self.schedule = []
        self.blockList = []
        print("System is now entering sleep mode")


    def io(self, mylist, level):
        """This method manages the blocked processes. Every time it is called (every iteration), it increases
           block duration of each process by one. If the processes reach their specified wait limit,
           they are removed from the list and added back to the schedule with the highest priority. This
           implementation was the cleanest for the purpose of this simple simulator"""
        del_list = []
        for i in mylist:
            print("Block duration",i.ioDuration)
            i.ioDuration += 1
            if i.ioDuration >= i.ioLimit:
                self.addProcess(i, level)
                del_list.append(i)
        mylist = set(self.blockList) - set(del_list)
        self.blockList = list(mylist)


processA = process(1,True, 5)
processB = process(2)
processC = process(3)
processD = process(4)
thing = MFQ()
thing.addProcess(processA)
thing.addProcess(processB)
thing.addProcess(processC)
thing.addProcess(processD)
thing.execute()