# Сервер: принимает входящие подключения от клиентов,
# обрабатывает сообщения и сохраняет их в базе данных.

#client.py
import socket
import threading
import sqlite3

# Создает базу данных и таблицу для сообщений, если она не существует
def init_db():
    connection = sqlite3.connect('chat.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    message TEXT)''')
    connection.commit()
    connection.close()

# Обработка сообщений от клиентов
def handle_client(client_socket, addr): # Обрабатывает сообщения от клиентов и отправляет их всем подключенным пользователям
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print (f"[{addr}] {message}")
                save_message(addr, message) # Сохраняем сообщение в БД
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    client_socket.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

# Сохранение сообщения в базе данных
def save_message(addr, message): # Сохраняет сообщение в базе данных
    username = addr[0] # Используем IP адрес как имя пользователя
    connection = sqlite3.connect('chat.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
    connection.commit()
    connection.close()

def broadcast(message, client_socket): # Отправляет сообщение всем клиентам, кроме отправителя
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()

# Запуск сервера
def start_server(): # Инициализирует сервер и принимает подключения
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen()
    print("[STARTING] Server is starting...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket) # Добавляем нового клиента в список
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

clients = []
init_db()
start_server()
