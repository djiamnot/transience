# original idea borrowed from Michael Chermside:
# http://code.activestate.com/recipes/142435-list-iterator-with-advance-and-regress/

class Flexiterator(object):
    """This is an iterator for lists which allows one to advance
    or regress the position in the list. It also will raise an
    exception if the list is lengthened or shortened."""
    
    def __init__(self, myList):
        self.myList = myList
        self.originalLength = len(myList)
        self.nextIndex = 0

    def __iter__(self):
        return self

    class ListModifiedException(Exception):
        pass

    def next(self):
        if len(self.myList) != self.originalLength:
            raise Flexiterator.ListModifiedException

        index = self.nextIndex
        if index >= self.originalLength:
            raise StopIteration
        self.nextIndex += 1
        return self.myList[index]

    def prev(self):
        if len(self.myList) != self.originalLength:
            raise Flexiterator.ListModifiedException

        index = self.nextIndex - 1
        if index < 1:
            raise StopIteration
        self.nextIndex -= 1
        return self.myList[index]

    def advance(self, places=1):
        self.nextIndex += places

    def regress(self, places=1):
        self.nextIndex -= places
