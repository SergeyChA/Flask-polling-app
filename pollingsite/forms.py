from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired, Email, Length


class Base(FlaskForm):
    email = EmailField('email', validators=[Email(), Length(min=6, max=30)])
    password = StringField(
        'password', validators=[DataRequired(), Length(min=6)]
    )


class FormSingup(Base):
    username = StringField(
        'username', validators=[DataRequired(), Length(min=6, max=30)]
    )


class FormLogin(Base):
    pass
