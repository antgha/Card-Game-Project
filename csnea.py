import pygame, sys
import button
import random
import sqlite3
from sqlite3 import Error
import hashlib
from treeTraversal import TreeNode

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
backdrop = pygame.image.load('Background/pink_backdrop.png').convert_alpha()
pygame.display.set_caption("Tarneeb")

#TIMER
timer_font = pygame.font.SysFont('Arial', 35)
timer_text = timer_font.render("00:15", True, (0, 0, 0))
timer_text_rect = timer_text.get_rect(center = (WIDTH / 2, HEIGHT / 2 - 25))
seconds = 15
pygame.time.set_timer(pygame.USEREVENT, 1000)

base_font = pygame.font.SysFont('Arial', 25)

# USERNAME BOX USER INPUT
username_text = ''
username_active = False
username_input_rect = pygame.Rect(425, 65, 140, 32)
username_input_rect_colour = pygame.Color('black')

# PASSWORD BOX USER INPUT
password_text = ''
password_active = False
password_input_rect = pygame.Rect(425, 165, 140, 32)
password_input_rect_colour = pygame.Color('black')

#CONFIRM PASSWORD BOX USER INPUT
confirm_password_text = ''
confirm_password_active = False
confirm_password_input_rect = pygame.Rect(700, 265, 140, 32)
confirm_password_input_rect_colour = pygame.Color('black')

# LOADING IMAGES AND CONSTRUCTING BUTTONS
tarneeb_image = pygame.image.load('Background/tarneeblogo.png').convert_alpha()
tarneeb_button = button.Button(470, 50, tarneeb_image, 0.6)

login_image = pygame.image.load('Background/loginbutton.png').convert_alpha()
login_button = button.Button(520, 150, login_image, 0.6)

create_account_image = pygame.image.load('Background/createaccountbutton.png').convert_alpha()
create_account_button = button.Button(345, 250, create_account_image, 0.6)

username_image = pygame.image.load('Background/usernamebutton.png').convert_alpha()
username_button = button.Button(75, 50, username_image, 0.6)

password_image = pygame.image.load('Background/passwordbutton.png').convert_alpha()
password_button = button.Button(75, 150, password_image, 0.6)

login_back_image = pygame.image.load('Background/backbutton.png').convert_alpha()
login_back_button = button.Button(75, 350, login_back_image, 0.6)

confirm_password_image = pygame.image.load('Background/confirmpasswordbutton.png').convert_alpha()
confirm_password_button = button.Button(75, 250, confirm_password_image, 0.6)

create_account_back_image = pygame.image.load('Background/backbutton.png').convert_alpha()
create_account_back_button = button.Button(75, 450, create_account_back_image, 0.6)

login_confirm_image = pygame.image.load('Background/confirm.png').convert_alpha()
login_confirm_button = button.Button(75, 250, login_confirm_image, 0.6)

create_account_confirm_image = pygame.image.load('Background/confirm.png').convert_alpha()
create_account_confirm_button = button.Button(75, 350, create_account_confirm_image, 0.6)

back_of_card_image = pygame.image.load('Cards/back_of_card.jpg').convert_alpha()
back_of_card_button = button.Button(100, 50, back_of_card_image, 0.1)

logged_in = False

card_active_player1 = None
card_active_player2 = None
card_active_player3 = None
card_active_player4 = None

#TIMER
pause = False

#SETTINGS
audio_image = pygame.image.load('Background/audio_image.png').convert_alpha()
audio_image_button = button.Button(75, 50, audio_image, 0.6)

connection = sqlite3.connect('tarneeb.db')
cursor = connection.cursor()

def validLocation(pos):
    validArea = pygame.Rect(100, 50, 200, 200)
    # print("In area")
    return validArea.collidepoint(pos)
                
def eventHandler():
    global username_text, password_text, confirm_password_text, username_active, password_active, confirm_password_active, card_active_player1, card_active_player2, card_active_player3, card_active_player4, seconds, pause

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.USEREVENT:
            seconds -= 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if username_input_rect.collidepoint(event.pos):
                username_active = True
            else:
                username_active = False

            if password_input_rect.collidepoint(event.pos):
                password_active = True
            else:
                password_active = False
                
            if confirm_password_input_rect.collidepoint(event.pos):
                confirm_password_active = True
            else:
                confirm_password_active = False    
                   
            if card_active_player1 is None:     
                for card in mainGame.player1_cards:
                    if card.rect.collidepoint(event.pos):
                        card_active_player1 = card
                    pygame.display.flip()
                    
            if card_active_player2 is None:
                for card in mainGame.player2_cards:
                    if card.rect.collidepoint(event.pos):
                        card_active_player2 = card
                    pygame.display.flip()
                    
            if card_active_player3 is None:
                for card in mainGame.player3_cards:
                    if card.rect.collidepoint(event.pos):
                        card_active_player3 = card
                    pygame.display.flip()
                    
            if card_active_player4 is None:
                for card in mainGame.player4_cards:
                    if card.rect.collidepoint(event.pos):
                        card_active_player4 = card
                    pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONUP:
            if card_active_player1 is not None:
                card_active_player1 = None
                
            if card_active_player2 is not None:
                card_active_player2 = None
                
            if card_active_player3 is not None:
                card_active_player3 = None
                
            if card_active_player4 is not None:
                card_active_player4 = None
                
        if event.type == pygame.MOUSEMOTION:
            if card_active_player1 is not None:
                card_active_player1.rect.center = event.pos
                if validLocation(event.pos):
                    pass
                
            if card_active_player2 is not None:
                card_active_player2.rect.center = event.pos
                if validLocation(event.pos):
                    pass

            if card_active_player3 is not None:
                card_active_player3.rect.center = event.pos
                if validLocation(event.pos):
                    pass

            if card_active_player4 is not None:
                card_active_player4.rect.center = event.pos
                if validLocation(event.pos):
                    pass

        if event.type == pygame.KEYDOWN:
            if username_active:
                if event.key == pygame.K_BACKSPACE:
                    username_text = username_text[:-1]
                else:
                    username_text += event.unicode
            elif password_active:
                if event.key == pygame.K_BACKSPACE:
                    password_text = password_text[:-1]
                else:
                    password_text += event.unicode
            if confirm_password_active:
                if event.key == pygame.K_BACKSPACE:
                    confirm_password_text = confirm_password_text[:-1]
                else:
                    confirm_password_text += event.unicode
            
            if event.key == pygame.K_ESCAPE:
                pause = not pause
def checkLogin(username_text, password_text):
    global logged_in
    h = hashlib.new("SHA256")
    h.update(password_text.encode())
    hashed_password = h.hexdigest()
    cursor.execute("SELECT * FROM userdata WHERE Username = ? AND Password = ?", (username_text, hashed_password))
    if cursor.fetchone():
        print("Welcome")
        connection.commit()
        logged_in = True
    elif cursor.fetchone() is None:
        print("Invalid Username or Password")
        logged_in = False
        
    return logged_in

def createAccount(username_text, password_text, confirm_password_text):
    global account_created
    try:
        cursor.execute("SELECT * FROM userdata WHERE Username = ?", (username_text,))
        if cursor.fetchone():
            print("Username already exists")
            account_created = False
        else:
            if password_text == confirm_password_text:
                h = hashlib.new("SHA256")
                h.update(password_text.encode())
                hashed_password = h.hexdigest()
                cursor.execute("INSERT INTO userdata VALUES (?, ?)", (username_text, hashed_password))
                connection.commit()
                print("Account created")
                account_created = True
            else:
                print("Passwords do not match")
                account_created = False
    except Error as e:
        print(e)

account_created = createAccount(username_text, password_text, confirm_password_text)

def gameMenu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill((202, 228, 241))
        screen.blit(backdrop, backdrop.get_rect(center = (WIDTH / 2, HEIGHT / 2)))
        mainGame.drawHand(screen)
        mainGame.compareCards(card_active_player1, card_active_player2, card_active_player3, card_active_player4)

        # if seconds >= 0:
        #     display_seconds = seconds % 60
        #     display_minutes = int(seconds / 60) % 60
        #     #THIS DOES PADDING WHERE I AM ABLE TO ADJUST THE NUMBER OF 0'S ACCORDING TO SECONDS, MILLISECONDS, 02 MEANS 2 DIGITS, 03 WILL BE 001, ETC.
        #     timer_text = timer_font.render(f"{display_minutes:02}:{display_seconds:02}", True, (0, 0, 0))
        # screen.blit(timer_text, timer_text_rect)
        
        if pause == True:
            pauseMenu()
                        
        eventHandler()
        clock.tick(60)
        pygame.display.update()

class MenuState:
    def __init__(self):
        self.mainMenu()

    def mainMenu(self):
        while True:
            screen.fill((202, 228, 241))
            if tarneeb_button.draw(screen) and logged_in == True:
                gameMenu()
            if login_button.draw(screen):
                self.loginMenu()
            if create_account_button.draw(screen):
                self.createAccountMenu()

            eventHandler()
            pygame.display.update()

    def loginMenu(self):
        while True:
            screen.fill((202, 228, 241))
            username_button.draw(screen)
            password_button.draw(screen)
            pygame.draw.rect(screen, username_input_rect_colour, username_input_rect, 2)
            pygame.draw.rect(screen, password_input_rect_colour, password_input_rect, 2)
            if login_back_button.draw(screen):
                self.mainMenu()
            
            # LOAD USERNAME TEXT BOX INSIDE MENU
            username_text_surface = base_font.render(username_text, True, (225, 255, 255))
            screen.blit(username_text_surface, (username_input_rect.x + 5, username_input_rect.y + 5))
            
            # LOAD PASSWORD TEXT BOX INSIDE MENUS
            password_text_surface = base_font.render(password_text, True, (255, 255, 255))
            screen.blit(password_text_surface, (password_input_rect.x + 5, password_input_rect.y + 5))

            if login_confirm_button.draw(screen):
                checkLogin(username_text, password_text)
                
            if logged_in == True:
                logged_in_text = base_font.render("LOGGED IN", True, (0, 0, 0))
                screen.blit(logged_in_text, (500, 500))
            elif logged_in == False and login_confirm_button.draw(screen):
                not_logged_in_text = base_font.render("INVALID USERNAME OR PASSWORD", True, (0, 0, 0))
                screen.blit(not_logged_in_text, (500, 500))
                
            eventHandler()

            pygame.display.update()

    def createAccountMenu(self):
        while True:
            screen.fill((202, 228, 241))
            username_button.draw(screen)
            password_button.draw(screen)
            confirm_password_button.draw(screen)
            pygame.draw.rect(screen, username_input_rect_colour, username_input_rect, 2)
            pygame.draw.rect(screen, password_input_rect_colour, password_input_rect, 2)
            pygame.draw.rect(screen, confirm_password_input_rect_colour, confirm_password_input_rect, 2)
            if create_account_back_button.draw(screen):
                self.mainMenu()

            # LOAD USERNAME TEXT BOX INSIDE MENU.
            username_text_surface = base_font.render(username_text, True, (0, 0, 0))
            screen.blit(username_text_surface, (username_input_rect.x, username_input_rect.y))

            # LOAD PASSWORD TEXT BOX INSIDE MENU.
            password_text_surface = base_font.render(password_text, True, (0, 0, 0))
            screen.blit(password_text_surface, (password_input_rect.x, password_input_rect.y))

            # LOAD CONFIRM PASSWORD TEXT BOX INSIDE MENU.
            confirm_password_surface = base_font.render(confirm_password_text, True, (0, 0, 0))
            screen.blit(confirm_password_surface, (confirm_password_input_rect.x, confirm_password_input_rect.y))

            if create_account_confirm_button.draw(screen):
                createAccount(username_text, password_text, confirm_password_text)
                
            if account_created == True:
                account_created_text = base_font.render("ACCOUNT CREATED", True, (0, 0, 0))
                screen.blit(account_created_text, (500, 500))
            elif account_created == False:
                account_not_created_text = base_font.render("PASSWORDS DO NOT MATCH", True, (0, 0, 0))
                screen.blit(account_not_created_text, (500, 500))
                
            eventHandler()

            pygame.display.update()

carddict = {"two_of_hearts": 0, "three_of_hearts" : 1, "four_of_hearts" : 2, "five_of_hearts" : 3, "six_of_hearts" : 4, 
        "seven_of_hearts" : 5, "eight_of_hearts" : 6, "nine_of_hearts" : 7, "ten_of_hearts" : 8, 
        "jack_of_hearts" : 9, "queen_of_hearts" : 10, "king_of_hearts" : 11, "ace_of_hearts" : 12,
        "two_of_diamonds" : 13, "three_of_diamonds" : 14, "four_of_diamonds" : 15, "five_of_diamonds" : 16, "six_of_diamonds" : 17,
        "seven_of_diamonds" : 18, "eight_of_diamonds" : 19, "nine_of_diamonds" : 20, "ten_of_diamonds" : 21,
        "jack_of_diamonds" : 22, "queen_of_diamonds" : 23, "king_of_diamonds" : 24, "ace_of_diamonds" : 25,
        "two_of_spades" : 26, "three_of_spades" : 27, "four_of_spades" : 28, "five_of_spades" : 29, "six_of_spades" : 30,
        "seven_of_spades" : 31, "eight_of_spades" : 32, "nine_of_spades" : 33, "ten_of_spades" : 34,
        "jack_of_spades" : 35, "queen_of_spades" : 36, "king_of_spades" : 37, "ace_of_spades" : 38,
        "two_of_clubs" : 39, "three_of_clubs" : 40, "four_of_clubs" : 41, "five_of_clubs" : 42, "six_of_clubs" : 43,
        "seven_of_clubs" : 44, "eight_of_clubs" : 45, "nine_of_clubs" : 46, "ten_of_clubs" : 47,
        "jack_of_clubs" : 48, "queen_of_clubs" : 49, "king_of_clubs" : 50, "ace_of_clubs" : 51}

class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.card = value + suit
        self.filename = value.lower() + '_of_' + suit.lower() + '.png'
                
    def show(self):
        return "{}_of_{}".format(self.value, self.suit)

class Deck(Card):
    def __init__(self):
        self.player1 = []
        self.player2 = []
        self.player3 = []
        self.player4 = []
        self.build()

    def build(self):
        self.cards = []
        
        for s in ["hearts", "diamonds", "spades", "clubs"]:
            for v in ["ace", "two", "three", "four", "five", "six", 
                      "seven", "eight", "nine", "ten", "jack", "queen", "king"]:
                self.cards.append(Card(v, s))
                
        return self.cards
                
    def shuffle(self):
        self.build()
        
        for i in range(len(self.cards) - 1, 0, -1):
            rand = random.randint(0 , i)
            self.cards[i], self.cards[rand] = self.cards[rand], self.cards[i]
            
        return self.cards
        
    def deal(self):
        self.shuffle()
        
        for i in range(13):
            self.player1.append(self.cards.pop(0))
        self.player1.sort(key=lambda x: carddict[x.filename.replace(".png", "")])

        for i in range(13):
            self.player2.append(self.cards.pop(0))
        self.player2.sort(key=lambda x: carddict[x.filename.replace(".png", "")])
                    
        for i in range(13):
            self.player3.append(self.cards.pop(0))
        self.player3.sort(key=lambda x: carddict[x.filename.replace(".png", "")])

        for i in range(13):
            self.player4.append(self.cards.pop(0))
        self.player4.sort(key=lambda x: carddict[x.filename.replace(".png", "")])
        
        print("Player 1: ")
        print("Number of elements in player1: ", len(self.player1))
        for i in self.player1:
            print(i.show())
        print("Player 2: ")
        print("Number of elements in player2: ", len(self.player2))
        for i in self.player2:
            print(i.show())
        print("Player 3: ")
        print("Number of elements in player3: ", len(self.player3))
        for i in self.player3:
            print(i.show())
        print("Player 4: ")
        print("Number of elements in player4: ", len(self.player4))
        for i in self.player4:
            print(i.show())
            
        return self.player1, self.player2, self.player3, self.player4

    def rotateCards(self):
        for card in self.player1_cards:
            card.image = pygame.transform.rotate(card.image, 0)
        for card in self.player2_cards:
            card.image = pygame.transform.rotate(card.image, 90)
        for card in self.player3_cards:
            card.image = pygame.transform.rotate(card.image, 180)
        for card in self.player4_cards:
            card.image = pygame.transform.rotate(card.image, 270)
        
    def draw(self):
        self.deal()
        
        self.player1_cards = [button.Button(350 + (25 * i), 400, pygame.image.load('Cards/' + self.player1[i].filename).convert_alpha(), 0.2) for i in range(13)]
        self.player2_cards = [button.Button(70, 80 + (25 * i), pygame.image.load('Cards/' + self.player2[i].filename).convert_alpha(), 0.2) for i in range(13)]
        self.player3_cards = [button.Button(700 - (25 * i), 50, pygame.image.load('Cards/' + self.player3[i].filename).convert_alpha(), 0.2) for i in range(13)]
        self.player4_cards = [button.Button(1000, 400 - (25 * i), pygame.image.load('Cards/' + self.player4[i].filename).convert_alpha(), 0.2) for i in range(13)]

        self.rotateCards()
        
        return self.player1_cards, self.player2_cards, self.player3_cards, self.player4_cards

    def drawHand(self, screen):
        for card in self.player1_cards:
            card.draw(screen)
            pygame.display.update()
        for card in self.player2_cards:
            card.draw(screen)
            pygame.display.update()
        for card in self.player3_cards:
            card.draw(screen)
            pygame.display.update()
        for card in self.player4_cards:
            card.draw(screen)
            pygame.display.update()

            
    def removeCard(self, card):
        if card in self.player1:
            self.player1.remove(card)
            self.player1_cards = [button.Button(350 + (25 * i), 400, pygame.image.load('Cards/' + card.filename).convert_alpha(), 0.2) for i, card in enumerate(self.player1)]
            
        if card in self.player2:
            self.player2.remove(card)
            self.player2_cards = [button.Button(70, 80 + (25 * i), pygame.image.load('Cards/' + card.filename).convert_alpha(), 0.2) for i, card in enumerate(self.player2)]
            
        if card in self.player3:
            self.player3.remove(card)
            self.player3_cards = [button.Button(700 - (25 * i), 50, pygame.image.load('Cards/' + card.filename).convert_alpha(), 0.2) for i, card in enumerate(self.player3)]
            
        if card in self.player4:
            self.player4.remove(card)
            self.player4_cards = [button.Button(1000, 400 - (25 * i), pygame.image.load('Cards/' + card.filename).convert_alpha(), 0.2) for i, card in enumerate(self.player4)]
            
        pygame.display.update()      
    
class MainGame(Deck):
    def __init__(self):
        super().__init__()
        self.highestBidder = None
        self.bids = [0, 0, 0, 0]
        self.highestBids = {}
        self.startPlayerTurn()

    def startPlayerTurn(self):
        self.getHighestBidder()
        self.first_player = 0
        
        if self.highestBidder == 1:
            self.first_player = 1
            self.getTrumpSuit()
        elif self.highestBidder == 2:
            self.first_player = 2
            self.getTrumpSuit()
        elif self.highestBidder == 3:
            self.first_player = 3
            self.getTrumpSuit()
        elif self.highestBidder == 4:
            self.first_player = 4
            self.getTrumpSuit()

        self.draw()
        
    def getBid(self, username_text, highestBid):
        self.username = username_text
        self.auction_bid = []
        self.value_auction_bid = [7, 8, 9, 10, 11, 12, 13, "pass"]
        self.bids = [0, 0, 0, 0]
        self.current_position = 0
        
        #FOR PLAYES IN SELF.PLAYERS

        for i in self.value_auction_bid:
            self.auction_bid.append(pygame.image.load('Background/' + str(i) + '.png').convert_alpha())

        self.auction_bid_buttons = [button.Button(100 + (30 * i), 200, self.auction_bid[i], 0.3) for i in range(8)]

        run = True
        while run:
            try:
                screen.blit(base_font.render(f"{self.username}, ENTER BID ({highestBid}-13): ", True, (0, 0, 0)), (100, 100))
                pygame.display.flip()

                for bid in self.auction_bid_buttons:
                    if bid.draw(screen):
                        bid_value = self.auction_bid_buttons.index(bid) + 7
                        if bid_value == 14:
                            bid_value -= 14
                        self.bids[self.current_position] = bid_value
                        self.current_position += 1
                        if bid_value > highestBid:
                            highestBid = bid_value
                        print(bid_value, self.bids)
                run = False
            except:
                if self.current_position > 4:
                    screen.blit(base_font.render("BIDDING ENDED", True, (0, 0, 0)), (100, 100))
                    print(highestBid)
                elif bid_value == 13:
                    screen.blit(base_font.render("BIDDING ENDED", True, (0, 0, 0)), (100, 100))
                    print("13, end bid")
                    run = False
                
                #CHECK WETHER THERE WAS 4 PASSES AND IF THERE WAS, RECURSIVELY CALL A NEW BIDDING

            eventHandler()
            pygame.display.update()

    def getHighestBidder(self):
        self.getBid(username_text, highestBid = 0)
        self.maximumBid = 0
        self.highestBidder = 0

        for bidIndex, bid in enumerate(self.bids):
            if bid > self.maximumBid:
                self.maximumBid = bid
                self.highestBidder = bidIndex + 1

        print("Highest Bidder (Player) & Highest Bid:", self.highestBidder, ",", self.maximumBid)
        return self.highestBidder, self.maximumBid
    
    def getTrumpSuit(self):
        self.trump_suit_list = []
        self.value_trump_suit = ["hearts", "diamonds", "spades", "clubs"]
        self.trump_suit = ""
        suit_value = 0
        
        for suit in self.value_trump_suit:
            self.trump_suit_list.append(pygame.image.load('Background/' + suit + '.png').convert_alpha())

        self.trump_suit_buttons = [button.Button(400 + (150 * i), 200, self.trump_suit_list[i], 0.2) for i in range(4)]
        
        run = True
        while run:
            screen.blit(base_font.render("SELECT TRUMP SUIT: ", True, (0, 0, 0)), (100, 100))
            pygame.display.flip()

            for suit in self.trump_suit_buttons:
                if suit.draw(screen):
                    suit_value = self.trump_suit_buttons.index(suit) + 1

            if suit_value == 1:
                self.trump_suit = "Hearts"
                print("Hearts")
                run = False
            elif suit_value == 2:
                self.trump_suit = "Diamonds"
                print("Diamonds")
                run = False
            elif suit_value == 3:
                self.trump_suit = "Spades"
                print("Spades")
                run = False
            elif suit_value == 4:
                self.trump_suit = "Clubs"
                print("Clubs")
                run = False

            eventHandler()
            pygame.display.update()
            
            return self.trump_suit

    def compareCards(self, card_active_player1, card_active_player2, card_active_player3, card_active_player4):
        self.roundWinner = 0
        self.gameWinner = 0

        for index, button_card in enumerate(self.player1_cards):
            if button_card == card_active_player1:
                card = self.player1[index]
                card_shown = card.show()
                player1_value, player1_suit = card_shown.split("_of_")
                print("Card:", card_shown)
                print("Player 1 Value:", player1_value, "Player 1 Suit:", player1_suit)
            
        for index, button_card in enumerate(self.player2_cards):
            if button_card == card_active_player2:
                card = self.player2[index]
                card_shown = card.show()
                player2_value, player2_suit = card_shown.split("_of_")
                print("Card:", card_shown)
                print("Player 2 Value:", player2_value, "Player 2 Suit:", player2_suit)

        for index, button_card in enumerate(self.player3_cards):
            if button_card == card_active_player3:
                card = self.player3[index]
                card_shown = card.show()
                player3_value, player3_suit = card_shown.split("_of_")
                print("Card:", card_shown)
                print("Player 3 Value:", player3_value, "Player 3 Suit:", player3_suit)

        for index, button_card in enumerate(self.player4_cards):
            if button_card == card_active_player4:
                card = self.player4[index]
                card_shown = card.show()
                player4_value, player4_suit = card_shown.split("_of_")
                print("Card:", card_shown)
                print("Player 4 Value:", player4_value, "Player 4 Suit:", player4_suit)
                
        if player1_suit == self.trump_suit and player2_suit == self.trump_suit and player3_suit == self.trump_suit and player4_suit == self.trump_suit:
            if player1_value > player2_value and player1_value > player3_value and player1_value > player4_value:
                self.roundWinner = 1
                print("Player 1 Wins")
            elif player2_value > player1_value and player2_value > player3_value and player2_value > player4_value:
                self.roundWinner = 2
                print("Player 2 Wins")
            elif player3_value > player1_value and player3_value > player2_value and player3_value > player4_value:
                self.roundWinner = 3
                print("Player 3 Wins")
            elif player4_value > player1_value and player4_value > player2_value and player4_value > player3_value:
                self.roundWinner = 4
                print("Player 4 Wins")
                
        if player1_suit == player2_suit == player3_suit == player4_suit:
            if player1_value > player2_value and player1_value > player3_value and player1_value > player4_value:
                self.roundWinner = 1
                print("Player 1 Wins")
            elif player2_value > player1_value and player2_value > player3_value and player2_value > player4_value:
                self.roundWinner = 2
                print("Player 2 Wins")
            elif player3_value > player1_value and player3_value > player2_value and player3_value > player4_value:
                self.roundWinner = 3
                print("Player 3 Wins")
            elif player4_value > player1_value and player4_value > player2_value and player4_value > player3_value:
                self.roundWinner = 4
                print("Player 4 Wins")
            
        if player1_suit == self.trump_suit and player2_suit != self.trump_suit and player3_suit != self.trump_suit and player4_suit != self.trump_suit:
            self.roundWinner = 1
            print("Player 1 Wins")
        elif player2_suit == self.trump_suit and player1_suit != self.trump_suit and player3_suit != self.trump_suit and player4_suit != self.trump_suit:
            self.roundWinner = 2
            print("Player 2 Wins")
        elif player3_suit == self.trump_suit and player1_suit != self.trump_suit and player2_suit != self.trump_suit and player4_suit != self.trump_suit:
            self.roundWinner = 3
            print("Player 3 Wins")
        elif player4_suit == self.trump_suit and player1_suit != self.trump_suit and player2_suit != self.trump_suit and player3_suit != self.trump_suit:
            self.roundWinner = 4
            print("Player 4 Wins")
            
        if player1_suit == self.trump_suit and player2_suit == self.trump_suit and player3_suit != self.trump_suit and player4_suit != self.trump_suit:
            if player1_value > player2_value:
                self.roundWinner = 1
                print("Player 1 Wins")
            else:
                self.roundWinner = 2
                print("Player 2 Wins")
        elif player1_suit == self.trump_suit and player3_suit == self.trump_suit and player2_suit != self.trump_suit and player4_suit != self.trump_suit:
            if player1_value > player3_value:
                self.roundWinner = 1
                print("Player 1 Wins")
            else:
                self.roundWinner = 3
                print("Player 3 Wins")
        elif player1_suit == self.trump_suit and player4_suit == self.trump_suit and player2_suit != self.trump_suit and player3_suit != self.trump_suit:
            if player1_value > player4_value:
                self.roundWinner = 1
                print("Player 1 Wins")
            else:
                self.roundWinner = 4
                print("Player 4 Wins")
        elif player2_suit == self.trump_suit and player3_suit == self.trump_suit and player1_suit != self.trump_suit and player4_suit != self.trump_suit:
            if player2_value > player3_value:
                self.roundWinner = 2
                print("Player 2 Wins")
            else:
                self.roundWinner = 3
                print("Player 3 Wins")
        elif player2_suit == self.trump_suit and player4_suit == self.trump_suit and player1_suit != self.trump_suit and player3_suit != self.trump_suit:
            if player2_value > player4_value:
                self.roundWinner = 2
                print("Player 2 Wins")
            else:
                self.roundWinner = 4
                print("Player 4 Wins")
        elif player3_suit == self.trump_suit and player4_suit == self.trump_suit and player1_suit != self.trump_suit and player2_suit != self.trump_suit:
            if player3_value > player4_value:
                self.roundWinner = 3
                print("Player 3 Wins")
            else:
                self.roundWinner = 4
                print("Player 4 Wins")
                
        if player1_suit == player2_suit == self.trump_suit and player3_suit != self.trump_suit and player4_suit != self.trump_suit:
            if player1_value > player2_value:
                self.roundWinner = 1
                print("Player 1 Wins")
            else:
                self.roundWinner = 2
                print("Player 2 Wins")
        elif player1_suit == player3_suit == self.trump_suit and player2_suit != self.trump_suit and player4_suit != self.trump_suit:
            if player1_value > player3_value:
                self.roundWinner = 1
                print("Player 1 Wins")
            else:
                self.roundWinner = 3
                print("Player 3 Wins")
        elif player1_suit == player4_suit == self.trump_suit and player2_suit != self.trump_suit and player3_suit != self.trump_suit:
            if player1_value > player4_value:
                self.roundWinner = 1
                print("Player 1 Wins")
            else:
                self.roundWinner = 4
                print("Player 4 Wins")
        elif player2_suit == player3_suit == self.trump_suit and player1_suit != self.trump_suit and player4_suit != self.trump_suit:
            if player2_value > player3_value:
                self.roundWinner = 2
                print("Player 2 Wins")
            else:
                self.roundWinner = 3
                print("Player 3 Wins")
        elif player2_suit == player4_suit == self.trump_suit and player1_suit != self.trump_suit and player3_suit != self.trump_suit:
            if player2_value > player4_value:
                self.roundWinner = 2
                print("Player 2 Wins")
            else:
                self.roundWinner = 4
                print("Player 4 Wins")
        elif player3_suit == player4_suit == self.trump_suit and player1_suit != self.trump_suit and player2_suit != self.trump_suit:
            if player3_value > player4_value:
                self.roundWinner = 3
                print("Player 3 Wins")
            else:
                self.roundWinner = 4
                print("Player 4 Wins")
        
                
        
                
                
                
                
                
                
        
    def pointSystem(self, gameWinner, roundWinner):
        team1_game_points = 0
        team2_game_points = 0
        team1_round_points = 0
        team2_round_points = 0
        
        if gameWinner == 1 or gameWinner == 3:
            if self.highestBid == 13 and team1_game_points == 13:
                team1_game_points += 13
            elif self.highestBid < 13 and team1_round_points == 13:
                team1_game_points += 3
            elif self.highestBid < 13 and team1_game_points == self.highestBid:
                team1_game_points += self.highestBid
            elif team1_game_points < self.highestBid:
                team1_game_points -= self.highestBid
                team2_game_points += team2_game_points
            elif team1_game_points > self.highestBid:
                team1_game_points += team1_game_points
                
        if gameWinner == 2 or gameWinner == 4:
            if self.highestBid == 13 and team2_round_points == 13:
                team2_game_points += 13
            elif self.highestBid < 13 and team2_round_points == 13:
                team2_game_points += 3
            elif self.highestBid < 13 and team2_round_points == self.highestBid:
                team2_game_points += self.highestBid
            elif team2_round_points < self.highestBid:
                team2_game_points -= self.highestBid
                team1_game_points += team1_round_points      
                
        #4 PASSES, THE DECK RESHUFFLE
        #IF I BID 8 AND GET 7, I LOSE 8 AND WHATEVER THE OPPOSING TEAM WINS, THEY GAIN THAT AMOUNT
        #IF I ORDER 13 AND GET THEM, I GET 26 POINTS
        #IF I ORDER 13 AND GET LESS THAN 13, I LOSE 26 POINS OR HOWEVER MUCH I WANT TO MAKE IT
        #IF I ORDER 13 AND GET LESS THAN 13, I LOSE 13 POINTS. 
        #FIRST TEAM TO GET TO 31 POINTS WINS THE GAME
        #ONE GAME OR UP TO 31 POINTS
        #IF SOMEONE ORDER 7 AND THE ANOTHER 8, THE PLAYER THAT BIDDED 7 GETS TO CHOOSE 9 OR MORE OR PASS AND IT KEEPS REPEATING 
        #IF SOMEONE BIDS 13 NOONE ELSE CAN BID
        
        

d = Deck()
mainGame = MainGame()
            
def pauseMenu():
    transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(transparent_surface, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])
    screen.blit(transparent_surface, (0, 0))
    
    if audio_image_button.draw(screen):
        audioSettings()

def leaderboard():
    cursor.execute("SELECT * FROM userdata WHERE Username = ? AND Password = ?", (username_text, password_text))
    if high_score < cursor.fetchone():
        high_score = cursor.fetchone()
    return high_score

def audioSettings():
    pass

MenuState()
        
connection.close()
cursor.close()