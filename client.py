import socket, sys, json
def ask(req, port=7009):
    s = socket.create_connection(("127.0.0.1", port), timeout=120); s.sendall((req + "\n").encode()); buf = b""
    while True:
        d = s.recv(1 << 16)
        if not d: break
        buf += d
        if buf.endswith(b"\n") and buf.count(b"{") <= buf.count(b"}"): break
    s.close(); return json.loads(buf.decode()) if buf.strip().startswith(b"{") else buf.decode()
