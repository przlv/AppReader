import os, secrets
from reader import app, db
from reader.models import *
from flask import render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from PIL import Image
from reader.forms import *
from reader.validator import *
from sqlalchemy.exc import IntegrityError
from random import randrange, choice
import datetime

from scripts import generate_quote


current_user = -1
delivery_price = 'Чтобы узнать, войдите в личный кабинет'
app.jinja_env.globals.update(generate_quote=generate_quote)

@app.route('/', methods=('GET', 'POST'))
def index():
    bookss = Book.query.order_by(Book.title.desc()).paginate()
    authors = Author.query.order_by(Author.surname.desc()).paginate()
    type = Type.query.order_by(Type.name.desc()).paginate()
    publish = Publish.query.order_by(Publish.name.desc()).paginate()
    level = Level.query.order_by(Level.name.desc()).paginate()
    genre = Genre.query.order_by(Genre.name.desc()).paginate()
    if request.method == 'GET':
        for book in bookss.items:
            feedbacks = Feedback.query.filter(Feedback.book_id == book.book_id).paginate()
            feedbacks = feedbacks.items
            if feedbacks:
                sumfeed = 0
                for feed in feedbacks:
                    sumfeed += feed.rating
                sumfeed /= len(feedbacks)

                edit_book = Book.query.get(book.book_id)
                edit_book.rating = round(sumfeed, 2)
                db.session.commit()
            else:
                edit_book = Book.query.get(book.book_id)
                edit_book.rating = 0
                db.session.commit()
    elif request.method == 'POST':
        form = request.form
        if not 'search' in form:
            filter_books = []
            for book in bookss.items:
                if form['rating'] != '':
                    if int(book.rating) != int(form['rating']):
                        continue
                if Genre.query.get(book.genre).name != form['genre'] and form['genre'] != '':
                    continue
                if form['price1'] != '' or form['price2'] != '':
                    if form['price1'] != '':
                        if float(form['price1']) > book.price:
                            continue
                    if form['price2'] != '':
                        if float(form['price2']) < book.price:
                            continue
                if (not (Author.query.get(book.author_id).surname in form['author'])) and form['author'] != '':
                    continue
                if Type.query.get(book.type_id).name != form['type'] and form['type'] != '':
                    continue
                if Publish.query.get(book.publish_id).name != form['publish'] and form['publish'] != '':
                    continue
                if Level.query.get(book.level_id).name != form['level'] and form['level'] != '':
                    continue
                filter_books.append(book.book_id)
            
            bookss.items = []
            for indx in filter_books:
                bookss.items.append(Book.query.get(indx))
        else:
            desired_text = form['search']
            filter_books = []
            if desired_text != '':
                for book in bookss.items:
                    if desired_text in book.title:
                        filter_books.append(book.book_id)
                        continue
                    if desired_text in book.description:
                        filter_books.append(book.book_id)
                        continue
                    try:
                        if desired_text in book.library_text:
                            filter_books.append(book.book_id)
                            continue
                        if desired_text in book.affinity:
                            filter_books.append(book.book_id)
                            continue
                    except:
                        continue
            bookss.items = []
            for indx in filter_books:
                bookss.items.append(Book.query.get(indx))    

    return render_template('index.html',
                            books_list = bookss,
                            authors=authors.items,
                            type=type.items,
                            publish=publish.items,
                            level=level.items,
                            genre=genre.items,)


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
    global current_user, delivery_price
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
                user.last_logon = datetime.datetime.today()
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                current_user = user.user_id
                delivery_price = int(User.query.get_or_404(current_user).zipcode[:3])
                if delivery_price < 200 or delivery_price > 600:
                    delivery_price += randrange(100, 200)
                else:
                    delivery_price += randrange(1,50)
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

@app.route('/authors/', methods=('GET', 'POST'))
def authors():
    authorss = Author.query.order_by(Author.surname.desc()).paginate()
    if request.method == "POST":
            form  = request.form
            desired_text = form['search']
            filter_authors = []
            if desired_text != '':
                for author in authorss.items:
                    if desired_text in author.first_name:
                        filter_authors.append(author.author_id)
                        continue
                    if desired_text in author.surname:
                        filter_authors.append(author.author_id)
                        continue
                    if desired_text in author.last_name:
                        filter_authors.append(author.author_id)
                        continue

            authorss.items = []
            for indx in filter_authors:
                authorss.items.append(Author.query.get(indx))    

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
    authors = Author.query.order_by(Author.surname.desc()).paginate()
    genres = Genre.query.order_by(Genre.name.desc()).paginate()
    publishes = Publish.query.order_by(Publish.name.desc()).paginate()
    levels = Level.query.order_by(Level.name.desc()).paginate()

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
            author_id= Author.query.filter(Author.first_name == request.form['author_id'].split(' ')[0]+' ').paginate().items[0].author_id,
            genre= Genre.query.filter(Genre.name == request.form['genre']).paginate().items[0].genre_id,
            publish_id = Publish.query.filter(Publish.name == request.form['publish_id']).paginate().items[0].publish_id,
            type_id = 1,
            level_id= Level.query.filter(Level.name == request.form['level_id']).paginate().items[0].Level_id     
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('admin_sklad'))

    elif request.method == 'GET':
        return render_template('admin-add-book.html', authors=authors.items, genres = genres.items, publishes=publishes.items, levels=levels.items)

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

@app.route('/<int:sort_id>')
def sort(sort_id):
   bookss = Book.query.order_by(Book.price.desc()).paginate()
   if sort_id == 1:
      bookss = Book.query.order_by(Book.price.asc()).paginate()
   if sort_id == 2:
      bookss = Book.query.order_by(Book.price.desc()).paginate()
   if sort_id == 3:
      bookss = Book.query.order_by(Book.rating.desc()).paginate()
   if sort_id == 4:
      bookss = Book.query.order_by(Book.rating.asc()).paginate()
   if sort_id == 5:
      bookss = Book.query.order_by(Book.title.asc()).paginate()
   if sort_id == 6:
      bookss = Book.query.order_by(Book.title.desc()).paginate()
   if sort_id == 7:
      bookss = Book.query.order_by(Book.year_publication.desc()).paginate()

   return render_template('index.html', books_list = bookss)

@app.route('/admin-users/')
def admin_users():
    users = User.query.order_by(User.first_name.desc()).paginate()
    return render_template('admin_user_control.html', users=users.items)

@app.route('/edituser/<int:user_id>', methods=['GET', 'POST'])
def edituser(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template('admin-edit-user.html', user=user)
    elif request.method == 'POST':
        form = UserForm(request.form)
        user.first_name = form.first_name.data
        user.surname = form.surname.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.zipcode = form.zipcode.data
        user.address = form.address.data
        user.login = form.login.data
        user.password = form.password.data
        user.UserType = form.UserType.data

        db.session.commit()
        return redirect(url_for('admin_users'))

@app.route('/deleteuser/<int:user_id>')
def deleteuser(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_users'))

@app.route('/admin-authors/')
def admin_authors():
    authors = Author.query.order_by(Author.first_name.desc()).paginate()
    return render_template('admin_authors_control.html', authors=authors.items)

@app.route('/editauthors/<int:author_id>', methods=['GET', 'POST'])
def editauthors(author_id):
    author = Author.query.get_or_404(author_id)
    if request.method == 'GET':
        return render_template('admin-edit-author.html', author=author)
    elif request.method == 'POST':
        form = AuthorForm(request.form)
        if request.files['cover']:
            file = request.files['cover']
            filepath = ''
            filepath = '/'.join(['reader/uploads',file.filename])
            file.save(filepath)
            cover = file.filename
        else:
            cover = author.cover
        author.first_name = form.first_name.data
        author.surname = form.surname.data
        author.last_name = form.last_name.data
        author.cover = cover

        db.session.commit()
        return redirect(url_for('admin_authors'))

@app.route('/deleteauthors/<int:author_id>')
def deleteauthors(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('admin_authors'))

@app.route('/admin-add-author/', methods=['GET', 'POST'])
def admin_add_author():
    if request.method == 'POST':
        form = AuthorForm(request.form)
        if request.files['cover']:
            file = request.files['cover']
            filepath = ''
            filepath = '/'.join(['reader/uploads',file.filename])
            file.save(filepath)
            cover = file.filename
        else:
            cover = 'default.jpg'
        new_author = Author(
            first_name = form.first_name.data,
            surname = form.surname.data,
            last_name = form.last_name.data,
            cover = cover,
        )
        db.session.add(new_author)
        db.session.commit()
        return redirect(url_for('admin_authors'))

    elif request.method == 'GET':
        return render_template('admin-add-author.html')

@app.route('/viewbook/<int:book_id>')
def viewbook(book_id):
    book = Book.query.get_or_404(book_id)
    genres = Genre.query.filter(Genre.genre_id == book.genre).paginate()
    publish = Publish.query.filter(Publish.publish_id == book.publish_id).paginate()
    typee = Type.query.filter(Type.type_id == book.type_id).paginate()
    feedback = Feedback.query.filter(Feedback.book_id == book_id).paginate()
    users = User.query.order_by(User.user_id.asc()).paginate()
    if not type(delivery_price) == int: str(delivery_price)+' ₽' 
    return render_template('viewbook.html', book=book,
                            genre = genres.items[0].name,
                            rating_int = int(book.rating),
                            publish = publish.items[0].name,
                            typee = typee.items[0].name,
                            user_id = current_user,
                            feedback = feedback.items,
                            users = users.items,
                            delivery_price = delivery_price
                            )

@app.route('/buybook', methods= ['POST'])
def buybook():
    jsdata = request.form['javascript_data']
    book_id = int(jsdata)
    book = Book.query.get_or_404(book_id)
    new_buy = Delivery(
        date= datetime.datetime.today(),
        count= 1,
        description= book.title,
        weight= book.weight,
        user_id=current_user,
        price=book.price+delivery_price,
    )
    db.session.add(new_buy)
    book.count -= 1
    db.session.commit()

    deliverys = Delivery.query.filter(Delivery.user_id == current_user).paginate()
    
    list_added = {}
    deliverys = deliverys.items
    for deliv in deliverys:
        reg_date = f'{deliv.date.year}-{deliv.date.month}-{deliv.date.day}'
        if not reg_date in list_added:
            list_added[reg_date] = []
        list_added[reg_date].append(deliv)
    
    for key, group in list_added.items():
        if len(group) > 1:
            count = 0
            description =''
            weight = 0
            price = 0
            for item in group:
                count += item.count
                description += item.description +'; '
                weight += item.weight
                price += item.price
            
            for item in group:
                delivery = Delivery.query.get_or_404(item.delivery_id)
                db.session.delete(delivery)
            db.session.commit()

            new_buy = Delivery(
                            date= group[0].date,
                            count= count,
                            description= description,
                            weight = weight,
                            user_id=current_user,
                            price=price,
                    )
            db.session.add(new_buy)
            db.session.commit()

    return {'ok':1}

@app.route('/cosmos/')
def cosmos():
    return render_template('cosmos.html')

@app.route('/feedlike/<int:book_id>/<int:rating>')
def feedlike(book_id, rating):
    feedback = Feedback.query.filter((Feedback.user_id == current_user)&(Feedback.book_id == book_id)).paginate()
    feedback = feedback.items
    if (not feedback) and (current_user!=-1):
        with open('reader/uploads/feedback.txt', encoding='utf-8') as file:
            txt = file.readlines()
        new_feed = Feedback(
            feedback_id = randrange(100,9999),
            comment= choice(txt),
            rating= rating,
            user_id= current_user,
            book_id= book_id,
        )
        db.session.add(new_feed)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/account/add-profile.html', methods=['GET', 'POST'])
def addprofile():
    form = UserForm(request.form)
    if request.method == "GET":
        return render_template('add-profile.html')
    if request.method == "POST":
        if form.validate_on_submit: 
            RedEmail = form.Regemail.data
            RegPass = form.Regpass.data
            Regname =  form.Regname.data
            result_valid = Registation_validation(Regname,RegPass,RedEmail)
            if result_valid[0] == True:
                new_User = User(
                    first_name = form.first_name.data,
                    surname = form.surname.data,
                    last_name = form.last_name.data,
                    last_logon = datetime.datetime.today(),
                    phone = form.phone.data,
                    zipcode = form.zipcode.data,
                    address = form.address.data,
                    email = form.Regemail.data,
                    login = form.Regname.data,
                    password = form.Regpass.data,
                    RegDate= datetime.datetime.today(),
                    UserType = "user",
                    Auth = 0
                )
                db.session.add(new_User)
                db.session.commit()
                return redirect(url_for('account'))
            else:
                return render_template('add-profile.html', Regerror=result_valid[1])

@app.route('/genreopen/<int:genre_id>')
def genreopen(genre_id):
    bookss = Book.query.filter(Book.genre == genre_id).paginate()
    authors = Author.query.order_by(Author.surname.desc()).paginate()
    type = Type.query.order_by(Type.name.desc()).paginate()
    publish = Publish.query.order_by(Publish.name.desc()).paginate()
    level = Level.query.order_by(Level.name.desc()).paginate()
    genre = Genre.query.order_by(Genre.name.desc()).paginate()

    return render_template('index.html',
                            books_list = bookss,
                            authors=authors.items,
                            type=type.items,
                            publish=publish.items,
                            level=level.items,
                            genre=genre.items,)

@app.route('/authoropen/<int:author_id>')
def authoropen(author_id):
    bookss = Book.query.filter(Book.author_id == author_id).paginate()
    authors = Author.query.order_by(Author.surname.desc()).paginate()
    type = Type.query.order_by(Type.name.desc()).paginate()
    publish = Publish.query.order_by(Publish.name.desc()).paginate()
    level = Level.query.order_by(Level.name.desc()).paginate()
    genre = Genre.query.order_by(Genre.name.desc()).paginate()

    return render_template('index.html',
                            books_list = bookss,
                            authors=authors.items,
                            type=type.items,
                            publish=publish.items,
                            level=level.items,
                            genre=genre.items,)
