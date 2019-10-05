import tkinter as tk
from tkinter import ttk
from deque_class import Deque
#from solitaire_class import Solitaire

solitaire_game = tk.Tk()
solitaire_game.grid()
solitaire_game.title("SOLITARE 101")
solitaire_game.geometry("500x270+500+200")


#option buttons area
options_button_frame = tk.Frame(solitaire_game, height=20)
options_button_frame.pack()

#enter number items to play with
ncards_label1 = tk.Label(solitaire_game, text = \
    "Playing with:")
ncards_label1.grid(column=0, row=0)
entry_ncards = tk.Entry(solitaire_game)
entry_ncards.grid(column=1, row=0)
ncards_label2 = tk.Label(solitaire_game, text="items")
ncards_label2.grid(column=2, row=0)



solitaire_game.mainloop()