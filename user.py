#we will create user objects when correct set of password and username has been entered
class User:

	def __init__(self, email):
		self.email = email

	def get_id(self):
		return self.email

	def is_authenticated(self):
		return True

	def is_active(self):
		return True		

	def is_anonymous(self):     
		return False
