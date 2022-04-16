from flask import current_app as app

class Message:

	def __init__(self, user_id, msg, ts):
		self.user_id = user_id
		self.content = msg
		self.ts = ts

	@staticmethod
	def get_messages(user_id):
		rows = app.db.execute('''
SELECT * 
FROM System_messages
WHERE user_id=:user_id
ORDER BY ts DESC
''',
					user_id=user_id)

		return [Message(*row) for row in rows]