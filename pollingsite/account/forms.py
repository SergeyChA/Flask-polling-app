from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError,
)
from pollingsite.models import User, db


class FormAccountUpdate(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField(
        'Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = db.session.execute(
            db.select(User).filter(User.username == username.data)
        ).scalar()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.'
            )

    def validate_email(self, email):
        user = db.session.execute(
            db.select(User).filter(User.email == email.data)
        ).scalar()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.'
            )