from app import db, login_manager
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    userData = Queries().get(user_id)
    user = User(userData[0], userData[1], userData[2])
    return user

class User(UserMixin):

    def __init__(self, id, username, password_hash, active=True):
        self.id = id
        self.username = username
        self.passwork_hash = password_hash
        self.active = active

class Queries():
    def __init__(self):
        try:
            conn = db.connect()
        except cursor.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        self.conn = conn

#######################################################################
# GET By ID
######################################################################
    def get(self, id):
        print("getter ")
        conn = db.connect()
        cursor = conn.cursor()

        idstr = str(id)
        #print("idstr: ", idstr)

        sql = "SELECT * FROM user WHERE id = '" + idstr + "' "
        #print("sql: ", sql)
        cursor.execute(sql)
        userData = cursor.fetchone()
        conn.close()

        return userData

#######################################################################
# REGISTER_CHECKUSER
######################################################################
    def register_checkUser(self, username):
        #print("username ", username)
        conn = db.connect()
        cursor = conn.cursor()

        sql = "SELECT * FROM user WHERE username = '" + username + "' "
        cursor.execute(sql)
        usrData = cursor.fetchone()
        conn.close()

        return usrData

#######################################################################
# LOGIN_CHECKUSER
######################################################################
    def login_checkUser(self, username, password):
        print("username ", username)
        conn = db.connect()
        cursor = conn.cursor()

        sql = "SELECT * FROM user WHERE username = '" + username + "' "
        cursor.execute(sql)
        usrData = cursor.fetchone()
        conn.close()

        if usrData == None:
            return None

        password_hash = usrData[2]
        pwCheck = check_password_hash(password_hash, password)

        if pwCheck:
            # print("1Models: user_json ")
            # user_json = json.dumps(usrData)
            # print("Models: user_json ", user_json)
            return usrData
        else:
            return None


#######################################################################
# REGISTER A NEW USER
######################################################################
    def register(self, username, password):
        #print("username ", username)
        #print("password ", password)
        conn = db.connect()
        cursor = conn.cursor()
        pwh = generate_password_hash(password)
        s = "('" + username + "', '" + pwh + "')"
        sql = "INSERT INTO user (username, password_hash) VALUES " + s
        cursor.execute(sql)
        conn.commit()

        sql = "SELECT * FROM user WHERE username = '" + username + "' "
        cursor.execute(sql)
        usrData = cursor.fetchone()
        conn.close()

        return usrData
