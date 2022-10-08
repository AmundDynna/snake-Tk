from cmath import nan
from tkinter import *
from random import randint
import time

root = Tk()
startKnapp = Button(root)
settingsButton = Button(root)
bekreftButton = Button(root)
food = Label(root)

maksMatLabel = Label(root)
windowsizeLabel = Label(root)
gridsizeLabel = Label(root)
updateTimeLabel = Label(root)

maksMatInput = Entry(root)
windowsizeInput = Entry(root)
gridsizeInput = Entry(root)
updateTimeInput = Entry(root)

windowsize = 500
gridsize = 12
updateTime =  100
maksMat = 3
middle = (int)((gridsize) / 2)
gridpx = (int)(windowsize / gridsize)

gameStart = False
xPos = []
yPos = []
xPosMat = []
yPosMat = []
snake = []
epler = []
bevegele = []
bevegele.append([0, 0])
poeng = 0
mat = 0
loss = False
settingsMenu = False
starttid = 0

root.geometry(str(windowsize) + "x" + str(windowsize))
root.title("Snake")

# Lager grid for root med lik str
for i in range(gridsize):
    root.columnconfigure(i, minsize=gridpx)

for i in range(gridsize):
    root.rowconfigure(i, minsize=gridpx)

def settings():
    global startKnapp, settingsButton, settingsMenu, bekreftButton, maksMatLabel, updateTimeLabel, gridsizeLabel, windowsizeLabel, maksMatInput, updateTimeInput, gridsizeInput, windowsizeInput
    settingsMenu = True
    startKnapp.destroy()
    settingsButton.destroy()
    bekreftButton = Button(root, text = "Bekreft", font=("Verdana", 14), command=confirmSettings)
    bekreftButton.grid(row=gridsize-1, column=0, columnspan=middle, sticky="nsew")

    # Lage 4 labels for hver setting
    maksMatLabel = Label(root, text="Maks Mat")
    maksMatLabel.grid(row=0, column=0, sticky="nsew")
    updateTimeLabel = Label(root, text="Oppdateringstid")
    updateTimeLabel.grid(row=0, column=1, sticky="nsew")
    gridsizeLabel = Label(root, text="Brettstørrelse")
    gridsizeLabel.grid(row=0, column=2, sticky="nsew")
    windowsizeLabel = Label(root, text="Vindustørrelse")
    windowsizeLabel.grid(row=0, column=3, sticky="nsew")

    # Lage 4 inputs for hver setting
    maksMatInput = Entry(root, font=("Verdana", 12), width=int(gridpx/4))
    maksMatInput.grid(row=1, column=0, sticky="nsew")
    updateTimeInput = Entry(root, font=("Verdana", 12), width=int(gridpx/4))
    updateTimeInput.grid(row=1, column=1, sticky="nsew")
    gridsizeInput = Entry(root, font=("Verdana", 12), width=int(gridpx/4))
    gridsizeInput.grid(row=1, column=2, sticky="nsew")
    windowsizeInput = Entry(root, font=("Verdana", 12), width=int(gridpx/4))
    windowsizeInput.grid(row=1, column=3, sticky="nsew")

def confirmSettings():
    global settingsButton, settingsMenu, bekreftButton, maksMatLabel, updateTimeLabel, gridsizeLabel, windowsizeLabel, maksMatInput, updateTimeInput, gridsizeInput, windowsizeInput, maksMat, updateTime, windowsize, gridsize, middle, gridpx
    settingsMenu = False
    bekreftButton.destroy()
    maksMatLabel.destroy()
    updateTimeLabel.destroy()
    gridsizeLabel.destroy()
    windowsizeLabel.destroy()
    # Skaffe data fra de fire innstillingene
    maksMatI = nan
    updateTimeI = nan
    gridsizeI = nan
    windowsizeI = nan
    try:
        maksMatI = int(maksMatInput.get())
    except:
        maksMatI = maksMat
    if maksMatI > 0 and maksMatI <= gridsize**2:
        maksMat = maksMatI
    
    try:
        updateTimeI = int(updateTimeInput.get())
    except:
        updateTimeI = updateTime
    if updateTimeI > 0:
        updateTime = updateTimeI

    try:
        gridsizeI = int(gridsizeInput.get())
    except:
        gridsizeI = gridsize
    if gridsizeI > 3 and gridsizeI <= windowsize:
        gridsize = gridsizeI

    try:
        windowsizeI = int(windowsizeInput.get())
    except:
        windowsizeI = windowsize
    if windowsizeI > gridsize and windowsizeI <= 1080:
        windowsize = windowsizeI

    maksMatInput.destroy()
    updateTimeInput.destroy()
    gridsizeInput.destroy()
    windowsizeInput.destroy()

    # Fikse innstillinger
    root.geometry(str(windowsize) + "x" + str(windowsize))
    middle = (int)((gridsize) / 2)
    gridpx = (int)(windowsize / gridsize)
    for i in range(gridsize):
        root.columnconfigure(i, minsize=gridpx)

    for i in range(gridsize):
        root.rowconfigure(i, minsize=gridpx)

    # Lage try funksjon for alle 4 innstillingene og hvis noen ikke virker går den tilbake til
    # forrige innstillinger
    menu()
    

def onKeyPress(event):
    if(gameStart == True):
        global bevegele
        if((event.char == 'w' or event.keycode == 38) and bevegele != [[0, 1]]):
            bevegele.append([0, -1])

        elif((event.char == 's' or event.keycode == 40) and bevegele != [[0, -1]]):
            bevegele.append([0, 1])

        elif((event.char == 'a' or event.keycode == 37) and bevegele != [[1, 0]]):
            bevegele.append([-1, 0])

        elif((event.char == 'd' or event.keycode == 39) and bevegele != [[-1, 0]]):
            bevegele.append([1, 0])


    elif(gameStart == False):
        if(settingsMenu == False):
            if(event.char == '\r'):
                start()


# Menu function
def menu():
    global gameStart, startKnapp, loss, settingsButton
    gameStart = False
    loss = False
    startKnapp = Button(root, text = "Start", font=("Verdana", 14), command=start)
    startKnapp.grid(row=middle, column=middle, sticky="nsew")
    settingsButton = Button(root, text = "Innstillinger", font=("Verdana", 14), command=settings)
    settingsButton.grid(row=0, column=0, columnspan=middle, sticky="nsew")

# Start 
def start():
    global startKnapp, xPos, yPos, gameStart, bevegele, poeng, mat, loss, starttid, settingsButton
    loss = False
    bevegele = []
    bevegele.append([0, 0])
    starttid = time.time()
    poeng = 0
    mat = 0
    gameStart = True
    xPos = [middle]
    yPos = [middle]
    startKnapp.destroy()
    settingsButton.destroy()
    nextFrame()

# Tegner eplene for hver frame

def drawFood():
    global xPosMat, yPosMat, epler
    for i in range(len(epler)):
        epler[i].destroy()
    for i in range(len(xPosMat)):
        epler.append(Label(root, bg="red", font=("Verdana", 1)))
        epler[-1].grid(row=yPosMat[i], column=xPosMat[i], sticky="nsew")

# Lager posisjonene til eplene
def makeFood():
    global xPos, yPos, xPosMat, yPosMat, epler, loss, mat
    fantMat = False
    rad = nan
    kolonne = nan
    tries = 0
    while fantMat == False:
        if tries > 5000:
            mat = maksMat
            fantMat = True
        testArr = []
        rad = randint(0, gridsize - 1)
        kolonne = randint(0, gridsize - 1)
        for i in range(len(xPos)):
            if (xPos[i - 1] == kolonne) and (yPos[i - 1] == rad):
                testArr.append(False)
        if xPosMat != []:
            for i in range(len(xPosMat)):
                if xPosMat[i] == kolonne and yPosMat[i] == rad:
                    testArr.append(False)
        tries += 1
        if testArr == []:
            fantMat = True
    xPosMat.append(kolonne)
    yPosMat.append(rad)



def drawSnake():
    # lag array av labels
    global xPos, yPos, snake
    lengde = len(xPos)
    sLen = len(snake)

    # Sletter forige slange
    for i in range(sLen):
        snake[i].destroy()
    snake = []

    # Tegner ny slange fra xPos og yPos
    for i in range(lengde):
        kolonne = xPos[i]
        rad = yPos[i]
        if(kolonne < 0 or rad < 0):
            break
        snake.append(Label(root, bg="green", relief="solid", font=("Verdana", 1)))
        snake[i].grid(row=rad, column=kolonne, sticky="nsew")


# lage function som legger inn bevegelse i array
def snakePosition():
    global xPos, yPos, bevegele, xPosMat, yPosMat, mat, poeng, food, gameStart, epler, loss, starttid
    if xPos != []:
        if len(bevegele) > 1:
            bevegele.pop(0)
        sisteX = xPos[-1]
        nyPosX = sisteX + bevegele[0][0]
        sisteY = yPos[-1]
        nyPosY = sisteY + bevegele[0][1]

        if(nyPosX < 0 or nyPosX >= gridsize):
            loss = True
        elif(nyPosY < 0 or nyPosY >= gridsize):
            loss = True
        
        try:
            if gameStart == True:
                if bevegele != [[0, 0]]:
                    for t in range(len(xPos)):
                        if xPos[t] == nyPosX and yPos[t] == nyPosY:
                            lostGame()
                            gameStart = False
        except:
            if gameStart == True:
                loss = True
                gameStart = False

        xPos.append(nyPosX)
        yPos.append(nyPosY)



        # Funksjon på når slangen spiser mat
        fjern = False
        for i in range(len(xPosMat)):
            if nyPosX == xPosMat[i-1] and nyPosY == yPosMat[i-1]:
                xPosMat.pop(i-1)
                yPosMat.pop(i-1)
                epler[i- 1].destroy()
                epler.pop(i- 1)
                mat -= 1
                poeng += 1
                fjern = True
        root.title("Snake      Poeng: " + str(poeng) + "       Tid: " + str(int(time.time() - starttid)))  
        if fjern == False:
            xPos.pop(0)
            yPos.pop(0)
        # Funksjon for å sjekke om slangen kræsjer med seg selv
        

def nextFrame():
    global mat, gameStart, loss
    while mat < maksMat:
        makeFood()
        mat += 1
    drawFood()
    snakePosition()
    drawSnake()
    if gameStart == True:
        root.after(updateTime, nextFrame)
    if loss == True:
        lostGame()
    

def lostGame():
    global snake, food, xPos, yPos, bevegele, gameStart, xPosMat, yPosMat, epler
    gameStart = False
    xPos = []
    yPos = []
    bevegele = []
    bevegele.append([0, 0])
    xPosMat = []
    yPosMat = []
    sLen = len(snake)
    for i in range(sLen):
        snake[i].destroy()
    for i in range(len(epler)):
        epler[i].destroy()
    snake = []
    epler = []
    food.destroy()
    menu()

menu()
root.bind('<KeyPress>', onKeyPress)
root.mainloop()