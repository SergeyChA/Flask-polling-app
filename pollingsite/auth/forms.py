from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    ValidationError,
    BooleanField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
)
from pollingsite.models import User, db


class Base(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6)]
    )
    submit = SubmitField('Sing up')


class FormSingup(Base):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=3, max=30)]
    )
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')]
    )

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


class FormLogin(Base):
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
