from ircbot import IrcBot
from mongodb import SoccerDB


class SoccerBot(IrcBot):
    """ A game stats bot for daily table soccer matches.
    """

    db = SoccerDB()

    def show_winner(self, args=""):
        message = self.db.get_stats(True)
        self.message(message)

    def show_loser(self, args=""):
        message = self.db.get_stats(False)
        self.message(message)

    def last_games(self,args=""):
        message = self.db.get_last_games(9)
        self.message(message)

    def change_topic(self, arg):
        print 'Change Topic to: ' + arg
        self.send(('TOPIC %s %s\r' % (self.channel_, arg)))

    def set(self, arg):
        try:
            winner, loser = arg.split(' vs. ')
            winner = winner.split(' ')
            loser = loser.split(' ')
        except ValueError:
            print "Input not correct!"
            return
        self.db.update_score(loser, False)
        self.db.update_score(winner, True)
        self.db.update_gameinfo(winner, loser)
        self.show_loser()

    def set_winner(self, arg):
        self.set_score(arg, True)

    def set_loser(self, arg):
        self.set_loser(arg, False)

    def set_score(self, arg, winner_type):
        try:
            name, value = arg.split(' ')
        except ValueError:
            print "Input not correct!"
            return
        print 'Set score of %s to %s' % (name, value)
        if winner_type:
            self.db.set_score(name, value, winner_type)
            self.show_loser()
            self.show_winner()

    def owner(self, args):
        self.set_owner(args)

    # Command dictionary
    command_dict = {
        ':!topic': change_topic,
        ':!loser': show_loser,
        ':!winner': show_winner,
        ':!last': last_games,
    }
    super_user_command_dict = {
        ':!set': set,
        ':!setwinner': set_winner,
        ':!setloser': set_loser,
        ':!owner': owner,
    }

    def handle_dict_cmds(self, cmd, args, owner):
        try:
            if owner not in self.bot_owners:
                print owner + " does not have the rights."
                return
            print 'handle command: ' + cmd + ' ' + args
            self.super_user_command_dict[cmd](self, args)
        except ValueError:
            print 'Could not handle message. ValueError.'

    def handle_message(self, message):
        if message is None:
            return
        [owner, message_type, chan, command, args] = message

        print message
        if command in self.super_user_command_dict:
            self.handle_dict_cmds(command, args, owner)

        if command in self.command_dict:
            self.command_dict[command](self, args)

my_bot = SoccerBot("SoccerBot", "server", 6667)
my_bot.set_owner('')
my_bot.connect('#thisisatestchan')
my_bot.message('I am here!')

while 1:
    # Loop mandatory function to keep connection with server,alive!
    # return message for further processing
    my_bot.handle_message(my_bot.get_message)
