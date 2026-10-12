import socket
import time
import sys
import threading

SERVER_IP = "46.174.54.240"
SERVER_PORT = 8441

def run_bot(bot_id):
    # Корректный стартовый пакет подключения Teeworlds/DDNet
    connect_packet = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    
    print(f"[Бот {bot_id}] Начинаю подключение к {SERVER_IP}:{SERVER_PORT}", flush=True)
    
    while True:
        try:
            # Шлем запрос токена
            sock.sendto(connect_packet, (SERVER_IP, SERVER_PORT))
            print(f"[Бот {bot_id}] Пакет подключения отправлен, жду ответ...", flush=True)
            
            data, addr = sock.recvfrom(1024)
            if data:
                print(f"[Бот {bot_id}] Получен ответ от сервера! Авторизуюсь...", flush=True)
                token = data[14:18] if len(data) > 18 else b"\x00\x00\x00\x00"
                
                # Пакет захода с ником
                net_packet = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x03" + token + f"CloudBot_{bot_id}".encode() + b"\x00"
                sock.sendto(net_packet, (SERVER_IP, SERVER_PORT))
                
                # Пакет постоянного спама движения вправо
                move_packet = b"\x00\x10\x00\x01\x01\x00\x00\x00"
                print(f"[Бот {bot_id}] Успешный вход! Спамлю движение вправо...", flush=True)
                
                while True:
                    sock.sendto(move_packet, (SERVER_IP, SERVER_PORT))
                    time.sleep(0.05)
        except socket.timeout:
            print(f"[Бот {bot_id}] Ошибка: Сервер не отвечает (Таймаут). Возможен бан IP хостинга!", flush=True)
            time.sleep(3)
        except Exception as e:
            print(f"[Бот {bot_id}] Произошла ошибка: {e}", flush=True)
            time.sleep(2)

# Включаем 4 ботов
for i in range(1, 5):
    t = threading.Thread(target=run_bot, args=(i,), daemon=True)
    t.start()
    time.sleep(0.3)

print("Все потоки ботов запущены!", flush=True)
while True:
    time.sleep(1)
