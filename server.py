import socket  
import pickle  
from player import Player  
from threading import Thread  

class Server:
    def __init__(self):
        self.port = 5555  # Le numéro de port sur lequel le serveur écoute
        self.host = "100.118.201.175"  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Créer une socket TCP
        self.addr = (self.host, self.host)
        self.players_data = {}  # Utilisé pour stocker les données de tous les joueurs. La clé est l'identifiant du joueur et la valeur est les données du joueur.

    def start(self):
        self.sock.bind((self.host, self.port))  # Se lier à l'hôte et au port spécifiés
        self.sock.listen()  
        print("Waiting for a connection, Server Started")  
        while True:  # Boucle infinie, continuant à accepter les connexions client
            conn, addr = self.sock.accept()  # Accepter une connexion client
            print("Connect to:", self.addr)  
            conn.send(str(id(conn)).encode("utf-8"))  # Envoyer l'identifiant unique de la connexion au client
            Thread(target=self.handle_message, args=(conn, )).start()  # Créer un nouveau fil de discussion pour chaque client afin de gérer les messages
        

    def handle_message(self, conn):
        while True:  # 无限循环，持续监听客户端消息
            try:
                data = conn.recv(2048)  # 接受客户端发送的数据，最大为2048字节
                if not data:  # 如果没有数据，说明连接可能已关闭
                    print("disconnected")
                    self.players_data.pop(str(id(conn)))  # 从玩家数据中移除对应的玩家信息
                    conn.close()  # 关闭连接
                    break  # 跳出循环
                else:
                    data = pickle.loads(data)  # 反序列化接收到的数据
                    self.update_one_player_data(data)  # 更新接收到的玩家数据
                    conn.sendall(pickle.dumps(self.get_other_players_data(data["id"])))  # 发送除了当前玩家外的所有玩家数据
            except Exception as e:
                print(repr(e))  # 打印出现的异常
                break  # 发生异常时跳出循环
        print("Lost connection")
        conn.close()

    def update_one_player_data(self, data):
        key = data["id"]  
        value = data["player"]  
        self.players_data[key] = value  

    def get_other_players_data(self, current_player_id):
        data = {}  # 创建一个新字典用于存储其他玩家的数据
        for key, value in self.players_data.items():  # 遍历所有玩家数据
            if key != current_player_id:  # 如果不是当前玩家的数据
                data[key] = value  # 添加到字典中
        return data  # 返回其他玩家的数据

if __name__ == '__main__':
    server = Server()  
    server.start()  