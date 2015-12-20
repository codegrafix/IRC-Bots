from ircbot import IrcBot


class SoccerBot(IrcBot):
    """ A simple irc bot which handles basic irc server connection
    """

    def show_stats(self):
        print 'Show stats'


    def change_topic(self, argument):
        print 'Change Topic'
        self.command("TOPIC " + self.channel_ + " " + str_split [1] + "\n")

    # Command dictionary
    command_dict = {
        ':!topic ': change_topic,
        ':!stats ': show_stats,
    }

    def handle_command(self, message):
        for command in self.command_dict:
            if command in message:
                self.command_dict[command](self)


# Create and connect
my_bot = SoccerBot("SoccerBot", "boomer.qld.au.starchat.net", 6667)
my_bot.connect('#thisisatestchan')
my_bot.message('I am here!')

while 1:
    # Loop mandatory function to keep connection with server,alive!
    # return message for further processing
    message = my_bot.get_message
    my_bot.handle_command(message)