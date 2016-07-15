import socket
import logging


def findcommand(message, command):
    if message.find(command) != -1:
        return True


class IrcBot:
    """ A simple irc bot which handles basic irc server connection
    """
    irc_socket = None
    bot_name_ = ''
    server_ = ''
    port_ = 0
    channel_ = ''
    # List of owners
    bot_owners = []

    logging.basicConfig(level=logging.DEBUG, filename="ircbot.log", format="%(asctime)s - %(name)s - %(message)s",
                        datefmt="%H:%M:%S", filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
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

    def send(self, message):
        logging.info('Sent: ' + message)
        self.irc_socket.send(message + "\n")

    def message(self, output_message):
        lines = output_message.split("\n")
        for line in lines:
            logging.info('line: ' + line)
            self.irc_socket.send("PRIVMSG " + self.channel_ + " :" + line + '\r')

    def set_owner(self, arg):
        try:
            owners = arg.split(' ')
        except ValueError:
            print "Input not correct!"
            return
        assert isinstance(owners, object)
        print 'Old bot owners are: %s' % self.bot_owners
        if owners not in self.bot_owners:
            self.bot_owners.extend(owners)
            print 'New bot owners are: %s' % self.bot_owners

    # Mandatory function to keep connection alive.
    @property
    def get_message(self):
        irc_message = self.irc_socket.recv(2048)
        irc_message = irc_message.split('\r\n')

        for line in irc_message:
            if line is None:
                return
            if findcommand(line, " PRIVMSG "):
                try:
                    # Split irc message and command param
                    message = line.split(' ')
                    if len(message) >= 4:
                        output = message[0:4] + [' '.join(message[4:])]
                    else:
                        output = message[0:3].append(' ')
                    return output
                except ValueError:
                    print 'Could not handle message'

            elif findcommand(line, "PING "):
                logging.info(line)
                self.ping(line.split(' ')[1])
            else:
                logging.debug(line)

def main():
    # Create and connect
    my_bot = IrcBot("Bot", "boomer.qld.au.starchat.net", 6667)

    my_bot.set_owner(':newbie|2!kvirc@Star531723.dynamic.RZ.UniBw-Muenchen.de')
    my_bot.connect('#test')
    my_bot.message('I am here!')

    while 1:
        # Loop mandatory function to keep connection with server,alive!
        # return message for further processing
        my_bot.get_message
