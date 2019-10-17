class Deque:
    def __init__(self):
        #use python list structure
        # index 0 is rear, index[-1] is front
        self.items = []

    def add_front(self, item): 
        return self.items.append(item)

    def add_rear(self, item): 
        return self.items.insert(0, item)
        
    def remove_front(self): 
        return self.items.pop()
        
    def remove_rear(self): 
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]

    def peeklast(self):
        return self.items[0]

    def printall(self, index):
        #prints from rear end [0]
        if len(self.items) == 0:
            print("")
        elif index == 0:
            print(self.items[0], "* " * (len(self.items)-1), sep=' ')
        else:
            for item in self.items:
                print(item, end = ' ')
            print(' ')