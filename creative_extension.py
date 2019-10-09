import tkinter as tk
import tkinter.messagebox
import random
from tkinter import ttk
from tkinter import *
from solitaire_class import Solitaire
from deque_class import Deque
import sys

def new_game():
    deal = []
    total_num = int(ncards_entry.get())
    for i in range(total_num):
        deal.append(i)
    random.shuffle(deal)
    real_game = Solitaire(deal)
    game.delete('1.0','end')
    real_game.display()
        
def counter():
    count.set(count+1)


def undo():
    pass

def help():
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

option_frame = tk.Frame(simple_solitaire, height = 70,highlightbackground = "black", highlightthickness = 4)
option_frame.pack(ipadx=5, ipady=5, side=TOP, fill=X)

move_count_frame = tk.Frame(simple_solitaire, height = 50, highlightbackground = "red", highlightthickness = 3)
move_count_frame.pack(fill=X, side=BOTTOM) 

move_frame = tk.Frame(simple_solitaire, height=50)
move_frame.pack(ipadx=5, ipady=10, side=TOP, fill=X)
    
game_frame = tk.Frame(simple_solitaire, highlightbackground = "blue", highlightthickness = 5)
game_frame.pack(ipady=10,ipadx=10,fill=BOTH,expand=TRUE)

moving_from_label = tk.Label(move_frame, text = "Moving from pile no.")
moving_from_label.pack(side=LEFT)
from_pile_entry = tk.Entry(move_frame, width=2)
from_pile_entry.pack(side=LEFT)
to_pile_label = tk.Label(move_frame, text = "to pile no.")
to_pile_label.pack(side=LEFT)
to_pile_entry = tk.Entry(move_frame, width=2)
to_pile_entry.pack(side=LEFT)

game = tk.Text(game_frame)
game.pack(fill=X)

move_count_label = tk.Label(move_count_frame, text="MOVE COUNT:")
move_count_label.pack(side=LEFT, ipadx=8)

count = tk.IntVar() #establish move int var
count.set(0)
count_label = tk.Label(move_count_frame, textvariable=count)
count_label.pack(side=LEFT)

out_of_label = tk.Label(move_count_frame, text="OUT OF")
out_of_label.pack(side=LEFT)

move_available = 6
move_available_label = tk.Label(move_count_frame, text=move_available)
move_available_label.pack(side=LEFT)

undo_button = tk.Button(option_frame, text="UNDO")
undo_button.pack(side=LEFT, ipadx=5, padx=8)

help_button = tk.Button(option_frame, text="HELP", command=help)
help_button.pack(side=LEFT, ipadx=5)

start_button = tk.Button(option_frame, text="START", command=new_game)
start_button.pack(side=RIGHT,ipadx=5, padx=8)

ncards_label2 = tk.Label(option_frame, text="items")
ncards_label2.pack(side=RIGHT)

ncards_entry = tk.Entry(option_frame, width=3)
ncards_entry.pack(side=RIGHT)
ncards_entry.insert(0,0)
ncards_entry.focus_set()  #sets the focus on entry 

ncards_label1 = tk.Label(option_frame, text="Playing with")
ncards_label1.pack(side=RIGHT, padx=(20,0))
#redirecting stdout to tkinter window
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        #self.widget.configure(state="disabled")

sys.stdout = TextRedirector(game, "stdout")
sys.stderr = TextRedirector(game, "stderr")

simple_solitaire.mainloop()
