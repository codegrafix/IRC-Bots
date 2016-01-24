from time import gmtime, strftime

from pymongo import MongoClient


class SoccerDB:
    name = ''
    client = None
    db = None
    player_collection = None
    game_collection = None

    def __init__(self):
        self.client = MongoClient('mongodb://')
        if not self.client:
            print "No Database found."
        self.db = self.client['test_db']
        # Create collections
        self.player_collection = self.db['player_stats']
        self.game_collection = self.db['game_stats']

    def create_player(self, name):
        if self.player_collection.find({"player": name}).count() == 0:
            print "Create player %s of %s" % (name, self.player_collection.find({"player": name}).count())
            lost = 0
            won = 0
            player_stats = {"player": name,
                            "lost": lost,
                            "won": won}
            self.player_collection.insert_one(player_stats).inserted_id
        assert isinstance(name, object)
        print 'Player %s already exists!' % name

    def update_score(self, names, winner):
        for name in names:
            if len(name) < 4:
                return

            self.create_player(name)
            if winner:
                result = self.player_collection.update(
                        {'player': name},
                        {'$inc': {'won': +1, "metrics.orders": 1}}
                )
            elif not winner:
                result = self.player_collection.update(
                        {'player': name},
                        {'$inc': {'lost': +1, "metrics.orders": 1}}
                )
            if not result['updatedExisting']:
                print "Could not update score. Player %s not found." % name

            cursor = self.player_collection.find({"player": name})
            for value in cursor:
                print 'UpdateScore of player ' + name + ' - lost: ' + str(value["lost"]) + ' won: ' + str(value["won"])
                # print str(result)

    def update_gameinfo(self, winner, loser):
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        info_string = '@ ' + time + ' ' + ' '.join(winner) + ' [Won] | ' + ' '.join(loser) + ' [Lost]'

        if self.game_collection.find({"gameinfo": "team1"}).count() == 0:
            print 'Create gameinfo object: ' + info_string
            game_stats = {"gameinfo": 'team1',
                          "lastgames": [info_string]}
            self.game_collection.insert_one(game_stats).inserted_id
        else:
            print 'Add new gameinfo object: ' + info_string
            result = self.game_collection.update(
                    {"gameinfo": 'team1'},
                    {'$push': {'lastgames': info_string}}
            )

    def set_score(self, name, score, winner_type):
        self.create_player(name)
        win_type = ""
        if winner_type:
            win_type = 'won'
        else:
            win_type = 'lost'
        result = self.player_collection.update(
                {'player': name},
                {'$set': {win_type: int(score)}}
        )
        if not result['updatedExisting']:
            print "Could not set score. Player %s not found." % name

    def get_last_games(self, nr_of_games):
        print 'Get last games... ' + str(nr_of_games)
        try:
            output_string = ''
            counter = 0
            for document in self.game_collection.find().sort('lastgames', 1):
                for line in reversed(document['lastgames']):
                    if counter >= nr_of_games:
                        print output_string
                        break;
                    else:
                        output_string += line + '\r\n'
                        counter += 1
                return output_string

        except ValueError:
            print "Value Error"

    def get_stats(self, show_winner):
        try:
            output_string = ""
            if show_winner:
                output_string = "Current winner stats:\n"
                for document in self.player_collection.find().sort("won", -1):
                    assert isinstance(document, object)
                    output_string += document['player'] + ': ' + str(document['won']) + '\r\n'
            else:
                output_string = "Current loser stats:\n"
                for document in self.player_collection.find().sort("lost", -1):
                    assert isinstance(document, object)
                    output_string += document['player'] + ': ' + str(document['lost']) + '\r\n'
            return output_string
        except ValueError:
            print "Value Error"
