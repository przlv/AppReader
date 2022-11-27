import os, secrets
from reader import app, db
from reader.models import *
from flask import render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from PIL import Image
from reader.forms import *
from sqlalchemy.exc import IntegrityError
from random import randrange

@app.route('/')
def index():
   bookss = Book.query.order_by(Book.title.desc()).paginate()
   return render_template('index.html', books_list = bookss)

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

def save_picture(cover):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(cover.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], picture_fn)

    output_size = (300, 300)
    i = Image.open(cover)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

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
#     book = Book.query.get_or_404(book_id)authorss
#     db.session.delete(book)
#     db.session.commit()
#     return redirect(url_for('index'))    

# @app.route('/export/')
# def data():
#   data = Book.query.all()
#   return jsonify(data)  

@app.route('/authors/')
def authors():
    authorss = Author.query.order_by(Author.surname.desc()).paginate()
    return render_template('authors.html', authors_list = authorss)

@app.route('/menu/')
def menu():
    return render_template('menu.html')

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    id_user_current = 2
    user = User.query.get(id_user_current)
    if request.method == 'POST':
        form = UpdateUser(request.form)
        if form.validate_on_submit:
            user.first_name = form.first_name.data
            user.surname = form.surname.data
            user.last_name = form.last_name.data
            user.phone = form.phone.data
            user.address = form.address.data
            user.login = form.login.data
            user.password = form.password.data
            try:
                db.session.commit()
            except:
                db.session.rollback()
    return render_template('profile.html', user = user)

@app.route('/delivery/')
def delivery():
    id_user_current = 2
    current_user = User.query.get(id_user_current)
    current_delivery = Delivery.query.filter(Delivery.user_id == id_user_current).paginate()
    card_code = randrange(1000, 9999)
    return render_template('delivery.html', user = current_user, user_delivery=current_delivery.items, card_code = card_code)

@app.route('/preference/')
def preference():
    id_user_current = 2
    current_user = User.query.get(id_user_current)
    current_delivery = Delivery.query.filter(Delivery.user_id == id_user_current).paginate()
    card_code = randrange(1000, 9999)
    return render_template('preference.html', user = current_user, user_delivery=current_delivery.items, card_code = card_code)

@app.route('/admin-sklad/')
def admin_sklad():
    books = Book.query.order_by(Book.title.desc()).paginate()
    return render_template('admin_sklad.html', books=books.items)


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/admin-add-book/', methods=['GET', 'POST'])
def admin_add_book():
    if request.method == 'POST':
        formbook = BookForm(request.form)
        # if formbook.cover.data:
        #     formbook.cover.data = save_picture(formbook.cover.data)
        # else:
        #     formbook.cover.data ='default.jpg'
        
        new_book = Book(
            # book_id= formbook.book_id.data,
            title= formbook.title.data,
            cover= 'default.jpg',
            rating= formbook.rating.data,
            description= formbook.description.data,
            created_at = formbook.created_at.data,
            year_publication= formbook.year_publication.data,
            price= formbook.price.data,
            sale= formbook.sale.data,
            weight= formbook.weight.data,
            page_count= formbook.page_count.data,
            price_type= formbook.price_type.data,
            library_text= formbook.library_text.data,
            affinity= formbook.affinity.data,
            count= formbook.count.data,
            # author_id= formbook.author_id.data,
            # genre= formbook.genre.data,
            # publish_id = formbook.publish_id.data,
            # type_id = formbook.type_id.data,
            # level_id= formbook.level_id.data      
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('admin_sklad'))

    elif request.method == 'GET':
        return render_template('admin-add-book.html')