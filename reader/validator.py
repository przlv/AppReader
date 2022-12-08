from reader.models import *

def Account_validation( Login , Password):

    Users = User.query.order_by(User.first_name.desc()).paginate()
    key = 0

    for user in Users.items:
        if Login == user.login:
           key = user.user_id
           break
    
    if key == 0:
        message = "Пользователя не существует"
        succses = False
        return [message,succses]
    
    Users = User.query.where(User.user_id == key).paginate()
    user = Users.items
    if Password != user[0].password:
        message = "Неправильный пароль"
        succses = False
        return [message,succses]
    else:
        user[0].Auth = 1
        try:
            db.session.commit()
        except:
            db.session.rollback()
        succses = True
        return [key,succses]
    
def Registation_validation(Login , Password , Email):

    Users = User.query.order_by(User.first_name.desc()).paginate()
    error = ''
    succsess = True
    for user in Users.items:
        if Login == user.login:
           succsess = False
           error = 'Пользователь с таким логином уже существует'
           break
    for user in Users.items:
        if Email == user.email:
           succsess = False
           error = error +' '+ Email+' уже существует в базе'
           break

    if succsess == False:
        checkbox = 'off'
        return [succsess,error,checkbox]
    else:
        succsess = True
        return [succsess]
