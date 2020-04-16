"""
Charmaine Wu
twu268  928887253
This is a game of simplified card game Solitaire with simple user interactions.
"""
import json
from operator import itemgetter
import tkinter as tk
import tkinter.messagebox
import random
from tkinter import ttk
from tkinter import *
from A2 import Deque
import sys
import os

game_iter = 0
real_game = None

try:
    with open("scores.txt","r") as json_file:           #try to open the score file
        pass
except:
    with open("scores.txt",'w') as json_file:           #if the score file does not exist, create a file
        json.dump({}, json_file)

#modifies original solitaire class
class Solitaire:
    def __init__(self, ncards):
        self.t = []
        self.__CardNo = len(ncards)
        self.__ColNo = (self.__CardNo // 8) + 3
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
        game.see(tk.END)

    def move(self, c1, c2):
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

    def check_c1(self):
        global game_iter
        global real_game
        if game_iter == real_game.__ChanceNo:       #if the move count exceeds limit, then the player loses and the game ends
                print("\nYou Lose!\n\n")
                ncards_entry.focus_set()
                game.see(tk.END)
                return
        try:
            c1 = int(from_pile_entry.get())
            if c1 >= real_game.__ColNo:             #if the input is greater than number of piles available, raise exception
                raise Exception
            to_pile_entry.focus_set()               #if the input is valid, sets cursor to next entry box
        except:
            print("INVALID PILE NUMBER")
            game_iter += 1                          #invalid input results in move count to be incremented by one
            count_label.config(text=game_iter)
            from_pile_entry.delete("0", tk.END)     #the entry box is cleared
        finally:
            game.see(tk.END)
            
    def check_c2(self):
        global game_iter
        global real_game
        if game_iter == real_game.__ChanceNo:
                print("\nYou Lose!\n\n")
                ncards_entry.focus_set()
                game.see(tk.END)
                return
        try:
            c2 = int(to_pile_entry.get())
            if c2 >= real_game.__ColNo:
                raise Exception
            game_iter += 1                          #both inputs are valid, so move count increments by one
            count_label.config(text=game_iter)
            real_game.both_valid()
            from_pile_entry.focus_set()             #sets cursor to the first entry box for next round
        except:
            print("INVALID PILE NUMBER")
            game_iter += 1
            count_label.config(text=game_iter)
            to_pile_entry.delete("0", tk.END)
        finally:
            game.see(tk.END)

    def both_valid(self):
        global game_iter
        global real_game
        c1 = int(from_pile_entry.get())
        c2 = int(to_pile_entry.get())
        from_pile_entry.delete("0",tk.END)      #clears entry boxes for c1 and c2 for next round(s)
        to_pile_entry.delete("0",tk.END)
        real_game.play(c1, c2)

    def play(self,c1,c2):
        global game_iter
        if game_iter <= self.__ChanceNo:
            self.move(c1, c2)
            if (self.IsComplete() == True):
                print("You win in {} steps!\n\n".format(game_iter))
                ncards_entry.focus_set()                        #sets cursor on the top right entry box for next round
                Ranking()                                       #once the game is finished, the prompt window for player to enter their name pops up
            else:
                if game_iter == self.__ChanceNo:
                    print("You Lose!\n\n")
                    ncards_entry.focus_set()

###CREATIVE EXTENSION###
class Ranking:
    def __init__(self):
        prompt_window = Toplevel(simple_solitaire)
        prompt_window.title("Username Entry")
        prompt_window.geometry("230x100+600+300")
        self.window = prompt_window
        username_prompt = tk.Label(self.window, text="Enter your name")
        username_prompt.pack()

        self.entry = tk.Entry(self.window)
        self.entry.pack(ipadx=5, padx=5)
        self.entry.focus_set()

        enter = tk.Button(self.window, text="ENTER",command=self.add_to_ranking)
        enter.pack(pady=5)
    
    def into_json(self, data):
        #This is where the local ranking is dumped into json file
        with open("scores.txt","w") as json_file:
            json.dump(data, json_file)

    def add_to_ranking(self):
        with open('scores.txt') as json_file:
            ranking = json.load(json_file)
        items_played_with = ncards_entry.get()
        player_name = self.entry.get()
        if items_played_with in ranking.keys():                                  #check if anyone has played with this many items
            if player_name in ranking[items_played_with].keys():                 #check if this playre has a history score
                if game_iter <= ranking[items_played_with][player_name]:
                    ranking[items_played_with][player_name] = game_iter          #keep the lower move count under the player's name
            else:
                ranking[items_played_with][player_name] = game_iter
        else:
            ranking[items_played_with] = {player_name: game_iter}
        self.into_json(ranking)                                                  #stores the scores into json file
        self.window.destroy()                                                    #closes the pop up window prompt
        ncards_entry.focus_set()                                                 #sets cursor to the item number entry for next round

def show_ranking():
    with open('scores.txt') as json_file:
        ranking = json.load(json_file)
    items_played_with = ncards_entry.get()
    #if the user input is 0, show all the rankings present for all number of items played with
    if items_played_with == "0":
        show_all_ranking()
        return
    try:
        #put all history scores for this many items played with into a list ocnsisting of tuples
        #then sort this list in ascending order of move counts
        ranking_display = [[name, str(value)] for name, value in ranking[items_played_with].items()]
        sorted_ranking = sorted(ranking_display, key=itemgetter(1))
        print("Ranking with {} items\n".format(items_played_with))
        rank_num = 1
        for player in sorted_ranking:
            name, score = player
            print("{:<5}".format(rank_num), end='')             #print the rank number
            print("{:<15}".format(name), end = '')              #print the player's name
            print(score)                                        #print the player's score/move count
            rank_num += 1                                       #the rank number will increment by one after each player
        print("")
    #if the number entry does not exist in current ranking history, a message will be displayed to inform the player
    except KeyError:
        print("No one has played with this many items! \n"\
            "You could be a history maker!")
    finally:
        game.see(tk.END)

def show_all_ranking():
    with open('scores.txt') as json_file:
        ranking = json.load(json_file)
    #sort the number of items played with in ascending order
    nums_played_with = [x for x in ranking.keys()]
    nums_played_with.sort()
    print("\n" + "      HALL OF FAME")
    print('#'*25)
    for number in nums_played_with:
        ranking_display = [[name, str(value)] for name, value in ranking[number].items()]
        #sort the list in ascending order of move counts
        sorted_ranking = sorted(ranking_display, key=itemgetter(1))
        print("{}{} items".format(" "*8, number))
        rank_num = 1
        for player in sorted_ranking:
            name, score = player
            print("{:<5}".format(rank_num), end='')
            print("{:<15}".format(name), end = '')
            print(score)
            rank_num += 1
        print('#'*25)
    game.see(tk.END)

def new_game():
    global game_iter
    global real_game
    game_iter = 0
    from_pile_entry.focus_set()                         #set focus to (move from) entry box
    deal = []
    try:
        total_num = int(ncards_entry.get())             #gets user input of number of cards
        if total_num == 0:
            print("If you are trying to access the ranking, presse the RANKING button.\n")
            raise Exception
    except:
        print("Invalid input\nRefer to HELP for instructions.")
        ncards_entry.focus_set()
        return
    finally:
        game.see(tk.END)
    move_available = total_num*2                        #calculates total moves available
    move_available_label.config(text=move_available)    #shows moves availble on screen
    for i in range(1,total_num+1):
        deal.append(i)
    random.shuffle(deal)                                #shuffles cards 
    real_game = Solitaire(deal)
    print("**************************NEW GAME**************************")
    real_game.display()

def help_func():
    #display a message box with game instructions and rules
    rules = "This is a simplified version of the classic game of Solitaire.\n"\
        "\nYou can choose how many items (cards) you would like to play with by "\
        "entering a number in the top right corner.\n"\
            "\nPress on the RANKING button to view the ranking history of this particular number."\
                "Or enter in 0 and then press RANKING to view all ranking history.\n"\
            "\nThe aim of the game is to build up a stack of cards in descending order. "\
                "\nAfter you enter in the pile number, click 'START'.\n"\
                "\nPile 0 is your foundation pile, where only the top card is shown, "\
                "and the other piles are all empty to start with.\n"\
                    "\nAn empty pile can be filled with any card.\n"\
                    "\nFrom the foundation pile, you are allowed to move one card at a time.\n"\
                    "\nAll piles should be built down in descending order.\n"\
                    "\nYou can move stacks of a pile to another pile, "\
                    "if they are built down in order.\n"\
                        "\nIf you don't want to or cannot move a card to another pile from the foundation pile,"\
                        "you can place it at the bottom of the foundation pile by moving from pile 0 to pile 0.\n"\
                            
    tk.messagebox.showinfo("HELP", rules)

    pass

simple_solitaire = tk.Tk()
simple_solitaire.geometry("480x430+500+200")
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
from_pile_entry.bind("<Return>", Solitaire.check_c1)

to_pile_label = tk.Label(move_frame, text = "to pile no.")
to_pile_label.pack(side=LEFT)

to_pile_entry.pack(side=LEFT)
to_pile_entry.insert(0,' ')
#solitaire class gets input number 2 when 'enter' is pressed
to_pile_entry.bind("<Return>", Solitaire.check_c2)

game = tk.Text(game_frame)
game.pack(fill=X)

ranking_button = tk.Button(option_frame, text="RANKING",command=show_ranking)
ranking_button.pack(side=LEFT, ipadx=5, padx =8)

help_button = tk.Button(option_frame, text="HELP", command=help_func)
help_button.pack(side=LEFT, ipadx=5)

start_button = tk.Button(option_frame, text="START", command=new_game)
start_button.pack(side=RIGHT,ipadx=5, padx=8)

ncards_label2 = tk.Label(option_frame, text="items")
ncards_label2.pack(side=RIGHT)

ncards_entry = tk.Entry(option_frame, width=3)
ncards_entry.pack(side=RIGHT)
#set the focus on entry
ncards_entry.focus_set()

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