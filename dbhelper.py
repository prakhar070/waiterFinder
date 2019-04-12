import pymongo
from bson.objectid import ObjectId

DATABASE = "waitercaller"

class DBHelper:
	def __init__(self):
		client = pymongo.MongoClient(connect=False)
		self.db = client[DATABASE]

	def get_user(self, email):
		return self.db.users.find_one({"email":email})

	def add_user(self, email, salt, hashed):
		self.db.users.insert({"email": email, "salt":salt, "hashed": hashed})

	#adding new table based on the table number entered by the owner
	def add_table(self, number, owner):
		new_id = self.db.tables.insert({"number": number, "owner":owner})
		return new_id

	#updating table to add the url part to the document
	def update_table(self, _id, url):
		self.db.tables.update({"_id":_id}, {"$set":{"url":url}})

	#returing a list of tables owned by an owner
	def get_tables(self, owner_id):
		return list(self.db.tables.find({"owner":owner_id}))

	#returing a single table based upon the table id
	def get_table(self, table_id):
		return self.db.tables.find_one({"_id":ObjectId(table_id)})

	#deleting a table from the collection
	def delete_table(self, table_id):
		self.db.tables.remove({"_id": ObjectId(table_id)}) 

	#adding request as sent by the user based upon the table id
	def add_request(self, table_id, time):
		table = self.get_table(table_id)
		self.db.requests.insert({"owner": table['owner'], "table_number": table['number'], "table_id": table_id, "time":time})

	#fetching all the requests to display on the dashboard
	def get_requests(self, owner_id):
		return list(self.db.requests.find({"owner":owner_id}))

	#deleting a request based upon the requestid
	def delete_request(self, request_id):
		self.db.requests.delete({"_id":ObjectId(request_id)})

