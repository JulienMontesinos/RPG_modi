import sys
import pygame
import pickle
import socket
from player import Player
from random import randint
from screen import Screen
from map import Map


class Game:
    def __init__(self):
        self.width = 480
        self.height = 480
        self.screen = Screen()
        self.map = Map(self.screen)

        self.player = Player(p_id=None,
                             x=randint(35,310),
                             y=randint(300,430),
                             frame_width=32,
                             frame_height=32)
        self.port = 5555
        self.host = "100.118.201.175"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

        #self.group.add(self.player) 

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.player.id = self.sock.recv(2048).decode("utf-8")

    def send_player_data(self):
        data = {
            "id": self.player.id,
            "player": self.player
        }
        self.sock.send(pickle.dumps(data))
        return self.sock.recv(2048)

    def update_other_players_data(self, data):
        for player in data.values():
            #player.draw(self.screen, self.sprite_sheet)
            self.map.add_player(player)

    def update_screen(self): #Appeler en continuer depuis le jeu lancé
        #self.screen.fill((255, 255, 255))
        self.screen.upadate()
        self.map.update()
        self.map.add_player(self.player)
        
        #self.screen.upadate()

        self.player.move()
        #self.player.draw(self.screen, self.sprite_sheet)

        other_players_data = pickle.loads(self.send_player_data())
        self.update_other_players_data(other_players_data)
        pygame.display.update()


    def start(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(20)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_screen()
