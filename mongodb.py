from pymongo import MongoClient
import datetime


class SoccerDB:
    name = ''
    client = MongoClient('mongodb://localhost:27017/')

    db = client['test-database']
    collection = db['test-collection']
    posts = db.posts

    def create_player(self, name):
        if self.posts.find({"player": name}).count() == 0:
            print "Create player %s of %s" % (name, self.posts.find({"player": name}).count())
            score = 0
            post = {"player": name,
                    "score": score}
            self.posts.insert_one(post).inserted_id
        print 'Player %s already exists!' % name

    def update_score(self, names):
        for name in names:
            result = self.db.posts.update(
                    {'player': name},
                    {'$inc': {'score': +1, "metrics.orders": 1}}
            )
            if not result['updatedExisting']:
                print "Could not update score. Player %s not found." % name

            cursor = self.db.posts.find({"player": name})
            for value in cursor:
                print 'UpdateScore of player ' + name + ' - ' + str(value['score'])
            print str(result)

    def set_score(self, name, score):
        result = self.db.posts.update(
                {'player': name},
                {'$set': {'score': score}}
        )
        if not result['updatedExisting']:
            print "Could not set score. Player %s not found." % name

    def get_stats(self):
        cursor = self.db.posts.find().sort([('score', -1)])
        output_string = "Current stats:\n"
        # print "Current stats:"
        for document in cursor:
            assert isinstance(document, object)
            output_string += document['player'] + ': ' + str(document['score']) + '\n'
        print output_string
        return output_string


def unit_test():
    connection = SoccerDB()
    connection.create_player("pabu")
    connection.update_score({"pabu"})

    connection.get_stats()
    connection.set_score("bla", 200)