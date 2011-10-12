#!/usr/bin/env python

class A():
    def __init__(self):
        self.stack = [1,2,3,4,5,6]
        self.num = 0
        self.stack = iter(self.stack)

    def advance_stack(self):
        self.num = self.stack.next()

class C():
    def __init__(self):
        self.c = A()

    
aa = A()
print("num variable {}".format(aa.num))
cc = C()
print("this is the c instance of A: {}".format(cc))
print("The current aa.num: {}".format(aa.num))
print("run cc.c.advance_stack()")
cc.c.advance_stack()
print("cc.c.num is now : {}".format(cc.c.num))
print("run cc.c.advance_stack()")
cc.c.advance_stack()
print("cc.c.num is now : {}".format(cc.c.num))

