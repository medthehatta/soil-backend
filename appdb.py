import pymongo


def default_db():
    client = pymongo.MongoClient()
    return client.get_database("soil")


# FIXME
# For experimentaiton purposes, just make this global for now
db = default_db()


def get_player_inventory():
    return list(db.player_inventory.find({}))
