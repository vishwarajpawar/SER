from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Length,Email, ValidationError
from app.dbmodels import User

class SignUp(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    email = StringField(label="Email: ",validators=[Email(), DataRequired()])
    username = StringField(label="User Name: ", validators=[Length(min=3, max=30), DataRequired()])
    firstname = StringField(label="First Name: ",validators=[Length(min=2,max=60), DataRequired()])
    lastname = StringField(label="Last Name: ", validators=[Length(min=2, max=60), DataRequired()])
    password1 = PasswordField(label="Password: ",validators=[Length(min=6, ), DataRequired()])
    submit = SubmitField(label="Sign Up")
    
class SignIn(FlaskForm):
    username = StringField(label="User Name: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")