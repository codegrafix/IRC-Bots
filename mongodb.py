from pymongo import MongoClient
import datetime


class SoccerDB:
    name = ''
    client = None
    db = None
    collection = None
    tas_soccer = None

    def __init__(self):
        self.client = MongoClient('mongodb://')
        if not self.client:
            print "No Database found."
        self.db = self.client['tas_soccer']
        self.tas_soccer = self.db.tas_soccer

    def create_player(self, name):
        if self.tas_soccer.find({"player": name}).count() == 0:
            print "Create player %s of %s" % (name, self.tas_soccer.find({"player": name}).count())
            score = 0
            tas_soccer = {"player": name,
                          "score": score}
            self.tas_soccer.insert_one(tas_soccer).inserted_id
        assert isinstance(name, object)
        print 'Player %s already exists!' % name

    def update_score(self, names):
        for name in names:
            if len(name) < 4:
                return

            self.create_player(name)
            result = self.db.tas_soccer.update(
                    {'player': name},
                    {'$inc': {'score': +1, "metrics.orders": 1}}
            )
            if not result['updatedExisting']:
                print "Could not update score. Player %s not found." % name

            cursor = self.db.tas_soccer.find({"player": name})
            for value in cursor:
                print 'UpdateScore of player ' + name + ' - ' + str(value["score"])
            print str(result)

    def set_score(self, name, score):
        self.create_player(name)
        result = self.db.tas_soccer.update(
                {'player': name},
                {'$set': {'score': int(score)}}
        )
        if not result['updatedExisting']:
            print "Could not set score. Player %s not found." % name

    @property
    def get_stats(self):
        """
        :rtype: str
        """
        # print "Current stats:"
        try:
            output_string = "Current stats:\n"
            for document in self.db.tas_soccer.find().sort("score", -1):
                assert isinstance(document, object)
                output_string += document['player'] + ': ' + str(document['score']) + '\r\n'
            return output_string
        except ValueError:
            print "Value Error"


def unit_test():
    connection = SoccerDB()
    connection.create_player("pabu")
    connection.update_score({"pabu"})

    connection.get_stats
    connection.set_score("bla", 200)
