from ircbot import IrcBot
from mongodb import SoccerDB


class SoccerBot(IrcBot):
    """ A game stats bot for daily table soccer matches.
    """

    db = SoccerDB()

    def show_stats(self, arg):
        # print 'Show stats' +
        message = self.db.get_stats
        self.message(message)

    def change_topic(self, arg):
        print 'Change Topic to: ' + arg
        self.send(('TOPIC %s %s\r' % (self.channel_, arg)))

    def score(self, arg):
        print '%s have lost...' % arg
        names = arg.split(' ')
        self.db.update_score(names)
        self.show_stats("")

    def set_score(self, arg):
        try:
            name, value = arg.split(' ')
        except ValueError:
            print "Input not correct!"
            return
        print 'Set score of %s to %s' % (name, value)
        self.db.set_score(name,value)
        self.show_stats("")

    # Command dictionary
    command_dict = {
        ':!topic ': change_topic,
        ':!stats': show_stats,
        ':!score ': score,
        ':!set ': set_score,
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
