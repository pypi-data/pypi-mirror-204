from collections.abc import Iterable
#CONSTANTS
class FontStyle:
    DEFAULT = 0
    BOLD = 1
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7

class FontColor:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37

class BackgroundColor:
    DEFAULT = ''
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47


def fibonacci(n:int):
    if type(n) != int:
        raise TypeError
    if n < 1:
        return "error, n should be a positive number which is greater than 1"
    if n < 3:
        return 1
    a, b = 1, 1

    for i in range(2, n):
        a = a + b if i % 2 == 0 else a
        b = a + b if i % 2 == 1 else b
    return a if a > b else b

def fibonacci_list(n):
    if type(n) != int:
        raise TypeError
    if n < 1:
        return "error, n should be a positive number which is greater than 1"
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    list = [1, 1]
    for i in range(2, n):
        list.append(list[i - 2] + list[i - 1])
    return list

class Queue:
    def __init__(self,size:int = -1):
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
        return f'Queue({str(self.__queue)}, ' \
               f'headPointer = {self.__head if self.__size != -1 else len(self.__queue) - 1}, ' \
               f'tailPointer = {self.__tail if self.__size != -1 else 0})'

    def __len__(self):
        return self.__count if self.__size != -1 else len(self.__queue)

    def __iter__(self):
        return iter(self.getlist())

    def __contains__(self, item):
        return item in self.getlist()

    def __getitem__(self, item):
        return self.getlist()[int(item)]

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
        contents = self.getlist()
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
            raise TypeError
        if self.__size > 0:
            if self.__count == self.__size:
                print('the queue is full, try pop()')
                return
            self.__queue[self.__tail] = content
            self.__tail = (self.__tail+1)%self.__size
            self.__count += 1
        else:
            try:
                self.__queue.append(content)
            except:
                print('invalid input')

    def pop(self):
        if self.__size > 0:
            if self.__count == 0:
                print('the queue is empty, try push()')
                return
            print('remove:', self.__queue[self.__head])
            self.__head = (self.__head + 1)%self.__size
            self.__count -= 1
        else:
            try:
                del self.__queue[0]
            except IndexError:
                print('warning : no value in the queue,try push(content) to add one')


class Stack():
    def __init__(self,size:int=-1):
        self.a = 0
        if size > 0:
            self.__stack = [0]*size
        else:
            self.__stack = []
        self.__size = size
        self.__top = -1

    def __repr__(self):
        return f'Stack({str(self.__stack)}, topPointer = {self.__top if self.__top != -1 else len(self.__stack)-1})'

    def __len__(self):
        return self.__top if self.__size != -1 else len(self.__stack)

    def __iter__(self):
        return iter(self.getlist())

    def __contains__(self, item):
        return item in self.getlist()

    def __getitem__(self, item):
        return self.getlist()[int(item)]

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
            raise TypeError
        if self.__size > 0:
            if self.__top < self.__size - 1:
                self.__top += 1
                self.__stack[self.__top] = content
            else:
                print('stack is full, try pop()')
        else:
            self.__stack.insert(0,content)

    def pop(self):
        if self.__size > 0:
            if self.__top > -1:
                print(self.__stack[self.__top])
                self.__top -= 1
            else:
                print('warning : stack is empty ,try push(content)')
        else:
            try:
                print(self.__stack[0])
                del self.__stack[0]
            except IndexError:
                print('warning : stack is empty ,try push(content)')

class Hmath:
    class Functions:
        def __init__(self, expression: str, variable: str):
            if type(expression) != str or type(variable) != str:
                raise TypeError
            self.__expression = expression
            self.__var = variable

        def evaluate(self, value: int|float):
            if type(value) not in (int, float):
                raise TypeError
            expression = self.__expression.replace(self.__var, str(value))
            return eval(expression)

        def gradient(self, accuracy:float, value: int|float):
            if type(value) not in (int, float) or type(accuracy) != float:
                raise TypeError
            x1 = value
            x2 = value + 10 ** -accuracy
            y1 = self.evaluate(x1)
            y2 = self.evaluate(x2)
            res = (y2 - y1) / (x2 - x1)
            return round(res, 1) if res - int(res) > 0.999 or res - int(res) < 0.001 else round(res, 3)


def prints(content,fontStyle=FontStyle.DEFAULT,fontColor=FontColor.WHITE,backgroundColor=BackgroundColor.DEFAULT):
    print("\033[{};{};{}m{}\033[0m".format(fontStyle,fontColor,backgroundColor,content))

class LinkedListNode:
    def __init__(self, val):
        if type(val) not in (int, str, float):
            raise TypeError
        self.val = val
        self.next = None

    def __repr__(self):
        result = ''
        temp = self
        while temp != None:
            result += (str(temp.val) + ' --> ')
            temp = temp.next
        print(result[:-5])
        return f'LinkedList({result})'

    def __iter__(self):
        return iter(self.getlist())

    def __contains__(self, item):
        return item in self.getlist()

    def __getitem__(self, item):
        return self.getlist()[int(item)]

    def getlist(self):
        content = []
        temp = self
        while temp != None:
            content.append(temp.val)
            temp = temp.next
        return content

def create_linkedlist_from_list(lst:list):
    if type(lst) != list:
        raise TypeError
    if len(lst) == 0:
        return LinkedListNode(None)
    node = LinkedListNode(lst[0])
    temp = node
    for i in lst[1:]:
        temp.next = LinkedListNode(i)
        temp = temp.next
    return node

def create_stack_from_list(lst:list, Fixedlength:bool = True):
    if type(lst) != list:
        raise TypeError

    if Fixedlength:
        stack = Stack(len(lst))
    else:
        stack = Stack()
    for i in lst:
        stack.push(i)
    return stack

def create_queue_from_list(lst:list, Fixedlength:bool = True):
    if type(lst) != list:
        raise TypeError

    if Fixedlength:
        queue = Queue(len(lst))
    else:
        queue = Queue()
    for i in lst:
        queue.push(i)
    return queue



def BinarySearch(iterable, target):
    if not isinstance(iterable, Iterable):
        raise TypeError
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
















