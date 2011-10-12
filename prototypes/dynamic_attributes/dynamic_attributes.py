#!/usr/bin/env python

class A():
    def __init__(self):
        self.a = 1



class C():
    def __init__(self):
        self.c = A()
        self.set_remote(self.c, 99)

    def set_remote(self, name, val):
        setattr(name, 'a', val)


aa = A()
print("this is original {}".format(aa.a))
cc = C()
print("this is the c instance of A: {}".format(cc))
print("The original .a was changed by C so is: {}".format(aa.a))
print("The original cc.c.a should now be 99 but is: {}".format(cc.c.a))

