from reader.models import *

def Account_validation( Login , Password):

    Users = User.query.order_by(User.first_name.desc()).paginate()
    key = 0

    for user in Users.items:
        if Login == user.login:
           key = user.user_id
    
    if key == 0:
        message = "пользователя не существует"
        succses = False
        return [message,succses]
    
    Users = User.query.where(User.user_id == key).paginate()
    user = Users.items
    if Password != user[0].password:
        message = "неправильный пароль"
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
    

     