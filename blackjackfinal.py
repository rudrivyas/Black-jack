# Mini-project - Blackjack

import simplegui
import random

# load card sprite - 949x392 (sprite of 13x4 images)
CARD_SIZE = (73,98)
CARD_CENTER = (36.5,49)
card_images = simplegui.load_image("d:\card.png")

CARD_BACK_SIZE = (71,96)
CARD_BACK_CENTER = (35.5,49)
card_back = simplegui.load_image("d:\card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
msg=""
ab=False
score = 0
tr=0
vp=0
vd=0
deck=[]
q=0
cdpos=cppos=0
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        self.suit=suit
        self.rank=rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc=(CARD_CENTER[0]+CARD_SIZE[0]*RANKS.index(self.rank),
                  CARD_CENTER[1]+CARD_SIZE[1]*SUITS.index(self.suit))
                  
        canvas.draw_image(card_images,card_loc,CARD_SIZE,pos,CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.h=""
        self.hand=[]

    def __str__(self):
        return "Hand contains "+str(self.h)

    def add_Card(self, Card):
        self.hand.append(Card)
        return self.hand

    def get_value(self):
        value=0
        for card in self.hand:
            rank=card.get_rank()
            value=value+VALUES[rank]
        for Card in self.hand:
            rank=Card.get_rank()
            if rank=='A' and value<=11:
                value+=10
        return value
                
    def draw(self, canvas, p):
        pos=p
        global player
        for l in range(0,len(self.hand)):
            self.hand[l].draw(canvas,pos)
            pos[0]=pos[0]+90
        if in_play==True:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [115.5,184], CARD_BACK_SIZE)
        
            # draw a hand on the canvas, use the draw method for cards
        

# define deck class 
class Deck:
    def __init__(self):
        global deck
        popped=[]
        deck=[]
        self.Card=[Card(suit,rank)for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.Card)

    def deal_Card(self):
        popped=self.Card.pop(0)
        return popped
    
    def __str__(self):
        st="Deck contains "
        for i in range(52):
            st=st+str(deck[i])+" "
        return st


#define event handlers for buttons
def deal():
    global outcome,in_play,deck,q,player,dealer,vp,vd,D,msg,cdpos,cppos,flip,score,ab,tr
    if in_play==True:
        msg="Abandon.you lost!"
        ab=True
        score=-1
        in_play=False
    if in_play==False:
        cdpos=cppos=10
        if ab:
            msg="Abandon.you lost!click hit/stand(new)"
            ab=False
        else:
            msg="click hit or stand"
        in_play=True
        q=0
        vp=0
        vd=0
        D=Deck()
        D.shuffle()

        flip=0
        player=Hand()
        dealer=Hand()

        player.add_Card(D.deal_Card())
        dealer.add_Card(D.deal_Card())
        player.add_Card(D.deal_Card())
        dealer.add_Card(D.deal_Card())
        vp=player.get_value()
        vd=dealer.get_value()

        tr += 1

    
def hit():
    global vp,vd,in_play,score,msg,flip,deck,q,D
    if in_play==True:
        player.add_Card(D.deal_Card())
        flip=1
        vp=player.get_value()

        if vp>21:
            score=-1
            msg="your game busted.NEW DEAL?"
            in_play=False


        elif vp>vd:
            score=-1
            msg="you win!new deal?"
            in_play=False

        if vp==vd:
            score=-1
            msg="you lose!new deal?"
            in_play=False
            
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global vp,vd,in_play,score,msg,flip
    if in_play:
        dealer.add_Card(D.deal_Card())
        flip=1
        vd=dealer.get_value()

        if vd>17:
            score-=1
            in_play=False
            msg="dealer's game busted.you win click deal"
        if vp==vd:
            score-=1
            in_play=False
            msg="you lose!new deal"
def exit():
    frame.stop()
            

# draw handler    
def draw(canvas):
    global score,msg,player,dealer,ab
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Game: "+str(tr), [500,60], 25, "Yellow")
    canvas.draw_text("BlackJack", [210,70], 48, "Aqua")
    canvas.draw_text("Score: "+str(score), [250,100], 32, "White")
    canvas.draw_text("Dealer", [20,170], 36, "White")
    canvas.draw_text("Player", [20,380], 36, "White")
    canvas.draw_text(msg, [160,380], 24, "Red")
    player.draw(canvas,[20,400])
    dealer.draw(canvas,[20,200])
frame=simplegui.create_frame("home",600,600)
frame.add_button("deal",deal,200)
frame.add_button("hit",hit,200)
frame.add_button("stand",stand,200)
frame.add_button("exit",exit,200)
frame.set_draw_handler(draw)
deal()

frame.start()
