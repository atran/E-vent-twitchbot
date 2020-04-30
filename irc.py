import sys
import re
import socket

class IRCClient:
  SERVER = 'irc.chat.twitch.tv'
  PORT = 6667

  socket_retry_count = 0

  def __init__(self, settings):
    self.settings = settings
    self.set_socket_object()
  
  def set_socket_object(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock = sock

    sock.settimeout(10)

    server = (self.SERVER, self.PORT)
    try:
      sock.connect(server)
    except:
      print("[ERROR] Cannot connect to IRC")
      if self.socket_retry_count < 2:
        self.socket_retry_count += 1
        return self.set_socket_object()
      else:
        sys.exit()

    sock.settimeout(None)

    self.send("PASS %s\r\n" % self.settings['password'])
    self.send("USER %s\r\n" % self.settings['username'])
    self.send("NICK %s\r\n" % self.settings['username'])

    if not self.check_login_status(self.recv()):
      print("[ERROR] IRC credentials not accepted")
      sys.exit()
    else:
      print("[LOG] Connected to twitch.tv")
      self.send("JOIN %s\r\n" % self.settings['channel'])
      print("[LOG] Connected to channel %s" % self.settings['channel'])

      print(sock.recv(1024))

  def check_login_status(self, data):
    if not re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data): return True

  def check_has_message(self, data):
    return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$', data)
  
  def parse_message(self, data):
    return {
      'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0],
      'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', data)[0],
      'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0]
    }

  def ping(self, data):
    if data.startswith('PING'):
      self.send(data.replace('PING', 'PONG')) 

  def send(self, msg):
    return self.sock.send(msg.encode())

  def recv(self, amount=1024):
    return self.sock.recv(amount).decode()

  def recv_messages(self, amount=1024):
    data = self.recv(amount)

    if not data:
      print('Lost connection, reconnecting.')
      return self.set_socket_object()

    self.ping(data)

    if self.check_has_message(data):
      return [self.parse_message(line) for line in filter(None, data.split('\r\n'))]

    return