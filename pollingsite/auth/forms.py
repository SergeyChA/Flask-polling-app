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
    email = StringField(
        'Почта',
        validators=[
            DataRequired(message='Введите почту'),
            Email(message='Неверная почта')]
    )
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message='Введите пароль'),
            Length(min=6, message='Пароль должен быть не менее 6 символов')
        ]
    )
    submit = SubmitField('Регистрация')


class FormSingup(Base):
    username = StringField(
        'Имя',
        validators=[
            DataRequired(message='Введите имя'),
            Length(
                min=3,
                max=30,
                message='Имя должно быть от 3 до 30 символов'
            )
        ]
    )
    confirm_password = PasswordField(
        'Повторите пароль',
        validators=[
            DataRequired(message='Повторите пароль'),
            EqualTo('password', message='Пароли не совпадают')
        ]
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
            raise ValidationError('Такая почта уже занята')


class FormLogin(Base):
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
