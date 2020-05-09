from app import db, login_manager
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    userData = Queries().get(user_id)
    user = User(userData[0], userData[1], userData[2], userData[3])
    return user

class User(UserMixin):

    def __init__(self, id, username, isAdmin_yn, password_hash, active=True):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.active = active
        self.isAdmin_yn = isAdmin_yn

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
        #print("in getter")
        conn = db.connect()
        cursor = conn.cursor()
        idstr = str(id)
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
        #print("username ", username)
        conn = db.connect()
        cursor = conn.cursor()

        sql = "SELECT * FROM user WHERE username = '" + username + "' "
        cursor.execute(sql)
        usrData = cursor.fetchone()
        conn.close()

        if usrData == None:
            return None

        password_hash = usrData[3]
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

#######################################################################
# DISTRICTS ALL
######################################################################
    def districts_all(self):
        json_districts = []
        conn = db.connect()
        cursor = conn.cursor()
        sql = """SELECT district_id, district_name
        FROM district
        ORDER BY district_name """
        cursor.execute(sql)
        conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_district = {'district_id': row[0], 'district_name': row[1]}
            json_districts.append(json_district)
            json_district = {}
        return json_districts

#######################################################################
# CATEGORIES ALL
######################################################################
    def categories_all(self):
        print("In categories_all ")
        json_categories = []
        conn = db.connect()
        cursor = conn.cursor()
        sql = """SELECT category_id, category_description
            FROM category
            ORDER BY category_description"""
        cursor.execute(sql)
        conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_category = {'category_id': row[0], 'category_description': row[1]}
            json_categories.append(json_category)
            json_category = {}
        return json_categories

#######################################################################
# REFERENCES BY DISTRICT
######################################################################
    def references_by_district(self, district_id):
        print("In Models: references_by_district ")
        json_refs = []
        conn = db.connect()
        cursor = conn.cursor()
        sql = """SELECT r.reference_id, r.reference, r.filename, r.url
            FROM reference r
            INNER JOIN district_to_reference d ON d.reference_id = r.reference_id
            WHERE d.district_id = %s
            ORDER BY r.reference """
        cursor.execute(sql, district_id)
        conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_ref = {'reference_id': row[0], 'reference': row[1],
                'filename': row[2], 'url': row[3]}
            json_refs.append(json_ref)
            json_ref = {}
        return json_refs

#######################################################################
# REFERENCES BY CATEGORY
######################################################################
    def references_by_category(self, category_id):
        json_refs = []
        conn = db.connect()
        cursor = conn.cursor()
        sql = """SELECT r.reference_id, r.reference, r.filename, r.url
            FROM reference r
            INNER JOIN category_to_reference c ON c.reference_id = r.reference_id
            WHERE c.category_id = %s
            ORDER BY r.reference """
        cursor.execute(sql, category_id)
        conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_ref = {'reference_id': row[0], 'reference': row[1],
                'filename': row[2], 'url': row[3]}
            json_refs.append(json_ref)
            json_ref = {}
        return json_refs

#######################################################################
# REFERENCE DISPLAY PDFS
######################################################################
#THEN CONCAT('/static/pdfs/', filename)
    def url_pdf(self, id):
        json_refs = []
        conn = db.connect()
        cursor = conn.cursor()
        sql = """SELECT url, filename,
            CASE
                WHEN filename IS NOT NULL AND filename != 'None' AND filename != ''
                    THEN CONCAT('/static/pdfs/', filename)
                WHEN url IS NOT NULL AND url != 'None' AND url != '' THEN url
            END AS path
            FROM reference
            WHERE reference_id = %s
                AND ((url IS NOT NULL and url != 'None' and url != '')
                    OR (filename IS NOT NULL and filename != 'None' and filename != ''))"""
        cursor.execute(sql, id)
        row = cursor.fetchone()
        conn.close()
        #Convert to JSON format
        json_ref = {'url': row[2]}
        return json_ref
