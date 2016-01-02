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

    def set_loser(self, arg):
        try:
            names = arg.split(' ')
        except ValueError:
            print "Input not correct!"
            return
        print '%s are losers...' % names
        self.db.update_score(names)
        self.show_stats("")

    def set_score(self, arg):
        try:
            name, value = arg.split(' ')
        except ValueError:
            print "Input not correct!"
            return
        print 'Set score of %s to %s' % (name, value)
        self.db.set_score(name, value)
        self.show_stats("")

    def owner(self, args):
        self.set_owner(args)

    # Command dictionary
    command_dict = {
        ':!topic': change_topic,
        ':!stats': show_stats,
    }
    super_user_command_dict = {
        ':!loser': set_loser,
        ':!set': set_score,
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


my_bot = SoccerBot("SoccerBot", "boomer.qld.au.starchat.net", 6667)
my_bot.set_owner(':newbie|2!kvirc@Star531723.dynamic.RZ.UniBw-Muenchen.de')
my_bot.connect('#thisisatestchan')
my_bot.message('I am here!')

while 1:
    # Loop mandatory function to keep connection with server,alive!
    # return message for further processing
    my_bot.handle_message(my_bot.get_message)
