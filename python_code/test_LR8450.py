import socket

HOST = "192.168.2.154"
PORT = 8802
TIMEOUT = 5.0

def write(sock, cmd):
    sock.sendall((cmd + "\r\n").encode("ascii"))

def query(sock, cmd):
    write(sock, cmd)
    data = sock.recv(4096).decode("ascii", errors="ignore").strip()
    return data

with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as s:
    s.settimeout(TIMEOUT)

    print("IDN:", query(s, "*IDN?"))
    print("Header before:", query(s, ":HEADer?"))

    write(s, ":HEADer OFF")        # command has no response body
    print("Header after:", query(s, ":HEADer?"))

    print("Error:", query(s, ":ERRor?"))
    print("Status:", query(s, ":STATus?"))