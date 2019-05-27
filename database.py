import pymongo

from constants import DATABASE_URL

# pymongo database setup
client = pymongo.MongoClient(DATABASE_URL)
db = client.development
message_details = db.message_details


def insert_update_msg_details(sender_id, timestamp, positive, negative):
    """This function inserts or updates the messages which include timestamp, positive, negative for a particular
     sender, sender_id is the _id of the collection

    database structure:
    {
   "_id":"000000000001212",
   "messages":[
      [
         {
            "timestamp":{
               "$date":{
                  "$numberLong":"1558895150655"
               }
            }
         },
         {
            "mood":{
               "negative":{
                  "$numberDouble":"0.24077"
               },
               "positive":{
                  "$numberDouble":"0.66739"
               }
            }
         }
      ]
   ]
}
     """
    message_details.update({'_id': sender_id}, {'$push': {'messages': {'timestamp': timestamp, 'positive': positive,
                                                                       'negative': negative}}}, upsert=True)
    return 'ok'
