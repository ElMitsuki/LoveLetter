from tkinter import *
from mttkinter import mtTkinter
import time

class Renderer:

    """
        GUI interface
    """

    def __init__(self,q):
        self.__window=Tk()
        self.__centerWindow(self.__window,500,100)
        self.__scrollbar = Scrollbar(self.__window, width = 32)
        self.__canvas=Canvas(self.__window,width=self.__window.winfo_screenwidth(), height=self.__window.winfo_screenheight(), scrollregion=(0, 0, 1000, 1000), yscrollcommand = self.__scrollbar.set)
        self.__imgs={
            "back":PhotoImage(file="interface/cards/back.png"),
            "Guard":PhotoImage(file="interface/cards/guard.png"),
            "Priest":PhotoImage(file="interface/cards/priest.png"),
            "Baron":PhotoImage(file="interface/cards/baron.png"),
            "Handmaid":PhotoImage(file="interface/cards/handmaid.png"),
            "Prince":PhotoImage(file="interface/cards/prince.png"),
            "King":PhotoImage(file="interface/cards/king.png"),
            "Countess":PhotoImage(file="interface/cards/countess.png"),
            "Princess":PhotoImage(file="interface/cards/princess.png"),
        }
        self.__canvas_items={}
        self.__q=q
        self.__simuMod = False
        self.__oneSide = False
    
    def getWindow(self):
        return self.__window

    def getOneSide(self):
        return self.__oneSide
    def setOneSide(self, new_bool):
        self.__oneSide = new_bool

    def getSimuMod(self):
        return self.__simuMod

    def __centerWindow(self, window, width, height):
        """Automatically centres the window

        window = window to center
        width = width of the window
        height = height of the window
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def __genImg(self,item,name,x,y,coeff=0,offset=138):
        """Genereates an image on canvas

        item = name of the item
        name = name of the card
        x = pos x
        y = pos y
        coeff = coefficient
        offset = offset on x
        """
        self.__canvas_items[item]=self.__canvas.create_image(x+offset*coeff, y,anchor = NW, image=self.__imgs[name])

    def __writeTxt(self, item, text, x, y):
        """Writes a text on canvas

        item = name of the item
        text = text to write
        x = pos x
        y = pos y
        """
        self.__canvas_items[item]=self.__canvas.create_text(x,y,anchor = NW, text=text)

    def __updateDisplay(self):
        """Updates display of the window

        """
        self.__canvas.pack()
        self.__scrollbar.config( command = self.__canvas.yview )
        self.__window.update()

    def playersNames(self):
        """Generates input and label widgets and starts autoloop
        """
        player_num = 1
        names=[]
        AI_anwsers=[]
        versions_awnsers = []
        paned_windows = []
        while player_num < 3:
            paned_windows.append(PanedWindow(self.__window, orient=VERTICAL))
            names.append(StringVar(value="")) 
            AI_anwsers.append(IntVar(value=0))
            versions_awnsers.append(IntVar(value=0))
            paned_windows[player_num-1].add(Label(self.__window, text="Name Player {} :".format(player_num)))
            paned_windows[player_num-1].add(Entry(self.__window, textvariable=names[player_num-1], width=50))
            p=PanedWindow(self.__window, orient=HORIZONTAL)
            p.add(Label(self.__window, text="Player {} is an AI ? :".format(player_num)))
            p.add(Radiobutton(self.__window, text="Yes", variable=AI_anwsers[player_num-1], value=1, command=lambda: self.__updatePlayersNames(paned_windows, AI_anwsers, versions_awnsers)))
            p.add(Radiobutton(self.__window, text="No", variable=AI_anwsers[player_num-1], value=0, command=lambda: self.__updatePlayersNames(paned_windows, AI_anwsers, versions_awnsers)))
            paned_windows[player_num-1].add(p)
            paned_windows[player_num-1].pack()
            player_num+=1


        Button(self.__window, text="Valider", command= lambda:self.__q.put([[names[0].get(),AI_anwsers[0].get(),versions_awnsers[0].get()],[names[1].get(),AI_anwsers[1].get(),versions_awnsers[1].get()]])).pack()
        self.__scrollbar.pack(side = RIGHT, fill = Y)
        self.__window.mainloop()

    def __updatePlayersNames(self, paned_windows, AI_anwsers, versions_awnsers):
        """
        docstring
        """
        i = 0
        for paned_window in paned_windows:
            add = True
            for child in paned_window.panes():
                add = False if getattr(self.__window.nametowidget(child), "name", None) == "version" and add else add
            if AI_anwsers[i].get() == 1 and add:
                p=PanedWindow(self.__window, orient=HORIZONTAL)
                p.name="version"
                p.add(Label(self.__window, text="AI version ? :"))
                p.add(Radiobutton(self.__window, text="V3", variable=versions_awnsers[i], value=1))
                p.add(Radiobutton(self.__window, text="V1", variable=versions_awnsers[i], value=0))
                paned_window.add(p)
                paned_window.pack()
            i+=1
        self.__window.update()

    def askNbSimu(self):
        for item in self.__window.winfo_children():
            if item.winfo_class() != "Canvas":
                item.destroy()
        self.__simuMod = True
        Label(self.__window, text="Number of simulations :").pack()
        spin = Spinbox(self.__window, from_=1, to=1000000)
        spin.pack()
        Button(self.__window, text="Valider", command= lambda:self.__q.put(spin.get())).pack()
        self.__window.update()

    def initRound(self, draw, discard, players):
        """Generates the display when the round is initialised

        draw = pile of cards
        discard = all cards discarded
        """
        self.__centerWindow(self.__window, self.__window.winfo_screenwidth(), self.__window.winfo_screenheight())
        for item in self.__window.winfo_children():
            if item.winfo_class() != "Canvas" and item.winfo_class() != "Scrollbar":
                item.destroy()
        for key, item_id in self.__canvas_items.items():
            self.__canvas.delete(item_id)
        self.__writeTxt("turn","Au tour de :", 580, 400)
        self.__writeTxt("current_player", "", 645,400)
        self.__writeTxt("score-{}".format(players[0].getId()),"Score de {} : {}".format(players[0].getName(),players[0].getScore()),580,415)
        self.__writeTxt("score-{}".format(players[1].getId()),"Score de {} : {}".format(players[1].getName(),players[1].getScore()),580,430)
        self.__genImg("draw","back",0,358)
        i=0
        for card in discard:
            self.__genImg("discard-{}".format(i),card.getName(),138,358,i)
            i+=1
        self.__updateDisplay()

    def draw(self, player_id, card_name, num, hide):
        """draws the drawn card

        player_id = id of the current player
        card_name = name of the drawn card
        num = num of the card
        hide = card must be hide or not
        """
        self.__genImg("player{}-card-{}".format(player_id,num), card_name, 0, 716 if not hide else 0, num)

    def chooseCard(self,player):
        """Add click event on hand card

        player = current player
        """
        i=0
        for card in player.getHand():
            self.__canvas.tag_bind(self.__canvas_items["player{}-card-{}".format(player.getId(),i)],"<Button-1>",lambda event:self.findIndexCard(event.widget.find_closest(event.x, event.y), player.getId(), len(player.getHand())))
            i+=1

    def findIndexCard(self, item_id_choose, player_id, hand_length):
        """Finds position of a card in a player hand from the id of the canvas item

        item_id_choose = item has launched event
        player_id = current player id
        """
        self.__canvas.tag_unbind(self.__canvas_items["player{}-card-0".format(player_id)],"<Button-1>")
        self.__canvas.tag_unbind(self.__canvas_items["player{}-card-1".format(player_id)],"<Button-1>")
        card_index=""
        for key, item_id in self.__canvas_items.items():
            if item_id == item_id_choose[0]:
                card_index=int(key.split("-")[2])
                self.__q.join()
                self.__q.put(card_index)
        self.removeCardHand(player_id,card_index, hand_length)
        self.__updateDisplay()

    def removeCardHand(self, player_id, card_index, hand_length):
        """Removes a card from a player hand

        player_id=current player id
        card_index=index of a selected card
        hand_length=length of player hand
        """
        self.__canvas.delete(self.__canvas_items["player{}-card-{}".format(player_id,card_index)])
        temp=""
        if card_index==0:
            temp=self.__canvas_items["player{}-card-0".format(player_id)]
        if temp != "" and hand_length > 0 :
            self.__canvas_items["player{}-card-0".format(player_id)]=self.__canvas_items["player{}-card-1".format(player_id)]
            self.__canvas_items["player{}-card-1".format(player_id)]=temp
            self.__canvas.move(self.__canvas_items["player{}-card-0".format(player_id)],-138,0)

    def updateDiscard(self, card_name, player_id, card_index, y=537):
        """Updates the discard of a player

        card_name = name of discarded card
        player_id = current player id
        card_index= index of card
        """
        self.__genImg("player{}-discard-{}".format(player_id,card_index), card_name, 0, y, card_index, 50)
        self.__updateDisplay()
        
    def initTurn(self,players,current_player,draw):
        """Init display for new turn

        players = list of player
        current_player = the current player
        """
        if self.__oneSide:
            for player in players:
                i=0
                for card in player.getHand():
                    if callable(getattr(player, "getSpecial", None)):
                        self.__canvas.itemconfigure(self.__canvas_items["player{}-card-{}".format(player.getId(),i)],image=self.__imgs["back"])
                    else:
                        self.__canvas.itemconfigure(self.__canvas_items["player{}-card-{}".format(player.getId(),i)],image=self.__imgs[card.getName()])
                    i+=1
                i=0
                for card in player.getDiscard():
                    self.__canvas.itemconfigure(self.__canvas_items["player{}-discard-{}".format(player.getId(),i)],image=self.__imgs[card.getName()])
                    i+=1
        else:
            for player in players:
                i=0
                for card in player.getHand():
                    if current_player.getId() == player.getId():
                        self.__canvas.itemconfigure(self.__canvas_items["player{}-card-{}".format(player.getId(),i)],image=self.__imgs["back"])
                        self.__canvas.move(self.__canvas_items["player{}-card-{}".format(player.getId(),i)],0,-716)
                    else:
                        self.__canvas.itemconfigure(self.__canvas_items["player{}-card-{}".format(player.getId(),i)],image=self.__imgs[card.getName()])
                        self.__canvas.move(self.__canvas_items["player{}-card-{}".format(player.getId(),i)],0,716)
                    i+=1
                i=0
                for card in player.getDiscard():
                    if current_player.getId() == player.getId():
                        self.__canvas.itemconfigure(self.__canvas_items["player{}-discard-{}".format(player.getId(),i)],image=self.__imgs[card.getName()])
                        self.__canvas.move(self.__canvas_items["player{}-discard-{}".format(player.getId(),i)],0,-358)
                    else :
                        self.__canvas.itemconfigure(self.__canvas_items["player{}-discard-{}".format(player.getId(),i)],image=self.__imgs[card.getName()])
                        self.__canvas.move(self.__canvas_items["player{}-discard-{}".format(player.getId(),i)],0,358)
                    i+=1
        if len(draw) == 0:
            self.__canvas.itemconfigure(self.__canvas_items["draw"],image="")
        self.__updateDisplay()

    def swapPlayer(self, player_name):
        """Changes text of current_player item

        player_name= name of current player
        """
        self.__canvas.itemconfigure(self.__canvas_items["current_player"], text=player_name)
        self.__updateDisplay()

    def __popup(self, title, func, timer=0):
        """Generates a popup

        title = title of the popup
        func = function that generates elements to be displayed
        timer = close window timer
        """
        popup = Toplevel()
        self.__centerWindow(popup, 700, 100)
        popup.title(title)
        if timer != 0 :
            popup.after(5000, popup.destroy)
        time.sleep(0.2)
        func(popup)
        popup.transient(self.__window)
        popup.grab_set()
        self.__window.wait_window(popup)

    def askCard(self):
        """Generates a popup that ask for guard
        """
        buttons = lambda popup:[
                Label(popup,text="Choose a card").pack(),
                list(map(
                    lambda buttons:Button(popup,text=buttons, command = lambda : self.__awnserCard(buttons,popup)).pack(side=LEFT, padx=10)if buttons != "back" and buttons != "Guard" else "",
                    self.__imgs
                ))
        ]
        self.__popup("Card choice", buttons)
        

    def __awnserCard(self, choosed_name, popup):
        """Callback of an event triggered by choosing a card in askCard

        choosed_name = name choosed by the user
        popup = popup
        """
        card_num={
            "Priest":2,
            "Baron":3,
            "Handmaid":4,
            "Prince":5,
            "King":6,
            "Countess":7,
            "Princess":8,
        }
        popup.destroy()
        self.__q.put(card_num[choosed_name])

    def displayMessage(self,texts):
        """Generates a popup that displays a message

        texts = list of text to display
        """
        if not self.__simuMod:
            labels = lambda popup :[
                list(
                    map(lambda labels: Label(popup,text=labels).pack(),
                        texts
                    )
                ),
                Button(popup,text="Quit",command = popup.destroy).pack()
            ]
            self.__popup("Message",labels,5000)

    def askPlayer(self, players):
        """Generates a popup that ask a player name

        players = list of players
        """
        self.__q.join()
        index = lambda popup:[
            Label(popup,text="Choose a player").pack(),
            list(
                map(
                    lambda index: Button(popup,text=players[index].getName(),command= lambda :self.__awnserPlayer(index,popup)).pack(side=LEFT, padx=10),
                    [0,1]
                )
            )
        ]
        self.__popup("Choose a player",index)

    def __awnserPlayer(self, choosed_player, popup):
        """Callback of an event triggered by choosing a player in askPlayer

        choosed_player = player index choosed by the user
        popup = popup
        """
        self.__q.put(choosed_player)
        popup.destroy()

    def showNbSimu(self, nb_simulation):
        """
        """
        for item in self.__window.winfo_children():
            if item.winfo_class() != "Canvas":
                item.destroy()
        Label(self.__window, text="Nb simulation rest : {}".format(nb_simulation)).pack()
        self.__window.update()

    def showCard(self,opponent_id,card_name):
        """Shows the hand of the opponent

        opponent_id = id of the oppoenent
        card_name = opponent card's name
        """
        self.__canvas.itemconfigure(self.__canvas_items["player{}-card-0".format(opponent_id)],image=self.__imgs[card_name])
        time.sleep(2)
        self.__canvas.itemconfigure(self.__canvas_items["player{}-card-0".format(opponent_id)],image=self.__imgs["back"])

    def end(self):
        """Destroy the window

        """
        time.sleep(3)
        self.__window.quit()