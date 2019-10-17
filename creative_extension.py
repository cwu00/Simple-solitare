import tkinter as tk
import tkinter.messagebox
import random
from tkinter import ttk
from tkinter import *
from deque_class import Deque
import sys
import os

game_iter = 1
real_game = None

# modified solitaire class
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
        piles = self.__ColNo
        for i in range(piles):
            if i == 0:
                print("{}: ".format("FOUNDATION (0)"), end = '')
            else:
                print("{}: ".format(i), end = '')
            self.t[i].printall(i)
        print("")

    def move(self, c1, c2):
        c1 = int(c1)
        c2 = int(c2)
        if c1 == c2 and c1 == 0: #always valid
            self.t[0].add_front(self.t[0].remove_rear())

        elif c1 == 0 and c2 > 0: #valid when N2 = N1 + 1
            if self.t[c2].size() == 0:
                self.t[c2].add_front(self.t[0].remove_rear())

            elif self.t[c2].peek() == self.t[0].peeklast() + 1:
                self.t[c2].add_front(self.t[0].remove_rear())
                
        elif c1 > 0 and c2 > 0: #valid when N2 = N1 + 1
            if self.t[c2].peek() == self.t[c1].peeklast() + 1:
                while self.t[c1].size() != 0:
                    self.t[c2].add_front(self.t[c1].remove_rear())
        real_game.display()

    def IsComplete(self):
        if self.t[0].size() == 0:
            check = 1
            while (check <= self.__ColNo-1): #check each line
                if self.t[check].size() != self.__CardNo: #if line has less than total num of cards, move on
                    check += 1
                elif self.t[check].size() == self.__CardNo:
                    return True
        return False

    def get_c1(self):
        global game_iter
        global real_game
        try:
            c1 = int(from_pile_entry.get())
            if c1 > (real_game.__ColNo):
                raise Exception
            to_pile_entry.focus_set()  #moves focus only when first input is valid
            return c1
        except:
            print("INVALID PILE NUMBER")
            game_iter += 1
            count_label.config(text=game_iter+1)
            from_pile_entry.delete("0",tk.END)
            c1 = Solitaire.get_c1      #continue getting input if it is not valid

    def get_c2(self):
        global game_iter
        global real_game
        try:
            c1 = real_game.get_c1()
            c2 = int(to_pile_entry.get())
            if c2 > real_game.__ColNo:
                raise Exception
            from_pile_entry.focus_set()
            game_iter += 1
            count_label.config(text=game_iter)
            from_pile_entry.delete("0",tk.END)   #clears entry boxes for c1 and c2 for next round(s)
            to_pile_entry.delete("0",tk.END)
            real_game.play(c1, c2)
        except:
            print("INVALID PILE NUMBER")
            game_iter += 1
            count_label.config(text=game_iter)
            to_pile_entry.delete("0",tk.END)
            c2 = Solitaire.get_c2

    def play(self,c1,c2):
        global game_iter
        if game_iter <= self.__ChanceNo:
            self.move(c1, c2)
            if (self.IsComplete() == True):
                print("You win in {} steps!".format(game_iter))
                ncards_entry.focus_set()
            else:
                if game_iter == self.__ChanceNo:
                    print("You Lose!")
                    ncards_entry.focus_set()
    
    def set_cursor_to_pile(self):
        to_pile_entry.focus_set()


###CREATIVE EXTENSION
def new_game():
    global game_iter
    global real_game
    game_iter = 0
    from_pile_entry.focus_set()                         #set focus to (move from) entry box
    deal = []
    total_num = int(ncards_entry.get())                 #gets user input of number of cards
    move_available = total_num*2                        #calculates total moves available
    move_available_label.config(text=move_available)    #shows moves availble on screen
    for i in range(total_num):
        deal.append(i)
    random.shuffle(deal)                                #shuffles cards 
    real_game = Solitaire(deal)
    game.delete('0.0',tk.END)                           #clears game screen
    print("**************************NEW GAME**************************")
    real_game.display()                                 ###change this to play when everything works###

def undo():
    print("UNDO")

def help_func():
    rules = "This is a simplified version of the classic game of Solitaire.\n"\
        "\nYou can choose how many items (cards) you would like to play with by"\
        "entering a number between 1-50 in the top right corner.\n"\
            "\nThe aim of the game is to build up a stack of cards in descending order, "\
            "from the number you entered - 1, to 0.\n"\
                "\nAfter you enter in the pile number, hit enter.\n"\
                "\nPile 0 is your foundation pile, where only the top card is shown, "\
                "and the other piles are all empty to start with.\n"\
                    "\nAn empty pile can be filled with any card.\n"\
                    "\nFrom the foundation pile, you are allowed to move one card at a time.\n"\
                    "\nAll other piles should be built down in descending order.\n"\
                    "\nYou can move stacks of a pile (not the foundation pile) to another pile, "\
                    "if they are built down in order.\n"\
                        "\nIf you don't want to or cannot move a card to another pile from the foundation pile,"\
                        "you can place it at the bottom of the foundation pile by moving from pile 0 to pile 0."
    tk.messagebox.showinfo("HELP", rules)


simple_solitaire = tk.Tk()
simple_solitaire.geometry("430x400+500+200")
simple_solitaire.title("SIMPLE SOLITARE")

option_frame = tk.Frame(simple_solitaire, height = 70,highlightbackground = "black", highlightthickness = 1)
option_frame.pack(ipadx=5, ipady=5, side=TOP, fill=X)

move_count_frame = tk.Frame(simple_solitaire, height = 50, highlightbackground = "black", highlightthickness = 1)
move_count_frame.pack(fill=X, side=BOTTOM) 

move_frame = tk.Frame(simple_solitaire, height=50, highlightbackground="black",highlightthickness=1)
move_frame.pack(ipadx=5, ipady=10, side=TOP, fill=X)
    
game_frame = tk.Frame(simple_solitaire, highlightbackground = "black", highlightthickness = 1)
game_frame.pack(ipady=10,ipadx=10,fill=BOTH,expand=TRUE)

moving_from_label = tk.Label(move_frame, text = "Moving from pile no.")
moving_from_label.pack(side=LEFT)

to_pile_entry = tk.Entry(move_frame, width=2)
from_pile_entry = tk.Entry(move_frame, width=2)
from_pile_entry.pack(side=LEFT)
from_pile_entry.insert(0,' ')
from_pile_entry.bind("<Return>",Solitaire.get_c1)

to_pile_label = tk.Label(move_frame, text = "to pile no.")
to_pile_label.pack(side=LEFT)


to_pile_entry.pack(side=LEFT)
to_pile_entry.insert(0,' ')
to_pile_entry.bind("<Return>", Solitaire.get_c2)                #solitaire class gets input number 2 when 'enter' is pressed

game = tk.Text(game_frame)
game.pack(fill=X)

undo_button = tk.Button(option_frame, text="UNDO", command=undo)
undo_button.pack(side=LEFT, ipadx=5, padx=8)

help_button = tk.Button(option_frame, text="HELP", command=help_func)
help_button.pack(side=LEFT, ipadx=5)

start_button = tk.Button(option_frame, text="START", command=new_game)
start_button.pack(side=RIGHT,ipadx=5, padx=8)

ncards_label2 = tk.Label(option_frame, text="items")
ncards_label2.pack(side=RIGHT)

ncards_entry = tk.Entry(option_frame, width=3)
ncards_entry.pack(side=RIGHT)
ncards_entry.insert(0,3)
ncards_entry.focus_set()                                        #sets the focus on entry

ncards_label1 = tk.Label(option_frame, text="Playing with")
ncards_label1.pack(side=RIGHT, padx=(20,0))

move_count_label = tk.Label(move_count_frame, text="MOVE COUNT:")
move_count_label.pack(side=LEFT, ipadx=8)

count_label = tk.Label(move_count_frame, text=0)
count_label.pack(side=LEFT)

out_of_label = tk.Label(move_count_frame, text="OUT OF")
out_of_label.pack(side=LEFT)

move_available_label = tk.Label(move_count_frame, text='0')
move_available_label.pack(side=LEFT)

#redirecting stdout to tkinter window
class TextRedirector():
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
sys.stdout = TextRedirector(game, "stdout")
sys.stderr = TextRedirector(game, "stderr")

simple_solitaire.mainloop()
