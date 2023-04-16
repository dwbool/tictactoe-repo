"""
Tic-tac-toe Game (based on: tkinter)
Author: Vladimir Bulychev
Email: dwbool@yahoo.com
Expert in: C++, C#, Delphi, T-SQL, PL/SQL
Project For: Python for Web development course
"""


from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import random

WBT:int = 40  # button width
X0:int = 20  # game field start
Y0:int = 20
ROW_LEN:int = 3  # cells in a row
lbl = 0 # message label (who won)

HUMAN_CHAR = 'X'   # human plays with this char
CPU_CHAR = '0'  # CPU uses this one

buttons:list = []  # game field cells

a2: list = []  # possible outcome of the nex move arrays:
a1: list = []
a0: list = []
threat :list =[]
win:list=[]



def row_col_index(row,col):
    return row * ROW_LEN + col


def possible_lines(row,col):
    res = 2
    n_already_horz = 0
    n_already_vert = 0
    n_human_horz = 0
    n_human_vert = 0
    found_human=0
    for i in range(0, ROW_LEN):
        index = row * ROW_LEN + i
        cur_text = buttons[index]['text']
        if cur_text == HUMAN_CHAR:
            n_human_horz += 1
            found_human=1
        elif cur_text == CPU_CHAR:
            n_already_horz+=1
    if found_human>0: res-=1
    found_human = 0
    for i in range(0, ROW_LEN):
        index = i * ROW_LEN + col
        cur_text = buttons[index]['text']
        if cur_text == HUMAN_CHAR:
            n_human_vert += 1
            found_human = 1
        elif cur_text == CPU_CHAR:
            n_already_vert+=1
    if found_human>0: res -= 1

    icur = row_col_index(row,col)
    if buttons[icur]['text']==CPU_CHAR : res=0  # wont allow to move here
    if buttons[icur]['text'] == HUMAN_CHAR: res = 0 # wont allow to move here
    return res,n_already_horz,n_already_vert , n_human_horz , n_human_vert


def choose_cpu_move():
    a2.clear()
    a1.clear()
    a0.clear()
    threat.clear()
    win.clear()
    for i in range(0, ROW_LEN*ROW_LEN):
        row = int(i / ROW_LEN)
        col = int(i % ROW_LEN)
        lin,n_already_horz,n_already_vert, n_human_horz , n_human_vert = possible_lines(row,col)
        if lin==2: a2.append(i) # this cell can be completed to both row and column (2 ways)
        elif lin==1: a1.append(i) # this cell can be completed to either row or column (1 way)
        if buttons[i]['text']=='': a0.append(i) # is empty
        if (n_human_horz>1 or n_human_vert>1) and buttons[i]['text']=='' : threat.append(i) # is a threat, CPU should put here
        if (n_already_horz > 1 or n_already_vert > 1) and buttons[i]['text'] == '': win.append(i) # moving here leads to a victory

    moved = 0
    won=0
    to_win = random.randint(0,1) # prevent CPU from winning, or else it will always do and the game will be too boring
    if len(a0)<=1: to_win =1
    if len(win)>0:
        if to_win==0  :

            for k in range(0,len(a0)):
                if not a0[k] in win:
                    b_ind = k
                    buttons[b_ind]['text'] = CPU_CHAR
                    moved = 1
                    print('PREVENTED CPU WINNING instead %d'%(b_ind)) # instead to some empty cell
                    break
            if moved==0:
                # could happen if only winning cells remained, so just use the first one
                b_ind = win[0]
                buttons[b_ind]['text'] = CPU_CHAR  # here CPU wins
                moved = 1
                won = 1


        else:
            r = random.randint(0,len(win)-1)
            b_ind = win[r]
            buttons[b_ind]['text']=CPU_CHAR  # here CPU wins
            moved = 1
            won=1
    elif len(threat)>0:
        r = random.randint(0,len(threat)-1)
        b_ind = threat[r]
        buttons[b_ind]['text']=CPU_CHAR  # avoiding threat from human player
        moved = 1
    elif len(a2)>0:
        r = random.randint(0,len(a2)-1)
        b_ind = a2[r]
        buttons[b_ind]['text']=CPU_CHAR # complete some 2 way possible cell
        moved = 1
    elif len(a1)>0:
        r = random.randint(0,len(a1)-1)
        b_ind = a1[r]
        buttons[b_ind]['text']=CPU_CHAR # complete some 1 way
        moved = 1
    elif len(a0)>0:
        r = random.randint(0, len(a0) - 1)
        b_ind = a0[r]
        buttons[b_ind]['text'] = CPU_CHAR # complete any empty
        moved = 1

    return moved,  won


def scan_human_won():
    # field button pressed
    for i in range(0, ROW_LEN ):
        found=1
        for k in range(0, ROW_LEN ):
            b_ind = i*ROW_LEN + k
            if buttons[b_ind]['text'] != HUMAN_CHAR:
                found=0
                break;
        if found>0: return 1;
    for i in range(0, ROW_LEN ):
        found=1
        for k in range(0, ROW_LEN ):
            b_ind = k*ROW_LEN + i
            if buttons[b_ind]['text'] != HUMAN_CHAR:
                found=0
                break;
        if found>0: return 1;
    return 0


def no_empty():
    for k in range(0, ROW_LEN*ROW_LEN):
        if buttons[k]['text'] == '':
            return 0
    return 1


def which_button(button_press):
    if lbl['text']!='':
        print('game is over already, press New Game')
        return
    row = int(button_press / ROW_LEN)
    col = int(button_press % ROW_LEN)
    print('btn index %d  row %d  col %d' % (button_press,row,col))
    cur_text = buttons[button_press]['text']
    hum_won = 0
    won=0
    moved=0
    if cur_text=='':
        buttons[button_press]['text'] = HUMAN_CHAR
        hum_won = scan_human_won()
    else:
        print("cannot move here")
        return
    if not hum_won:
        moved,won = choose_cpu_move()

    # output intrinsic structures for debug purposes:
    print("win "+str(win)) # winning cell array
    print("threat "+str(threat)) # threat cells
    print("a2 = row and col can be done "+str(a2))
    print("a1 = row or col can be done "+str(a1))
    print("a0 = any empty cell "+str(a0))
    print("moved "+str(moved)) # CPU did move actually

    # game results display:
    print('\r')
    if won>0 :
        print('CPU WON')
        lbl['text']='CPU WON'

    else:
        hum_won = hum_won>0 or scan_human_won()>0
        if hum_won:
            print('YOU WON')
            lbl['text'] = 'YOU WON'
        elif moved==0:
            print('DRAFT, you ended')
            lbl['text'] = 'DRAFT, you ended'
        else:
            if no_empty():
                print('DRAFT, CPU ended')
                lbl['text'] ='DRAFT, CPU ended'


def new_game(button_press):
    #https://pythonguides.com/python-tkinter-messagebox/
    res = messagebox.askquestion('askquestion', 'Do you want to start a new game?')
    if res == 'yes':
        pass
    elif res == 'no':
        return 1
    else:
        return 2

    for i in range(0, ROW_LEN * ROW_LEN):
        buttons[i]['text']=''

    if button_press==1 :
        # computer starts
        ind  = random.randint(0,ROW_LEN*ROW_LEN-1)
        buttons[ind]['text'] = CPU_CHAR

    lbl['text'] = ''
    return 0


ws = Tk()
ws.title("Tic-tac-toe")
ws.geometry('500x250')

# #https://pythonguides.com/python-tkinter-button/
# https://www.geeksforgeeks.org/how-to-check-which-button-was-clicked-in-tkinter/
# GAME field:
for i in range(0,ROW_LEN*ROW_LEN):
    b1 = Button(ws, text="", command=lambda m=i: which_button(m))
    b1.place(x= X0 + i*WBT % (WBT*ROW_LEN), y= Y0 + int(i*WBT / (WBT*ROW_LEN))*WBT, width=WBT , height=WBT)
    buttons.append(b1)

# restart control buttons
b1 = Button(ws, text="New Game, You Start (X)", command=lambda m=0: new_game(m))
b1.place(x= X0 + (WBT*ROW_LEN) + 50, y= Y0 , width=WBT*7 , height=WBT)
buttons.append(b1)

b1 = Button(ws, text="New Game, CPU Starts (0)", command=lambda m=1: new_game(m))
b1.place(x= X0 + (WBT*ROW_LEN) + 50, y= Y0 + WBT , width=WBT*7 , height=WBT)
buttons.append(b1)

#game result label:
#https://pythonguides.com/python-tkinter-label/
lbl = Label(ws, text="", font=("arial italic", 18) )
lbl.place(x= X0 + (WBT*ROW_LEN) + 50, y= Y0 + WBT*3 , width=WBT*7 , height=WBT)

ws.mainloop()


