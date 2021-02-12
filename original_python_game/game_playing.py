#1280x720

from tkinter import Tk, Canvas, PhotoImage, Button, IntVar, Label
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.simpledialog import askstring
from time import sleep
from math import sin, cos, sqrt, exp
from random import choice
from pickle import dump, load


#my comments generally appear above what they are labeling (like a title)
#all images are drawn by me for the purpose of this game
#the leaderboard pickle file has .pkl
#if you find your leaderboard too crowded, in the folder there is a Clean New Leaderbaord For You To Copy And Rename To leaderboard.pkl ArithmeticError(dispose of the old one appropriately)
#save files from a game have .pickle

#functions and procedures

def circle_coordinator(c,r):
    #takes circle coordinates and radius, returns the coordinates for create_oval()
    x=c[0]
    y=c[1]
    left=x+640-r
    top=y+360-r
    right=x+640+r
    bottom=y+360+r
    return (left,top,right,bottom)

def tomator(score,playerpos):
    #makes odds and speed depending on the current score (clock)
    (odds,speed)=difficulty(score)
    #takes odds and gives a flavour
    flavour=choice(["aimed"]*odds[0] + ["plain"]*odds[1] + ["healing"]*odds[2])
    #create a tomato, give it a target
    if flavour=="aimed":
        #target's coordinates relative relative to centre
        trcx=playerpos[0]
        trcy=playerpos[1]
        theta2=choice(range(0,62832))/10000
    else:
        r=choice(range(0,280))
        theta=choice(range(0,62832))
        theta2=choice(range(theta+15708,theta+47124))
        theta=theta/10000
        theta2=theta2/10000
        trcx = cos(theta)*r
        trcy = sin(theta)*r

    target=[trcx,trcy]
    position=[cos(theta2)*310,sin(theta2)*310]

    return [flavour,target,position,speed]

def difficulty(score):
    #after about 50 seconds it reaches top speed
    speed=2.5-exp(-score/10000)
    if score%3000<500:
        #bonus round
        odds=(1,2,6)
    else:
        odds=(((score//5000)+1)*10,((score//5000)+1)*10,3)
    return (odds,speed)

def playGame(playerhp,clock,tomatos):
    global window
    global controls

    #prepare canvas
    canvas=Canvas(window,width="1280",height="720")
    canvas.pack()

    #detect key press. this method is invonvenient but is best in my opinion
    ki=IntVar()
    ki.set(-1)
    window.bind("<KeyPress>",lambda event:ki.set(event.keycode))

    #initiate player
    player_pic = canvas.create_oval(playerhp[1][0]+630,playerhp[1][1]+350, playerhp[1][0]+650,playerhp[1][1]+370, fill="#f" + hex(playerhp[0])[2] + hex(playerhp[0])[2])

    #prepare images
    clsm_pic=PhotoImage(file="coloseum_top_down.png")
    splat_green_pic=PhotoImage(file="splat_green.png")
    splat_red_pic=PhotoImage(file="splat_red.png")
    stocks_chart=PhotoImage(file="boss_image.png")

    game_stage=0

    #for the drawings of splatted tomatos that appear for just under half a second
    splatted_tomatos=[[],[],[],[],[],[],[],[],[],[],[]]
    
    while game_stage==0:
        #process input
        k=ki.get()
        if k == controls["up"]:
            #up
            playerhp[2][1]-=1
        elif k == controls["right"]:
            #right
            playerhp[2][0]+=1
        elif k == controls["down"]:
            #down
            playerhp[2][1]+=1
        elif k == controls["left"]:
            #left
            playerhp[2][0]-=1
        elif k == controls["pause"]:
            #pause
            game_stage=2
        elif k == controls["secret"]:
            #cheat by healing to full hp
            playerhp[0]=15
        elif k == controls["secret2"]:
            #cheat by turning the tomatos to healing
            for t in range(len(tomatos)):
                tomatos[t][0]="healing"
        elif k == -1:
            #no button was pressed
            pass
        else:
            #boss. Pressing the pause button next will go to the pause menu
            game_stage=1
        ki.set(-1)

        
        #throw a projectile every now and then with increasing frewuency
        if clock%400==0 or clock%360==0:
            for counter in range(4+clock//200):
                tomatos.append(tomator(clock,playerhp[1]))
        if clock%int(10+30*exp(-clock/1000))==0:
            tomatos.append(tomator(clock,playerhp[1]))

        sleep(0.005)
        clock+=1

        #clear canvas
        canvas.delete("all")

        #draw everything

        #draw background
        canvas.create_image(0,0,image=clsm_pic,anchor="nw")

        #scoreboard
        canvas.create_text(60,20,text="Score: "+str(clock//10)+"\nHit Points: "+str(playerhp[0])+"/15")

        #draw splatted tomatos
        for r in splatted_tomatos:
            for s in r:
                if s[0]=="healing":
                    splc=splat_green_pic
                else:
                    splc=splat_red_pic
                canvas.create_image(s[1][0]+640,s[1][1]+360,image=splc,anchor="c")
        splatted_tomatos = [[]]+splatted_tomatos[:-1]

        #process tomatos
        index=0
        while index<len(tomatos):
            flavour,target,position,speed=tomatos[index]

            #find unit vector for direction of travel for projectile
            dx=position[0]-target[0]
            dy=position[1]-target[1]
            sf=sqrt((dx**2)+(dy**2))
            position[0]-=dx*speed/sf
            position[1]-=dy*speed/sf


            #check if projectile hits player
            if ((position[0] - playerhp[1][0])**2 + (position[1] -playerhp[1][1])**2) < 400:
                if flavour=="healing":
                    if playerhp[0]!=15:
                        playerhp[0]+=1
                else:
                    playerhp[0]-=4
                    playerhp[2][0]=playerhp[2][0]*0.5
                    playerhp[2][1]=playerhp[2][1]*0.5
                del tomatos[index]
            elif sf < 3.0:
                #if the projectile has reached its target
                splatted_tomatos[0].append((flavour,position))
                del tomatos[index]
            else:
                index+=1
                #draw the tomato
                canvas.create_oval(circle_coordinator(target, 5), outline="#d19f17")
                if flavour=="healing":
                    canvas.create_oval(circle_coordinator(position,10), fill="green", outline="green")
                else:
                    canvas.create_oval(circle_coordinator(position,10), fill="red", outline="red")

        #check for collision with wall
        if ((playerhp[1][0]**2) + (playerhp[1][1]**2)) > 87000:
            #ricochet and change hitpoints
            playerhp[2][0]=-0.9*playerhp[2][0]
            playerhp[2][1]=-0.9*playerhp[2][1]
            playerhp[0]-=2
            
        #move player by veloocity times speed scale factor, "speed", which I have replaced with the number I liked most following testing
        playerhp[1][0]+=playerhp[2][0]*1.5
        playerhp[1][1]+=playerhp[2][1]*1.5

        #dampen velocity
        playerhp[2][0]=playerhp[2][0]*0.99
        playerhp[2][1]=playerhp[2][1]*0.99

        #check hit points
        if playerhp[0]<=0:
            #to avoid errors
            playerhp[0]=0
            game_stage=3
            break

        #draw player
        canvas.create_oval(circle_coordinator(playerhp[1],10), fill="#f" + hex(playerhp[0])[2] + hex(playerhp[0])[2])
        
        window.update()
    canvas.destroy()

    #if boss key is active
    if game_stage==1:
        window.title("Multi-Stochastic Analyses of Stock")
        bim=Label(window,image=stocks_chart)
        bim.pack()
        k=ki.get()
        while k != controls["pause"]:
            window.wait_variable(ki)
            k=ki.get()
        bim.destroy()
        window.title("Colosseum")
        game_stage=2

    #set label for pause menu
    pause_instructions = Label(window, font=(30), text="Resume: Press control for up dodge\nSave: Press control for right dodge\nEnd Game and Return to Main Menu: Press control for down dodge",)
    #if pause menu is active
    while game_stage==2:
        game_stage=4
        pause_instructions.pack()
        pause_choice=chooseKey()
        if pause_choice==controls["up"]:
            #resume game. from the top of this function
            pause_instructions.pack_forget()
            return playGame(playerhp,clock,tomatos)
        elif pause_choice==controls["right"]:
            #save game and return to pause menu
            game_stage=2
            save_file=asksaveasfile("wb",defaultextension=".pickle")
            dump((playerhp,clock,tomatos),save_file)
        elif pause_choice==controls["down"]:
            #it is equivalent to game over
            game_stage=3
        else:
            #pause menu stays up
            game_stage=2
        pause_instructions.pack_forget()

    #if game over occurs
    if game_stage==3:
        return (clock//10)
    

def chooseKey():
    #get the next key to be pressed and put it in kc
    kci=IntVar()
    window.bind("<KeyPress>",lambda event:kci.set(event.keycode))
    window.wait_variable(kci)
    kc=kci.get()
    return kc

def mainMenu():
    #in case it is not clear already
    clearWindow()
    menu_image=PhotoImage(file="title_screen.png")
    imlabel=Label(window,image=menu_image)
    bs=[]
    bs.append(Label(window,font=("bold", 30),text="Main Menu"))
    bs.append(Button(window,text="New game",command=newGame))
    bs.append(Button(window,text="Resume saved game",command=resumeSavedGame))
    bs.append(Button(window,text="Leaderboard",command=showLeaderboard))
    bs.append(Button(window,text="Change controls",command=changeControls))
    bs.append(Button(window,text="Guide",command=guide))
    bs.append(Button(window,text="Quit",command=window.destroy))
    i=0
    for b in bs:
        b.grid(column=0,row=i)
        i+=1
    imlabel.grid(column=1,row=0,rowspan=7)
    window.mainloop()

def guide():
    clearWindow()
    title=Label(window,font=("bold",30),text="Guide")
    story=Label(window,text="The colosseum crow does not appreciate your voice and begin to hurl fruits at you. Can you dodge them?\nThe walls of the colosseum rebound you and deal damage to you.\nThe fruits include hurtful red tomatos and healing green apples.\nYou will be judged by how long you can survive.\nBy default use the arrow keys to dodge and Esc to pause on Windows.\nMost other buttons will give you the latest charts for market capitalisation co-linear regression.")
    back=Button(window,text="Main Menu",command=mainMenu)
    title.pack()
    story.pack()
    back.pack()

def clearWindow():
    deathrow=window.winfo_children()
    for inmate in deathrow:
        inmate.destroy()

def newGame():
    clearWindow()
    #playerhp contains their hit points, and position and veloocity relative to the centre of the colosseum
    start_playerhp = [15,[0,0],[0,0]]
    start_clock=0
    start_tomatos = []
    new_score=playGame(start_playerhp,start_clock,start_tomatos)
    game_over_image=PhotoImage(file="game_over.png")
    golabel=Label(window,image=game_over_image)
    golabel.pack()
    name=askstring("Enter name","Enter your name for the leaderboard")
    with open("leaderboard.pkl","rb") as f:
        lb_old=load(f)
    i=0
    while lb_old[i][0]>new_score:
        i+=1
    lb_new=lb_old[:i]+[(new_score,name)]+lb_old[i:]
    with open("leaderboard.pkl","wb") as f:
        dump(lb_new,f)
    mainMenu()
    
def resumeSavedGame():
    clearWindow()
    print("top tip: make sure the window with the game is active (you may have to do more than just click on it. pressing Alt Tab to the window should work)")
    save_file=askopenfile("rb",filetypes=[("*","*.pickle")])
    sst=load(save_file)
    new_score=playGame(*sst)
    game_over_image=PhotoImage(file="game_over.png")
    golabel=Label(window,image=game_over_image)
    golabel.pack()
    name=askstring("Enter name","Enter your name for the leaderboard")
    with open("leaderboard.pkl","rb") as f:
        lb_old=load(f)
    i=0
    while lb_old[i][0]>new_score:
        i+=1
    lb_new=lb_old[:i]+[(new_score,name)]+lb_old[i:]
    with open("leaderboard.pkl","wb") as f:
        dump(lb_new,f)
    mainMenu()

def showLeaderboard():
    clearWindow()
    with open("leaderboard.pkl","rb") as f:
        lb=load(f)
    title=Label(window,text="Leaderboard",font=("bold",30))
    title.pack()
    for i in range (len(lb)):
        try:
            textin=str(i+1)+". "+lb[i][1]+" scoring "+str(lb[i][0])
        except:
            textin=str(i+1)+". Anonymous scoring "+str(lb[i][0])
        entry=Label(window,text=textin,font=(20))
        entry.pack()
    backbutton=Button(window,text="back",command=mainMenu)
    backbutton.pack()

def customiseControls():
    clearWindow()
    #allows creation of a new controls set
    custom_controls={"secret":67, "secret2":78}
    l=Label(window,font=(30), text="press key for up dodge")
    l.pack()
    custom_controls["up"]=chooseKey()
    l.destroy()
    l=Label(window,font=(30), text="press key for right dodge")
    l.pack()
    custom_controls["right"]=chooseKey()
    l.destroy()
    l=Label(window,font=(30), text="press key for down dodge")
    l.pack()
    custom_controls["down"]=chooseKey()
    l.destroy()
    l=Label(window,font=(30), text="press key for left dodge")
    l.pack()
    custom_controls["left"]=chooseKey()
    l.destroy()
    l=Label(window,font=(30), text="press key for pause")
    l.pack()
    custom_controls["pause"]=chooseKey()
    l.destroy()
    return custom_controls
    
def changeControls():
    clearWindow()
    #allows switching between control sets
    #on windows the default cheat keys are c and n
    #on linux mint, finding them is left as an exercise to the reader
    #all other keys are for the boss
    mint_controls={"up":111, "right":114, "down":116, "left":113, "pause":9, "secret":67, "secret2":78}
    windows_controls={"up":38,"right":39,"down":40,"left":37, "pause":27, "secret":67, "secret2":78}
    contschoice=IntVar(window,value=3)
    bs=[]
    bs.append(Label(window, font=(30), text="Choose controls"))
    bs.append(Button(window,text="windows default", command = lambda: contschoice.set(0)))
    bs.append(Button(window,text="linux mint default", command = lambda: contschoice.set(1)))
    bs.append(Button(window,text="custom", command = lambda: contschoice.set(2)))
    for b in bs:
        b.pack()
    window.wait_variable(contschoice)
    cr=contschoice.get()
    global controls
    if cr == 0:
        controls=windows_controls
    elif cr == 1:
        controls=mint_controls
    elif cr == 2:
        controls=customiseControls()
    for i in range(len(bs)):
        bs[i].destroy()
    mainMenu()
    
#prepare window
window = Tk()
window.title("Colosseum")
window.geometry("1280x720")
window.configure(bg="beige")

#set default controls
#on windows the default cheat keys are c and n
#on linux mint, finding them is left as an exercise to the reader
#all other keys are for the boss
controls={"up":38,"right":39,"down":40,"left":37, "pause":27, "secret":67, "secret2":78}

mainMenu()
