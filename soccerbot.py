from ircbot import IrcBot


class SoccerBot(IrcBot):
    """ A game stats bot for daily table soccer matches.
    """

    def show_stats(self,arg):
        print 'Show stats' + arg

    def change_topic(self, arg):
        print 'Change Topic to: ' + arg
        self.send(('TOPIC %s %s\r' % (self.channel_, arg)))

    # Command dictionary
    command_dict = {
        ':!topic ': change_topic,
        ':!stats ': show_stats,
    }

    def handle_message(self, message):
        if len(message):
            for command in self.command_dict:
                for line in message:
                    if command in line:
                        param = line.split(command)[1]
                        print 'handle command: ' + command + param
                        self.command_dict[command](self, param)


# Create and connect
my_bot = SoccerBot("SoccerBot", "boomer.qld.au.starchat.net", 6667)
my_bot.connect('#thisisatestchan')
my_bot.message('I am here!')

while 1:
    # Loop mandatory function to keep connection with server,alive!
    # return message for further processing
    message = my_bot.get_message
    my_bot.handle_message(message)
