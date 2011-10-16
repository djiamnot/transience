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
        setattr(name, 'b', val*2)
        setattr(name, 'z', val*val)


aa = A()
print("this is original {}".format(aa.a))
cc = C()
print("this is the c instance of A: {}".format(cc))
print("The original .a was changed by C so is: {}".format(aa.a))
print("The original cc.c.a should now be 99 but is: {}".format(cc.c.a))


class Z():
    pass 

r = Z()

mylist = [1,2,3,4,5]
for i in mylist:
    setattr(r, 'var'+str(i), i)

print(r.var1)
print(r.var2)
print(r.var3)
print(r.var4)
print(r.var5)
