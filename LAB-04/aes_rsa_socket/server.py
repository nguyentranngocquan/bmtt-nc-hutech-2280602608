from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# Khởi tạo socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('server_ip', 12345))  # Thay 'server_ip' và port đúng

# Tạo khóa RSA client
client_key = RSA.generate(2048)

# Nhận khóa public key server (lấy kích thước buffer phù hợp, ví dụ 2048 byte)
server_public_key_data = client_socket.recv(2048)
server_public_key = RSA.import_key(server_public_key_data)

# Gửi public key client cho server
client_socket.send(client_key.publickey().export_key(format='PEM'))

# Nhận AES key được mã hóa bằng RSA từ server
encrypted_aes_key = client_socket.recv(256)  # RSA 2048 bit = 256 bytes

# Giải mã AES key bằng private key client
cipher_rsa = PKCS1_OAEP.new(client_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)


def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext  # Trả về iv + ciphertext


def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()


def receive_messages():
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print("Server disconnected.")
                break
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print("Received:", decrypted_message)
        except Exception as e:
            print("Error receiving message:", e)
            break


# Bắt đầu luồng nhận tin nhắn
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Vòng lặp gửi tin nhắn
while True:
    message = input("Enter message ('exit' to quit): ")
    encrypted_message = encrypt_message(aes_key, message)
    client_socket.send(encrypted_message)
    if message == "exit":
        break

client_socket.close()
