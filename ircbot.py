import socket
import logging


class IrcBot:
    """ A simple irc bot which handles basic irc server connection
    """
    irc_socket = None
    bot_name_ = ''
    server_ = ''
    port_ = 0
    channel_ = ''

    logging.basicConfig(level=logging.INFO, filename="sfpin.log", format="%(asctime)s - %(name)s - %(message)s",
                        datefmt="%H:%M:%S", filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    def __init__(self, bot_name="stupid_bot", server="localhost", port=6667):
        self.bot_name_ = bot_name
        self.server_ = server
        self.port_ = port
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def join(self, channel):
        self.channel_ = channel
        self.send('JOIN ' + self.channel_)

    def ping(self, arg='hallo'):
        self.send('PONG %s' % arg)

    def connect(self, chan):
        assert isinstance(self.port_, object)
        message = 'Connect to server: ' + self.server_ + ':' + str(self.port_)
        logging.info(message)
        try:
            self.irc_socket.connect_ex((self.server_, self.port_))
        except socket.error as msg:
            self.irc_socket.close()
            self.irc_socket = None
        logging.info('Connected....')

        # Send irc auth
        self.send('USER ' + self.bot_name_ + " 2 3 " + self.bot_name_)
        self.send('NICK ' + self.bot_name_)
        # Respond to PING
        self.join(chan)

    def findcommand(self, message, command):
        if message.find(command) != -1:
            return True

    def send(self, message):
        logging.info('Sent: ' + message)
        self.irc_socket.send(message + '\n')

    def message(self, output_message):
        self.irc_socket.send("PRIVMSG " + self.channel_ + " :" + output_message)

    # Mandatory function to keep connection alive.
    @property
    def get_message(self):
        message = self.irc_socket.recv(2048)
        message = message.split('\r\n')

        for line in message:
            logging.debug(line)
            if self.findcommand(line, "PING "):
                self.ping(line.split(' ')[1])
        assert isinstance(message, object)
        return message


def main():
    # Create and connect
    my_bot = IrcBot("bot", "dreamhack.se.quakenet.org", 6667)
    my_bot.connect('#thisisatestchan')
    my_bot.join('#thisisatestchan')

    while 1:
        # Loop mandatory function to keep connection with server,alive!
        # return message for further processing
        my_bot.get_message
