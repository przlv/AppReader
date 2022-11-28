from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, FloatField, DateField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from reader.models import Book

class BookForm(FlaskForm):
    book_id = IntegerField('ID книги', validators=[DataRequired()])
    title = StringField('Название', validators=[DataRequired(), Length(min=5, max=100)])
    rating = FloatField('Рейтинг', validators=[DataRequired(), NumberRange(min=0, max=5)])
    cover = FileField('Обложка книги', validators=[FileAllowed(['jpg', 'png'])])
    description = StringField('Описание', validators=[DataRequired(), Length(min=5, max=1000)])
    created_at = DateField('Дата добавления', format='%Y-%m-%d')
    year_publication = DateField('Название', format='%Y-%m-%d')
    price = FloatField('Цена', validators=[DataRequired()])
    sale = BooleanField('Скидка', validators=[DataRequired()])
    weight = IntegerField('Вес', validators=[DataRequired()])
    page_count = IntegerField('Количество страниц', validators=[DataRequired()])
    price_type = BooleanField('Тип цены', validators=[DataRequired()])
    library_text = StringField('Библио-текст', validators=[DataRequired(), Length(min=5, max=1000)])
    affinity = StringField('Аффиляция', validators=[DataRequired(), Length(min=5, max=250)])
    count = IntegerField('Количество книг', validators=[DataRequired()])
    author_id = IntegerField('ID Автора', validators=[DataRequired()])
    genre = IntegerField('ID Жанра', validators=[DataRequired()])
    publish_id = IntegerField('ID Издательства', validators=[DataRequired()])
    type_id = IntegerField('Тип литературы', validators=[DataRequired()])
    level_id = IntegerField('ID Специализации', validators=[DataRequired()])
    submit = SubmitField('Добавить')

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
