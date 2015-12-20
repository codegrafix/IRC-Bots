import socket


class IrcBot:
    """ A simple irc bot which handles basic irc server connection
    """
    bot_name_ = ''
    server_ = ''
    port_ = 0
    irc_socket = None

    def __init__(self, botname="stupid_bot", server="localhost", port=6667):
        self.bot_name_ = botname
        self.server_ = server
        self.port_ = port
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def join(self, chan):
        self.irc_socket.send('JOIN ' + chan + '\n')
        print 'join channel: ' + chan

    def ping(self):
        self.irc_socket.send("PONG :pingis\n")

    def connect(self, chan):
        assert isinstance(self.port_, object)
        print 'Connect to server: ' + self.server_ + ':' + str(self.port_)
        try:
            self.irc_socket.connect_ex((self.server_, self.port_))
        except socket.error as msg:
            self.irc_socket.close()
            self.irc_socket = None
        print 'Connected....'

        # Send irc auth
        self.irc_socket.send('USER ' + self.bot_name_ + " 2 3 " + self.bot_name_ + "\n")
        self.irc_socket.send('NICK ' + self.bot_name_ + "\n")
        self.join(chan)

    def findcommand(self, message, command):
        if message.find(' command ') != -1:
            return True

    # Mandatory function to keep connection alive.
    @property
    def stay_alive(self):
        message = self.irc_socket.recv(2048)
        message = message.strip('\n\r')
        print(message)

        if self.findcommand(message, "PING :"):
            self.ping()
        assert isinstance(message, object)
        return message

# Create and connect
mybot = IrcBot("bot", "boomer.qld.au.starchat.net", 6667)
mybot.connect('#thisisatestchan')

while 1:
    # Loop mandatory function to keep connection with server,alive!
    # return message for further processing
    mybot.stay_alive
