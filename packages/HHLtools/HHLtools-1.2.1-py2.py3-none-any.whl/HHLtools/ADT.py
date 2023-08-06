from collections.abc import Iterable
from HHLtools.Herror import *
class Queue:
    def __init__(self,size:int = -1):
        """
        :param size: the fixed size of the queue, if not set, infinite length
        """
        if size > 0:
            self.__size = size
            self.__queue = [0] * size
            self.__head = 0
            self.__tail = 0
            self.__count = 0
        else:
            self.__size = size
            self.__queue = []

    def __repr__(self):
        if self.__size != -1:
            return f'Queue({str(self.__queue)}, ' \
               f'headPointer = {self.__head if self.__size != -1 else len(self.__queue) - 1}, ' \
               f'tailPointer = {self.__tail if self.__size != -1 else 0}, Fixedlength = True)'
        else:
            return f'Queue({str(self.__queue)})'

    def __len__(self):
        return self.__count if self.__size != -1 else len(self.__queue)

    def __iter__(self):
        return iter(self.getlist())

    def __contains__(self, item):
        return item in self.getlist()

    def __getitem__(self, item):
        return self.getlist()[int(item)]

    def __eq__(self, other):
        return self.getlist() == other.getlist()

    def getlist(self):
        contents = []
        if self.__size == -1:
            contents = self.__queue[:]
        else:
            head = self.__head
            while 1:
                contents.append(self.__queue[head])
                head += 1
                head = head % self.__size
                if head == self.__tail:
                    break
        return contents

    def show(self):
        contents = self.__queue
        maxlen = 0
        for c in contents:
            if len(str(c)) > maxlen:
                maxlen = len(str(c))
        print('='*(15+maxlen+15))
        for c in range(len(contents)):
            front = ' '*15
            end = ' '
            if c == self.__head:
                front = 'headPointer    '
            if c == self.__tail:
                end = (maxlen+4)*' ' +'tailPointer'
            print(front+str(contents[c])+' '*(maxlen-len(str(contents[c])))+end)
        print('=' * (15 + maxlen + 15))

    def push(self, content: int|str|float):
        if type(content) not in (int, str, float):
            error(TypeError, f"push() argument must be an integer, a string, or a real number, not {str(type(content))[7:-1]}")
        if self.__size > 0:
            if self.__count == self.__size:
                error(IndexOutOfBoundError, 'the queue is full, try pop()')
                return
            self.__queue[self.__tail] = content
            self.__tail = (self.__tail+1)%self.__size
            self.__count += 1
        else:
            self.__queue.append(content)

    def pop(self):
        if self.__size > 0:
            if self.__count == 0:
                return None
            self.__head = (self.__head + 1)%self.__size
            self.__count -= 1
            return self.__queue[self.__head]
        else:
            try:
                del self.__queue[0]
            except IndexError:
                return None


class Stack():
    def __init__(self,size:int=-1):
        """

        :param size: the fixed size of the stack, if not set, infinite length
        """
        self.a = 0
        if size > 0:
            self.__stack = [0]*size
        else:
            self.__stack = []
        self.__size = size
        self.__top = -1

    def __repr__(self):
        if self.__size != -1:
            return f'Stack({str(self.__stack)}, topPointer = {self.__top if self.__top != -1 else len(self.__stack)-1})'
        else:
            return f'Stack({str(self.__stack)})'

    def __len__(self):
        return self.__top if self.__size != -1 else len(self.__stack)

    def __iter__(self):
        return iter(self.getlist())

    def __contains__(self, item):
        return item in self.getlist()

    def __getitem__(self, item):
        return self.getlist()[int(item)]

    def __eq__(self, other):
        return self.getlist() == other.getlist()

    def getlist(self):
        contents = []
        if self.__size == -1:
            contents = self.__stack[:]
        else:
            for i in range(0, self.__top):
                contents.append(self.__stack[i])
        return contents

    def push(self, content: int|str|float):
        if type(content) not in (int, str, float):
            error(TypeError, f"push() argument must be an integer, a string, or a real number, not {str(type(content))[7:-1]}")
        if self.__size > 0:
            if self.__top < self.__size - 1:
                self.__top += 1
                self.__stack[self.__top] = content
            else:
                error(IndexOutOfBoundError, 'the stack is full, try pop()')
        else:
            self.__stack.insert(0,content)

    def pop(self):
        if self.__size > 0:
            if self.__top > -1:
                self.__top -= 1
                return self.__stack[self.__top]
            else:
                return None
        else:
            try:
                del self.__stack[0]
                return self.__stack[0]
            except IndexError:
                return None



class LinkedListNode:
    def __init__(self, val):
        if type(val) not in (int, str, float):
            error(TypeError, f"an element in linked list must be an integer, a string, or a real number, not {str(type(val))[7:-1]}")
        self.val = val
        self.next = None

    def __repr__(self):
        content = []
        temp = self
        while temp.next is not None:
            content.append(temp.val)
            temp = temp.next
        content.append(temp.val)
        return f'LinkedList({content})'

    def __iter__(self):
        return iter(self.getlist())

    def __contains__(self, item):
        return item in self.getlist()

    def __getitem__(self, item):
        return self.getlist()[int(item)]

    def __eq__(self, other):
        return self.getlist() == other.getlist()

    def __add__(self, other):
        if type(other) != LinkedListNode:
            error(TypeError, "unsupported operand type(s) for +: 'LinkedListNode' and {str(type(other))[7:-1]}")
        temp = self
        while temp.next is not None:
            temp = temp.next
        temp.next = other
        return self

    def getlist(self):
        content = []
        temp = self
        while temp is not None:
            content.append(temp.val)
            temp = temp.next
        return content

def create_linkedlist_from_list(lst:list):
    if not isinstance(lst, Iterable):
        error(TypeError, f"'{type(lst)}' object is not iterable")
    if len(lst) == 0:
        return LinkedListNode(None)
    node = LinkedListNode(lst[0])
    temp = node
    for i in lst[1:]:
        temp.next = LinkedListNode(i)
        temp = temp.next
    return node

def create_stack_from_list(lst:list, Fixedlength:bool = True):
    if not isinstance(lst, Iterable):
        error(TypeError, f"'{type(lst)}' object is not iterable")

    if Fixedlength:
        stack = Stack(len(lst))
    else:
        stack = Stack()
    for i in lst:
        stack.push(i)
    return stack

def create_queue_from_list(lst:list, Fixedlength:bool = True):
    if not isinstance(lst, Iterable):
        error(TypeError, f"'{type(lst)}' object is not iterable")

    if Fixedlength:
        queue = Queue(len(lst))
    else:
        queue = Queue()
    for i in lst:
        queue.push(i)
    return queue



def BinarySearch(iterable, target):
    if not isinstance(iterable, Iterable):
        error(TypeError, f"'{type(iterable)}' object is not iterable")
    found = False
    highIndex = len(iterable)-1
    lowIndex = 0
    while not found and lowIndex <= highIndex:
        mid = (highIndex + lowIndex) // 2
        if iterable[mid] == target:
            found = True
            print(mid)
        elif iterable[mid] > target:
            highIndex = mid - 1
        else:
            lowIndex = mid + 1

    if not found:
        print("not found")

