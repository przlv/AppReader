import os, secrets
from reader import app, db
from reader.models import *
from flask import render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from PIL import Image
from reader.forms import *
from reader.validator import *
from sqlalchemy.exc import IntegrityError
from random import randrange
import datetime

current_user = -1

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

@app.route('/account/', methods=('GET', 'POST'))
def account():
    global current_user
    form = UserForm(request.form)
    if request.method == "GET":
        if current_user != -1:
            return render_template('menu.html')
        else:
            return render_template('account.html', form=form)
    
    if request.method == "POST":
        if form.validate_on_submit:
            Login = form.login.data
            Password = form.password.data
            result_valid = Account_validation(Login,Password)
            
            if result_valid[1] == True:
                user = User.query.get(result_valid[0])
                user.Auth = 1
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                current_user = user.user_id
                return render_template('menu.html')
            else:
                return render_template('account.html', error=result_valid[0]) 

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
    # db.session.delete(book)
    # db.session.commit()
    # return redirect(url_for('index'))    

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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = User.query.get(current_user)
    if request.method == 'POST':
        form = UserForm(request.form)
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
    user = User.query.get(current_user)
    current_delivery = Delivery.query.filter(Delivery.user_id == user.user_id).paginate()
    card_code = randrange(1000, 9999)
    return render_template('delivery.html', user = user, user_delivery=current_delivery.items, card_code = card_code)

@app.route('/preference/')
def preference():
    user = User.query.get(current_user)
    current_delivery = Delivery.query.filter(Delivery.user_id == user.user_id).paginate()
    card_code = randrange(1000, 9999)
    return render_template('preference.html', user = user, user_delivery=current_delivery.items, card_code = card_code)

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
        if request.files['cover']:
            file = request.files['cover']
            filepath = ''
            filepath = '/'.join(['reader/uploads',file.filename])
            file.save(filepath)
            cover = file.filename
        else:
            cover = 'default.jpg'
        new_book = Book(
            title= formbook.title.data,
            cover= cover,
            rating= formbook.rating.data,
            description= formbook.description.data,
            created_at = datetime.datetime.today(),
            year_publication= formbook.year_publication.data,
            price= formbook.price.data,
            sale= formbook.sale.data,
            weight= formbook.weight.data,
            page_count= formbook.page_count.data,
            price_type= formbook.price_type.data,
            library_text= formbook.library_text.data,
            affinity= formbook.affinity.data,
            count= formbook.count.data,
            author_id= formbook.author_id.data,
            genre= formbook.genre.data,
            publish_id = formbook.publish_id.data,
            type_id = 1,
            level_id= formbook.level_id.data      
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('admin_sklad'))

    elif request.method == 'GET':
        return render_template('admin-add-book.html')

@app.route('/exit/')
def exit():
    global current_user
    current_user = -1
    return render_template('account.html')

@app.route('/deletebook/<int:book_id>')
def deletebook(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('admin_sklad'))

@app.route('/editbook/<int:book_id>', methods=['GET', 'POST'])
def editbook(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'GET':
        return render_template('admin-edit-book.html', book=book)
    elif request.method == 'POST':
        formbook = BookForm(request.form)
        if request.files['cover']:
            file = request.files['cover']
            filepath = ''
            filepath = '/'.join(['reader/uploads',file.filename])
            file.save(filepath)
            cover = file.filename
        else:
            cover = book.cover
        book.title= formbook.title.data
        book.cover= cover
        book.rating= formbook.rating.data
        book.description= formbook.description.data
        book.year_publication= formbook.year_publication.data
        book.price= formbook.price.data
        # book.sale= formbook.sale.data
        book.weight= formbook.weight.data
        book.page_count= formbook.page_count.data
        # book.price_type= formbook.price_type.data
        book.library_text= formbook.library_text.data
        book.affinity= formbook.affinity.data
        book.count= formbook.count.data
        book.author_id= formbook.author_id.data
        book.genre= formbook.genre.data
        book.publish_id = formbook.publish_id.data
        book.type_id = 1
        book.level_id= formbook.level_id.data
        db.session.commit()
        return redirect(url_for('admin_sklad'))

@app.route('/admin-users/')
def admin_users():
    users = User.query.order_by(User.first_name.desc()).paginate()
    return render_template('admin_user_control.html', users=users.items)

@app.route('/admin-authors/')
def admin_authors():
    authors = Author.query.order_by(Author.first_name.desc()).paginate()
    return render_template('admin_authors_control.html', authors=authors.items)