import socket
import time
import sys
import threading

# Настройки вашего сервера DDNet
SERVER_IP = "46.174.54.240"
SERVER_PORT = 8441

def run_bot(bot_id):
    # Стартовый пакет для получения токена (Token handshake)
    connect_packet = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    
    while True:
        try:
            # Запрашиваем токен авторизации у сервера
            sock.sendto(connect_packet, (SERVER_IP, SERVER_PORT))
            data, addr = sock.recvfrom(1024)
            if data:
                # Извлекаем защитный токен из ответа сервера
                token = data[14:18] if len(data) > 18 else b"\x00\x00\x00\x00"
                # Формируем пакет входа с уникальным никнеймом бота
                net_packet = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x03" + token + f"CloudBot_{bot_id}".encode() + b"\x00"
                sock.sendto(net_packet, (SERVER_IP, SERVER_PORT))
                
                # Пакет ввода, симулирующий постоянный зажим клавиши "Вправо" (+right)
                move_packet = b"\x00\x10\x00\x01\x01\x00\x00\x00"
                while True:
                    sock.sendto(move_packet, (SERVER_IP, SERVER_PORT))
                    time.sleep(0.05)  # Интервал отправки для стабильного удержания
        except Exception:
            time.sleep(1)

# Автоматический запуск 4 автономных ботов (лимит игры на 1 IP хостинга)
for i in range(1, 5):
    t = threading.Thread(target=run_bot, args=(i,))
    t.daemon = True
    t.start()
    time.sleep(0.2)

print("\n[Успешно] Все 4 умных бота запущены в облаке!")

# Удерживаем процесс активным
while True:
    time.sleep(1)