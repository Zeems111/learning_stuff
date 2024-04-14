"""There is an abstract data type Stack that implements LIFO contract.
The stack has methods push and pop - add an element to the end of the stack
and pick up an element at the end of the stack. In Python type list implements
stack: push method is replaced by append method, pop method remains the same.

There is an another abstract data type Queue that implements FIFO contract.
The queue also has methods push and pop.
However, method push adds an element to the end of the queue, and method
pop extracts the element from the beginning of the queue. Using list in
this case is not very good because method pop(index=0) method works over
a linear time, but we want the push and pop methods to work over О(1).
In this task, you need to implement a queue on two stacks. One stack is
used only for writing elements, and the second stack is used only for
extracting elements. If the method pop is called for an empty queue
throw an exception IndexError with the message 'pop from an empty queue'."""
class Queue:
    def __init__(self):
        self.stack_in = list()
        self.stack_out = list()

    def push(self, x):
        self.stack_in.append(x)
        pass

    def pop(self):
        while self.stack_in:
            self.stack_out.append(self.stack_in.pop())
        try:
            return self.stack_out.pop()
        except IndexError as err:
             raise IndexError('pop from an empty queue') from None


queue = Queue()
try:
    queue.pop()  # IndexError('pop from an empty queue')
except:
    pass
queue.push(3)
queue.push(5)
queue.push(7)
queue.push(9)

print(queue.pop())  # return 3
print(queue.pop())  # return 5
print(queue.pop())  # return 7
print(queue.pop())  # return 9
queue.pop()  # IndexError('pop from an empty queue')