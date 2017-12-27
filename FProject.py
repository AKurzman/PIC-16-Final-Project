import numpy as np
from tkinter import *
from random import randint

def floodit(d):    #initializes a game with a given difficulty 'd'; 'easy','medium',or 'hard'
    global movetracker #global variable movetracker that keeps track of moves made
    movetracker=0
    
    #this funciton determines the number of moves to beat or match
    def determinemoves(n,tracker,gcolor):
        #initializes variable to keep local track of moves and copies of the tracker and colors
        movecounter=0
        tr=tracker.copy()
        gc=gcolor.copy()
        finished=False
        while finished !=True:
            #sets finished to true with every move but is changed at the end if a zero is detect
            finished=True
            #represents each possible adjacent color
            count=[0,0,0,0,0,0]
            most=0
            #runs through a for loop of every potential color
            for c in range(len(count)):
                tt=tr.copy() #local copy of tracker copy to be tested
                for i in range(len(tt)):
                    for j in range(len(tt)):
                        #tests all four directions; if tracker is active on a square
                        #and adjacent=c and tracker is not active, it will add one
                        #to respective index of count
                        if tt[i][j]==1:
                            if i!=(len(tt)-1):
                                if gc[i+1][j]==c:
                                    if tt[i+1][j]==0:
                                        count[c]+=1
                                    tt[i+1][j]=1
                            if j!=(len(tt)-1):
                                if gc[i][j+1]==c:
                                    if tt[i][j+1]==0:
                                        count[c]+=1
                                    tt[i][j+1]=1
                            if i!=(0):
                                if gc[i-1][j]==c:
                                    if tt[i-1][j]==0:
                                        count[c]+=1
                                    tt[i-1][j]=1
                            if j!=(0):
                                if gc[i][j-1]==c:
                                    if tt[i][j-1]==0:
                                        count[c]+=1
                                    tt[i][j-1]=1
                #determines the maximum value in count, i.e. maximum adjacent color
                if count[c]>most:
                    most=count[c]
                    trcopy=tt.copy() #creates new copy to be assigned
                    mcolor=c
            #sets all active squares to said color and changes finished to False if there
            #is an inactive square
            for i in range(len(tt)):
                for j in range(len(tt)):
                    if tr[i][j]==1:
                        gc[i][j]=mcolor
                    if tr[i][j]==0:
                        finished=False
            tr=trcopy #replaces original copy with the new copy to complete the cycle
            movecounter+=1 #adds a move to local movecounter
        return movecounter
                        
        
    #function used by all colored buttons to fill and activate accordingly
    def bfill(c,tracker,gcolor,n,colors):
        m=(500/n) #represents one box increment
        allotedmoves.delete(1.0,'end') #deletes top of scoreboard to be updated
        global movetracker #uses global movetracker
        if movetracker<movemax: #executed if moves made by player is less than alloted moves by algorithm
            #fills all previously activated squares to color of button
            for i in range(0,len(tracker)):
                for j in range(0,len(tracker)):
                    if tracker[i][j]==1:
                        w.create_rectangle(i*m,j*m,(i+1)*m,(j+1)*m, fill=colors[c])
            #tests all adjacents to original activated area.   If they are the same color they
            #are activated so next move they will be part of the group that is filled as well
            for i in range(0,len(tracker)):
                for j in range(0,len(tracker)):
                    if tracker[i][j]==1:
                        if i!=(len(tracker)-1):
                            if gcolor[i+1][j]==c:
                                tracker[i+1][j]=1
                        if j!=(len(tracker)-1):
                            if gcolor[i][j+1]==c:
                                tracker[i][j+1]=1
                        if i!=(0):
                            if gcolor[i-1][j]==c:
                                tracker[i-1][j]=1
                        if j!=(0):
                            if gcolor[i][j-1]==c:
                                tracker[i][j-1]=1
            #changes all values in the color tracking array of activated squares to make sure 
            #they match the move made
            for i in range(len(tracker)):
                for j in range(len(tracker)):
                    if tracker[i][j]==1:
                        gcolor[i][j]=c
        movetracker+=1 #adds one move
        #if your moves are less than max allowed and there is no 0 in tracker: YOU WIN!!
        #checks win before loss because if you win on the final allowed move it is still a win
        if movetracker<=movemax and 0 not in tracker:
            allotedmoves.insert('end','YOU\nWIN!!')
            movetracker-=1
        #if your moves are greater than or equal to max moves: YOU LOSE!!
        elif movetracker>=movemax:
            allotedmoves.insert('end','YOU\nLOSE!!')
            return
        else: #updates scoreboard to reflect movetracker
            scorebox='Moves:\n'+str(movetracker)+' / '+str(movemax)
            allotedmoves.insert('end',scorebox)
    
    def newgame(d): #function used by restart button.  Closes the old canvas and initializes a new
        master.destroy()          #instance of the floodit game with same difficulty
        floodit(d)
        
                    
    #if not valid input, returns and requests a valid difficulty setting    
    if d!='easy' and d!='Easy' and d!='medium' and d!='Medium' and d!='hard' and d!='Hard':
        print('Please enter a valid difficulty (Easy/Medium/Hard)')
        return
    #if difficulty is chosen as 'easy': inintializes an 8x8 board with 4 colors
    if d=='easy' or d=='Easy':
        colors=['orange','green','blue','red']
        tracker=np.zeros((8,8)) #tracker is the main array used to keep track of activated squares
        tracker[0][0]=1  #top left is activated since it is the starting point of the game
        gcolor=np.zeros((8,8))  #will hold an integer 0-3 representing which color that square holds
        master = Tk()
        w = Canvas(master, width=500, height=600)  #new canvas with 100 spare pixels at bottom to house buttons
        w.pack()
        w.create_rectangle(0,0,500,500) #500x500 board
        k=500/(8)
        #creates the nxn board
        for i in range(0,7):
            w.create_line(0,k,500,k)
            k+=500/(8)
        l=500/(8)
        for j in range(0,7):
            w.create_line(l,0,l,500)
            l+=500/(8)
        m=500/(8)
        #this fills the board with colors
        for i in range(8):
            for j in range(8):
                if i==0 and j==0: #the top left square always is initialized as color '0', aka orange
                    temp=0
                    gcolor[i][j]=temp
                elif (i==0 and j==1)or(i==1 and j==0): #the two adjacent sqaures to top left are initialized as anything but orange
                    temp=int(randint(1,3))
                    gcolor[i][j]=temp
                else:
                    temp=int(randint(0,3)) #every other square is filled randomly
                    gcolor[i][j]=temp
        for i in range(8):  #fills the empty game squares according to their color
            for j in range(8):
                a=int(gcolor[i][j])
                w.create_rectangle(i*m,j*m,(i+1)*m,(j+1)*m, fill=colors[a])
        movemax=determinemoves(8,tracker,gcolor)  #movemax=total allowed moves
        allotedmoves=Text(master,width=8,height=2) #text box set on bottom left
        allotedmoves.pack(anchor='s',side='left',expand=True)
        #creates buttons and packs them at bottom from l to r
        #each one represents a different color and has fill function as command
        b1=Button(master,bg='orange',width=8,command=lambda:bfill(0,tracker,gcolor,8,colors))
        b2=Button(master,bg='green',width=8,command=lambda:bfill(1,tracker,gcolor,8,colors))
        b3=Button(master,bg='blue',width=8,command=lambda:bfill(2,tracker,gcolor,8,colors))
        b4=Button(master,bg='red',width=8,command=lambda:bfill(3,tracker,gcolor,8,colors))
        reset=Button(master,text='RESTART',width=7,command=lambda:newgame(d)) #rigged to restart function
        b1.pack(anchor='s',side='left',expand=True)
        b2.pack(anchor='s',side='left',expand=True)
        b3.pack(anchor='s',side='left',expand=True)
        b4.pack(anchor='s',side='left',expand=True)
        reset.pack(anchor='s',side='left',expand=True)
        #sets up scoreboard with an initial 0/allowed moves
        scorebox='Moves:\n'+'0 / '+str(movemax)
        allotedmoves.insert('end',scorebox)
        mainloop()
    #initializes a medium difficulty version of the game; 10x10 board with 5 colors
    if d=='medium' or d=='Medium':
        colors=['orange','green','blue','red','purple']
        gcolor=np.zeros((10,10))
        master = Tk()
        w = Canvas(master, width=500, height=600)
        w.pack()
        tracker=np.zeros((10,10))
        tracker[0][0]=1
        w.create_rectangle(0,0,500,500)
        k=500/(10)
        for i in range(0,9):
            w.create_line(0,k,500,k)
            k+=500/(10)
        l=500/(10)
        for j in range(0,9):
            w.create_line(l,0,l,500)
            l+=500/(10)
        m=500/(10)
        for i in range(10):
            for j in range(10):
                if i==0 and j==0:
                    temp=0
                    gcolor[i][j]=temp
                elif (i==0 and j==1)or(i==1 and j==0):
                    temp=int(randint(1,4))
                    gcolor[i][j]=temp
                else:
                    temp=int(randint(0,4))
                    gcolor[i][j]=temp
        for i in range(10):
            for j in range(10):
                a=int(gcolor[i][j])
                w.create_rectangle(i*m,j*m,(i+1)*m,(j+1)*m, fill=colors[a])
        movemax=determinemoves(8,tracker,gcolor)
        allotedmoves=Text(master,width=8,height=2)
        allotedmoves.pack(anchor='s',side='left',expand=True)
        b1=Button(master,bg='orange',width=7,command=lambda:bfill(0,tracker,gcolor,10,colors))
        b2=Button(master,bg='green',width=7,command=lambda:bfill(1,tracker,gcolor,10,colors))
        b3=Button(master,bg='blue',width=7,command=lambda:bfill(2,tracker,gcolor,10,colors))
        b4=Button(master,bg='red',width=7,command=lambda:bfill(3,tracker,gcolor,10,colors))
        b5=Button(master,bg='purple',width=7,command=lambda:bfill(4,tracker,gcolor,10,colors))
        reset=Button(master,text='RESTART',width=7,command=lambda:newgame(d))
        b1.pack(anchor='s',side='left',expand=True)
        b2.pack(anchor='s',side='left',expand=True)
        b3.pack(anchor='s',side='left',expand=True)
        b4.pack(anchor='s',side='left',expand=True)
        b5.pack(anchor='s',side='left',expand=True)
        reset.pack(anchor='s',side='left',expand=True)
        scorebox='Moves:\n'+'0 / '+str(movemax)
        allotedmoves.insert('end',scorebox)
        mainloop()
    #initializes a hard version of the game; 12x12 board with 6 colors (real dimensions of apps version)
    if d=='hard' or d=='Hard':
        colors=['orange','green','blue','red','purple','yellow']
        gcolor=np.zeros((12,12))
        tracker=np.zeros((12,12))
        tracker[0][0]=1
        master = Tk()
        w = Canvas(master, width=500, height=520)
        w.pack()
        w.create_rectangle(0,0,500,500)
        k=500/(12)
        for i in range(0,11):
            w.create_line(0,k,500,k)
            k+=500/(12)
        l=500/(12)
        for j in range(0,11):
            w.create_line(l,0,l,500)
            l+=500/(12)
        m=500/(12)
        for i in range(12):
            for j in range(12):
                if i==0 and j==0:
                    temp=0
                    gcolor[i][j]=temp
                elif (i==0 and j==1)or(i==1 and j==0):
                    temp=int(randint(1,5))
                    gcolor[i][j]=temp
                else:
                    temp=int(randint(0,5))
                    gcolor[i][j]=temp
        for i in range(12):
            for j in range(12):
                a=int(gcolor[i][j])
                w.create_rectangle(i*m,j*m,(i+1)*m,(j+1)*m, fill=colors[a])
        movemax=determinemoves(8,tracker,gcolor)
        allotedmoves=Text(master,width=8,height=2)
        allotedmoves.pack(anchor='s',side='left',expand=True)
        b1=Button(master,bg='orange',width=6,command=lambda:bfill(0,tracker,gcolor,12,colors))
        b2=Button(master,bg='green',width=6,command=lambda:bfill(1,tracker,gcolor,12,colors))
        b3=Button(master,bg='blue',width=6,command=lambda:bfill(2,tracker,gcolor,12,colors))
        b4=Button(master,bg='red',width=6,command=lambda:bfill(3,tracker,gcolor,12,colors))
        b5=Button(master,bg='purple',width=6,command=lambda:bfill(4,tracker,gcolor,12,colors))
        b6=Button(master,bg='yellow',width=6,command=lambda:bfill(5,tracker,gcolor,12,colors))
        reset=Button(master,text='RESTART',width=7,command=lambda:newgame(d))
        b1.pack(anchor='s',side='left',expand=True)
        b2.pack(anchor='s',side='left',expand=True)
        b3.pack(anchor='s',side='left',expand=True)
        b4.pack(anchor='s',side='left',expand=True)
        b5.pack(anchor='s',side='left',expand=True)
        b6.pack(anchor='s',side='left',expand=True)
        reset.pack(anchor='s',side='left',expand=True)
        scorebox='Moves:\n'+'0 / '+str(movemax)
        allotedmoves.insert('end',scorebox)
        mainloop()
