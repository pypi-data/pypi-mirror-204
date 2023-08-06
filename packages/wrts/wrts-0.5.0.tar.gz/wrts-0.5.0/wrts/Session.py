from .types.Question import Question
from .types.Subject import Subject
from .types.Notif import Notif
import requests, json, platform

class LoginFailure(Exception):
	pass

class QuestionFailure(Exception):
	pass

class UploadError(Exception):
	pass

class Session:
	loggedin = False
	renew = 0
	expiration = 0
	token = ""
	subjects = None
	def __init__(self, user, passwd):
		self._login(user, passwd)
		self.subjects = self.give_subject_generator()
	def give_subject_generator(self):
		def generator(subjects, token):
			for subject in subjects:
				yield Subject(subject, token)
		resp = requests.get("https://api.wrts.nl/api/v3/subjects",headers={"x-auth-token": self.token}).json()
		return generator(resp["subjects"], self.token)
	def _login(self, user, passwd):
		resp = requests.post("https://api.wrts.nl/api/v3/auth/get_token", json={"email": user, "password": passwd}).json()
		#print(resp)
		if not resp["success"]:
			raise LoginFailure(resp["info"])
		self.loggedin = True
		self.renew = resp["renew_from"]
		self.expiration = resp["expires_at"]
		self.token = resp["auth_token"]
	def upload(self, path, mimetype="image/png"):
		f = open(path, "rb")
		data = f.read()
		f.close()
		Sep = "/"
		if platform.system() == "Windows": Sep = "\\"
		resp = requests.get("https://api.wrts.nl/api/v3/qna/questions/presigned_image_url", headers={"x-auth-token": self.token}).json()
		stat = requests.put(resp["signed_url"],headers={"x-auth-token":self.token,"Content-type":mimetype},data=data).status_code
		if stat == 200:
			return {"file_name": path.split(Sep)[-1], "image": resp["signed_url"].split("?")[0]}
		else:
			raise UploadError(f"Failed to upload {path}")
	def get_notifs(self, page, per_page=10):
		def generator(objs, token):
			for obj in objs:
				yield Notif(obj, token)
		resp = requests.get(f"https://api.wrts.nl/api/v3/users/notifications?page={page}&per_page={per_page}", headers={"x-auth-token": self.token}).json()
		return resp["total_count"], generator(resp["notifications"],self.token)
	def get_questions(self):
		resp = requests.get("https://api.wrts.nl/api/v3/public/qna/questions", headers={"x-auth-token": self.token}).json()
		def gen(questions, token):
			for q in questions:
				yield Question(q["id"],self.token)
		return resp["total_count"], gen(resp["results"], self.token)
	def get_question(self, id):
		return Question(id, self.token)
	def post_question(self, contents, subject, topic=None, attachments=[]):
		data = {"contents": contents, "subject_id": subject.id, "qna_attachments_attributes": attachments}
		if not topic == None:  data["topic_id"] = topic.id
		resp = requests.post("https://api.wrts.nl/api/v3/qna/questions",headers={"x-auth-token": self.token},json=json.dumps({"qna_question":data})).json()
		if "success" in resp:
			raise QuestionFailure(resp["error"])
		return self.get_question(resp["qna_question"]["id"])
