# Клиент: предоставляет пользователю интерфейс для ввода и отображения сообщений,
# отправляемых на сервер.

#server.py
import socket
import threading
import tkinter #Используется для создания графического интерфейса, где отображаются сообщения и поле ввода

# Отправляет сообщение на сервер и очищает поле ввода
def send_message():
    message = message_input.get()
    client.send(message.encode('utf-8'))
    message_input.delete(0, tkinter.END) # Очищаем поле ввода

# Получает сообщения от сервера и отображает их в текстовом поле
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat_display.config(state=tkinter.NORMAL) # Разрешаем редактирование
            chat_display.insert(tkinter.END, message + "\n") # Добавляем сообщение в текстовое поле
            chat_display.config(state = tkinter.DISABLED) # Запрещаем редактирование
            chat_display.yview(tkinter.END) # Прокручиваем текстовое поле вниз
        except:
            print("Ошибка подключения.")
            break

# Настройка окна приложения
root = tkinter.Tk()
root.title("Чат")

chat_display = tkinter.Text(root, state = tkinter.DISABLED)
chat_display.pack(padx = 10, pady = 10)

message_input = tkinter.Entry(root)
message_input.pack(padx=10, pady=10, fill=tkinter.X)
message_input.bind("<Return>", lambda event: send_message()) # Отправка сообщения при нажатии Enter

send_button = tkinter.Button(root, text = "Отправить", command = send_message)
send_button.pack(pady = 5)

# Установка соединения с сервером
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

# Запуск потока для получения сообщений
receive_thread = threading.Thread(target = receive_messages)
receive_thread.start()

root.mainloop()
