from ircbot import IrcBot


class SeaWolf(IrcBot):
    """ A stupid bot.
    """

    def notify(self, args):
        try:
            self.send('NAMES #test')
        except ValueError:
            print "Input not correct!"
            return

    # Command dictionary
    command_dict = {
        ':!notify': notify,
    }
    super_user_command_dict = {
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

        print 'Message: %', message
        if command in self.super_user_command_dict:
            self.handle_dict_cmds(command, args, owner)

        if command in self.command_dict:
            self.command_dict[command](self, args)

my_bot = SeaWolf("SeaWolf", "boomer.qld.au.starchat.net", 6667)
my_bot.set_owner(':pabu!pabu@irc.tas')
my_bot.connect('#test')
my_bot.message('I am here!')

while 1:
    # Loop mandatory function to keep connection with server,alive!
    # return message for further processing
    my_bot.handle_message(my_bot.get_message)
