from deque_class import Deque
class Solitaire:
    def __init__(self, ncards):
        self.t = []
        self.__CardNo = len(ncards)
        self.__ColNo = (self.__CardNo // 8) + 3 #number of card piles
        self.__ChanceNo = self.__CardNo * 2
        for i in range(self.__ColNo):
            self.t.append(Deque())
        for i in range(self.__CardNo):
            self.t[0].add_front(ncards[i])

    def display(self):
        #self.__ColNo number of card piles
        #each card pile is stored as a deque
        piles = self.__ColNo
        for i in range(piles):
            print("{}: ".format(i), end = '')
            self.t[i].printall(i)

    def move(self, c1, c2):
        if c1 == c2 and c1 == 0: #always valid
            self.t[0].add_front(self.t[0].remove_rear())

        elif c1 == 0 and c2 > 0: #valid when N2 = N1 + 1
            if self.t[c2].size() == 0:
                self.t[c2].add_front(self.t[0].remove_rear())

            elif self.t[c2].peek() == self.t[0].peeklast() + 1:
                self.t[c2].add_front(self.t[0].remove_rear())

            else:
                print("ILLEGAL MOVE")

        elif c1 > 0 and c2 > 0: #valid when N2 = N1 + 1
            try:
                if self.t[c2].peek() == self.t[c1].peeklast() + 1:
                    while self.t[c1].size() != 0:
                        self.t[c2].add_front(self.t[c1].remove_rear())
            except IndexError:
                print("ILLEGAL MOVE")

    def IsComplete(self):
        if self.t[0].size() == 0:
            check = 1
            while (check <= self.__ColNo-1): #check each line
                if self.t[check].size() != self.__CardNo: #if line has less than total num of cards, move on
                    check += 1
                elif self.t[check].size() == self.__CardNo:
                    return True
        return False

    def play(self): 
        print("*****************************************NEW "\
            "GAME***************************************") 
        for game_iter in range(self.__ChanceNo):
            self.display()
            print("Round", game_iter+1, "out of", self.__ChanceNo, end = ": ")
            col1 = int(input("Move from row no.:"),10)
            print("Round", game_iter+1, "out of", self.__ChanceNo, end = ": ")
            col2 = int(input("Move to row no.:"),10)
            if col1 >= 0 and col2 >= 0 and col1 < self.__ColNo and col2 < self.__ColNo:
                self.move(col1, col2)
            if (self.IsComplete() == True):
                print("You Win in", game_iter+1, "steps!")
                break
            else:
                if game_iter+1 == self.__ChanceNo:
                    print("You Lose!")
        print()

cards = [1, 2, 3]
game = Solitaire(cards)
game.play()