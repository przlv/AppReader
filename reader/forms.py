from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from reader.models import Book

class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(),
                                             Length(min=5, max=100)])
    author = StringField('Автор', validators=[DataRequired(),
                                             Length(min=5, max=100)])
    genre = StringField('Жанр', validators=[DataRequired(),
                                             Length(min=5, max=20)])
    cover = FileField('Обложка книги', validators=[FileAllowed(['jpg', 'png'])])
    rating = IntegerField('Моя оценка', validators=[DataRequired(), NumberRange(min=1, max=5)])
    description = TextAreaField('Сюжет',
                                validators=[DataRequired(),
                                            Length(max=500)])
    notes = TextAreaField('Заметки',
                                validators=[DataRequired(),
                                            Length(max=500)])
    submit = SubmitField('Добавить')

    def validate_title(self, title):
        title = Book.query.filter_by(title=title.data).first()
        if title:
            raise ValidationError('Такая книга уже есть в списке прочитанных.')


class UpdateBook(FlaskForm):
    title = StringField('Название', validators=[DataRequired(),
                                             Length(min=5, max=100)])
    author = StringField('Автор', validators=[DataRequired(),
                                             Length(min=5, max=100)])
    genre = StringField('Жанр', validators=[DataRequired(),
                                             Length(min=5, max=20)])
    cover = FileField('Обложка книги', validators=[FileAllowed(['jpg', 'png'])])
    rating = IntegerField('Моя оценка', validators=[DataRequired(), NumberRange(min=1, max=5)])
    description = TextAreaField('Сюжет',
                                validators=[DataRequired(),
                                            Length(max=500)])
    notes = TextAreaField('Заметки',
                                validators=[DataRequired(),
                                            Length(max=500)])
    submit = SubmitField('Обновить')

class UserForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(),
                                             Length(min=1, max=50)])
    surname = StringField('Фамилия', validators=[DataRequired(),
                                             Length(min=1, max=50)])
    last_name = StringField('Отчество', validators=[DataRequired(),
                                             Length(min=1, max=50)])
    phone = StringField('Мобильный телефон', validators=[DataRequired(),
                                             Length(min=10, max=15)])
    zipcode = StringField('Почтовый индекс', validators=[DataRequired(),
                                             Length(min=1, max=10)])
    address = StringField('Адрес', validators=[DataRequired(),
                                             Length(min=1, max=50)])
    login = StringField('Логин', validators=[DataRequired(),
                                             Length(min=1, max=50)])
    password = StringField('Пароль', validators=[DataRequired(),
                                             Length(min=1, max=50)])
    submit = SubmitField('Обновить')
