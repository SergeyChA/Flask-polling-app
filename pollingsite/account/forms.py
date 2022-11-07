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
from flask_login import current_user


class FormAccountUpdate(FlaskForm):
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
    email = StringField(
        'Почта',
        validators=[
            DataRequired(message='Введите почту'),
            Email(message='Неверная почта')]
    )
    picture = FileField(
        'Изменить фото',
        validators=[
            FileAllowed(
                ['jpg', 'png'],
                message='Формат изображения только jpg, png')
        ]
    )
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = db.session.execute(
                db.select(User).filter(User.username == username.data)
            ).scalar()
            if user:
                raise ValidationError('Такое имя уже занято')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = db.session.execute(
                db.select(User).filter(User.email == email.data)
            ).scalar()
            if user:
                raise ValidationError('Такая почта уже занята')
