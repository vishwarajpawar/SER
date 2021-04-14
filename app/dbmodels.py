from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

  id = db.Column(db.Integer(), primary_key=True)
  email = db.Column(db.String(length=50), nullable=False, unique=True)
  username = db.Column(db.String(length=30), nullable=False, unique=True)
  first_name = db.Column(db.String(length=60), nullable=False)
  last_name = db.Column(db.String(length = 60), nullable=False)
  password_hash = db.Column(db.String(length = 60), nullable=False)
  historyofser = db.relationship('History', backref='owned_by', lazy=True)

  @property
  def password(self):
    return self.password
  
  @password.setter
  def password(self,plain_text_password):
    self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

  def check_password_correction(self,attempted_password):
    return bcrypt.check_password_hash(self.password_hash, attempted_password)


class History(db.Model):

  id = db.Column(db.Integer(), primary_key=True, unique=True)
  file_name = db.Column(db.String(length = 60), nullable=False)
  emotion = db.Column(db.String(length = 60), nullable=False)
  gender = db.Column(db.String(length = 60), nullable=False)
  data_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
  def __repr__(self):
    return f'History {self.id}'

