import os, secrets
from reader import app, db
from reader.models import Book
from flask import render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from PIL import Image
from reader.forms import BookForm, UpdateBook
from sqlalchemy.exc import IntegrityError

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)    

# @app.route('/<int:book_id>/')
# def book(book_id):
#     book = Book.query.get_or_404(book_id)
#     return render_template('book.html', book=book)      

@app.route('/genre/')
def genre():
    page = request.args.get('page', 1, type=int)
    books = Book.query.filter(Book.genre == 'триллер').paginate(page=page, per_page=6)
    return render_template('genre.html', books=books)

@app.route('/account/')
def account():
    page = request.args.get('page', 1, type=int)
    books = Book.query.filter(Book.rating > 4).paginate(page=page, per_page=6)
    return render_template('account.html', books=books)      

# def save_picture(cover):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(cover.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], picture_fn)

#     output_size = (220, 340)
#     i = Image.open(cover)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     return picture_fn

# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     form = BookForm()
#     if form.validate_on_submit():
#         if form.cover.data:
#             cover = save_picture(form.cover.data)
#         else:
#             cover ='default.jpg'   
#         title = form.title.data
#         author = form.author.data
#         genre = form.genre.data
#         rating = int(form.rating.data)
#         description = form.description.data
#         notes = form.notes.data
#         book = Book(title=title,
#             author=author,
#             genre=genre,
#             rating=rating,
#             cover=cover,
#             description=description,
#             notes=notes)
#         db.session.add(book)
#         db.session.commit()
#         return redirect(url_for('index'))

    # return render_template('create.html', form=form)

# @app.route('/<int:book_id>/edit/', methods=('GET', 'POST'))
# def edit(book_id):
#     book = Book.query.get_or_404(book_id)
#     form = UpdateBook()
#     if form.validate_on_submit():
#         if form.cover.data:
#             cover = save_picture(form.cover.data)
#         else:
#             cover = book.cover
#         book.title = form.title.data
#         book.author = form.author.data
#         book.genre = form.genre.data
#         book.rating = int(form.rating.data)
#         book.description = form.description.data
#         book.notes = form.notes.data
#         try:
#             db.session.commit()
#             return redirect(url_for('index'))
#         except IntegrityError:
#             db.session.rollback()
#             flash('Произошла ошибка: такая книга уже есть в базе', 'error')
#             return render_template('edit.html', form=form)
      
            
#     elif request.method == 'GET':
#         form.title.data = book.title
#         form.author.data = book.author
#         form.genre.data = book.genre
#         form.rating.data = book.rating
#         form.cover.data = book.cover
#         form.description.data = book.description
#         form.notes.data = book.notes

#     return render_template('edit.html', form=form)      

# @app.post('/<int:book_id>/delete/')
# def delete(book_id):
#     book = Book.query.get_or_404(book_id)
#     db.session.delete(book)
#     db.session.commit()
#     return redirect(url_for('index'))    

# @app.route('/export/')
# def data():
#   data = Book.query.all()
#   return jsonify(data)  

@app.route('/authors/')
def authors():
    return render_template('authors.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')

#test
@app.route('/about/')
def about():
    return render_template('about.html')