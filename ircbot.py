import socket


class IrcBot:
    """ A simple irc bot which handles basic irc server connection
    """
    irc_socket = None
    bot_name_ = ''
    server_ = ''
    port_ = 0
    channel_ = ''

    def __init__(self, botname="stupid_bot", server="localhost", port=6667):
        self.bot_name_ = botname
        self.server_ = server
        self.port_ = port
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def join(self, channel):
        self.channel_ = channel
        self.irc_socket.send('JOIN ' + self.channel_ + '\n')
        print 'join channel: ' + self.channel_

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

    def command(self, message):
        self.irc_socket.send(message)

    def message(self, output_message):
        self.irc_socket.send("PRIVMSG " + self.channel_ + " :" + output_message + "\n")


    # Mandatory function to keep connection alive.
    @property
    def get_message(self):
        message = self.irc_socket.recv(2048)
        message = message.strip('\n\r')
        print(message)

        if self.findcommand(message, "PING :"):
            self.ping()
        assert isinstance(message, object)
        return message


def main():
    # Create and connect
    my_bot = IrcBot("bot", "boomer.qld.au.starchat.net", 6667)
    my_bot.connect('#thisisatestchan')

    while 1:
        # Loop mandatory function to keep connection with server,alive!
        # return message for further processing
        my_bot.get_message
