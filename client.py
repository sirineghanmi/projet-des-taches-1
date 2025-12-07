import socket
import json

BUFFER_SIZE = 4096
ENC = "utf-8"

class ClientTaches:
    def __init__(self, host="host.docker.internal", port=5000):
        self.host = host
        self.port = port
        self.sock = None

    def _connect(self):
        if self.sock:
            return True
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=5)
            return True
        except Exception as e:
            print(f"Erreur connexion: {e}")
            self.sock = None
            return False

    def envoyer(self, obj):
        if not self._connect():
            return None
        try:
            msg = json.dumps(obj, ensure_ascii=False) + "\n"
            self.sock.sendall(msg.encode(ENC))
            data = b""
            while True:
                chunk = self.sock.recv(BUFFER_SIZE)
                if not chunk:
                    self.close()
                    return None
                data += chunk
                if b"\n" in chunk:
                    break
            line, _sep, _rest = data.partition(b"\n")
            return json.loads(line.decode(ENC))
        except Exception as e:
            print(f"Erreur communication: {e}")
            self.close()
            return None

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        finally:
            self.sock = None
