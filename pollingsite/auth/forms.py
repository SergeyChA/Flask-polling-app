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
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Пароль', validators=[DataRequired(), Length(min=6)]
    )
    submit = SubmitField('Регистрация')


class FormSingup(Base):
    username = StringField(
        'Имя', validators=[DataRequired(), Length(min=3, max=30)]
    )
    confirm_password = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')]
    )

    def validate_username(self, username):
        user = db.session.execute(
            db.select(User).filter(User.username == username.data)
        ).scalar()
        if user:
            raise ValidationError('Такое имя уже занято')

    def validate_email(self, email):
        user = db.session.execute(
            db.select(User).filter(User.email == email.data)
        ).scalar()
        if user:
            raise ValidationError('Такая почта иже занята')


class FormLogin(Base):
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
