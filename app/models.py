from app import db, login_manager
from flask import session, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, current_user

@login_manager.user_loader
def load_user(user_id):
    userData = Queries().get(user_id)
    user = User(userData[0], userData[1], userData[2], userData[3], userData[4])
    return user

class User(UserMixin):

    def __init__(self, id, isAdmin_yn, username, email, password_hash, active=True):
        self.id = id
        self.isAdmin_yn = isAdmin_yn
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.active = active


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        #print("in verify_reset_token  ", token)

        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
            #print("in verify_reset_token user id  ", user_id)
        except:
            return None
        #print("in verify_reset_token user id2  ", user_id)
        userData = Queries().get(user_id)
        #print("in verify_reset_token user data  ", userData)
        user = User(userData[0], userData[1], userData[2], userData[3], userData[4])
        #print("in verify_reset_token user  ", user)
        return user


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
        cursor = self.conn.cursor()
        idstr = str(id)
        sql = "SELECT * FROM user WHERE id = '" + idstr + "' "
        #print("sql: ", sql)
        cursor.execute(sql)
        userData = cursor.fetchone()
        self.conn.close()

        return userData

#######################################################################
# REGISTER_CHECKUSER
######################################################################
    def register_checkUser(self, username):
        #print("username ", username)
        cursor = self.conn.cursor()

        sql = "SELECT * FROM user WHERE username = '" + username + "' "
        cursor.execute(sql)
        usrData = cursor.fetchone()
        self.conn.close()

        return usrData

#######################################################################
# UPDATE PASSWORD
######################################################################
    def update_password(self, username, password):
        #print("username, password ", username, password)
        pwh = generate_password_hash(password)

        #currentUser = current_user.username
        print("Update Password ", pwh, password, username)
        cursor = self.conn.cursor()

        sql = """UPDATE user
            SET password_hash = %s
            WHERE username = %s """
        cursor.execute(sql, (pwh, username))
        self.conn.commit()
        self.conn.close()

#######################################################################
# RESET_PASSWORD_CHECKUSER
######################################################################
    def reset_password_checkUser(self, username):
        #print("username in models ", username)
        cursor = self.conn.cursor()

        sql = "SELECT * FROM user WHERE username = '" + username + "' LIMIT 1"
        #print("sql: ", sql)
        cursor.execute(sql)
        user = cursor.fetchone()
        #print("user: ", user)
        self.conn.close()

        return user

#######################################################################
# LOGIN_CHECKUSER
######################################################################
    def login_checkUser(self, username, password):
        #print("username ", username)
        cursor = self.conn.cursor()

        sql = "SELECT * FROM user WHERE username = '" + username + "' "
        cursor.execute(sql)
        usrData = cursor.fetchone()
        self.conn.close()

        if usrData == None:
            return None

        password_hash = usrData[4]
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
    def register(self, username, password, email):
        #print("username ", username)
        #print("password ", password)
        cursor = self.conn.cursor()
        pwh = generate_password_hash(password)
        s = "('" + username + "', '" + pwh + "', '" + email + "')"
        sql = "INSERT INTO user (username, password_hash, email) VALUES " + s
        cursor.execute(sql)
        self.conn.commit()

        sql = "SELECT * FROM user WHERE username = '" + username + "' "
        cursor.execute(sql)
        usrData = cursor.fetchone()
        self.conn.close()

        return usrData

#######################################################################
# UPDATE USER ACCOUNT
######################################################################
    def update_account(self, username, email):
        #print("username ", username)
        #print("current_user ", current_user.username)
        currentUser = current_user.username
        cursor = self.conn.cursor()

        sql = """UPDATE user
            SET username = %s, email = %s
            WHERE username = %s """
        cursor.execute(sql, (username, email, currentUser))
        self.conn.commit()
        self.conn.close()

#######################################################################
# DISTRICTS ALL
######################################################################
    def districts_all(self):
        #print("In models -> districtsAll ")
        json_districts = []
        cursor = self.conn.cursor()
        sql = """SELECT district_id, district_name
        FROM district
        ORDER BY district_name """
        cursor.execute(sql)
        self.conn.close()
        rows = cursor.fetchall()
        #print("In models -> districtsAll- rows ", rows)
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
        #print("In categories_all ")
        json_categories = []
        cursor = self.conn.cursor()
        sql = """SELECT category_id, category_description
            FROM category
            ORDER BY category_description"""
        cursor.execute(sql)
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_category = {'category_id': row[0], 'category_description': row[1]}
            json_categories.append(json_category)
            json_category = {}
        return json_categories

#######################################################################
# SPECIAL COLLECTIONS ALL
######################################################################
    def specialCollections_all(self):
        #print("In models -> specialCollections ")
        json_specialCollections = []
        cursor = self.conn.cursor()
        sql = """SELECT spcol_id, spcol_description
            FROM special_collection
            ORDER BY spcol_description"""
        cursor.execute(sql)
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_specialCollection = {'spcol_id': row[0], 'spcol_description': row[1]}
            json_specialCollections.append(json_specialCollection)
            json_specialCollection = {}
        return json_specialCollections

#######################################################################
# REFERENCES BY DISTRICT
######################################################################
    def references_by_district(self, district_id):
        #print("In Models: references_by_district ")
        json_refs = []
        cursor = self.conn.cursor()
        sql = """SELECT r.reference_id, r.reference, r.filename, r.url
            FROM reference r
            INNER JOIN district_to_reference d ON d.reference_id = r.reference_id
            WHERE d.district_id = %s
            ORDER BY r.reference """
        cursor.execute(sql, district_id)
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        #print("In Models: references_by_district rows ", rows)
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
        cursor = self.conn.cursor()
        sql = """SELECT r.reference_id, r.reference, r.filename, r.url
            FROM reference r
            INNER JOIN category_to_reference c ON c.reference_id = r.reference_id
            WHERE c.category_id = %s
            ORDER BY r.reference """
        cursor.execute(sql, category_id)
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_ref = {'reference_id': row[0], 'reference': row[1],
                'filename': row[2], 'url': row[3]}
            json_refs.append(json_ref)
            json_ref = {}
        return json_refs

#######################################################################
# REFERENCES BY SPECIALCOLLECTION
######################################################################
    def references_by_specialCollection(self, spcol_id):
        json_refs = []
        cursor = self.conn.cursor()
        sql = """SELECT r.reference_id, r.reference, r.filename, r.url
            FROM reference r
            INNER JOIN specialcollection_to_reference sc
                ON sc.reference_id = r.reference_id
            WHERE sc.spcol_id = %s
            ORDER BY r.reference """
        cursor.execute(sql, spcol_id)
        self.conn.close()
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
        cursor = self.conn.cursor()
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
        self.conn.close()
        #Convert to JSON format
        json_ref = {'url': row[2]}
        return json_ref


#######################################################################
# REFERENCES SEARCH
######################################################################
    def references_search(self, usrFrag):
        json_refs = []
        cursor = self.conn.cursor()
        usrFragSQL1 = '%' + '' + '%'
        usrFragSQL2 = '%' + '' + '%'
        usrFragSQL3 = '%' + '' + '%'
        usrFragSplit = usrFrag.split(',')
        if len(usrFragSplit) == 1:
            usrFragSQL1 = '%' + usrFragSplit[0] + '%'
        if len(usrFragSplit) == 2:
            usrFragSQL1 = '%' + usrFragSplit[0] + '%'
            usrFragSQL2 = '%' + usrFragSplit[1] + '%'
        if len(usrFragSplit) == 3:
            usrFragSQL1 = '%' + usrFragSplit[0] + '%'
            usrFragSQL2 = '%' + usrFragSplit[1] + '%'
            usrFragSQL3 = '%' + usrFragSplit[2] + '%'
        sql = """SELECT reference_id, reference, filename, url
                    FROM reference
                    WHERE (reference like %s and reference like %s and reference like %s)
                    ORDER BY reference """
        cursor.execute(sql, (usrFragSQL1, usrFragSQL2, usrFragSQL3))
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_ref = {'reference_id': row[0], 'reference': row[1],
                'filename': row[2], 'url': row[3]}
            #json_ref = {'reference_id': row[0], 'reference': row[1]}
            json_refs.append(json_ref)
            json_ref = {}
        return json_refs


#######################################################################
#######################################################################
# REFERENCE - EDIT PAGES
######################################################################
#######################################################################

#######################################################################
# REFERENCE - EDIT PAGE FOR ALL DISTRICTS
######################################################################
    def references_edit(self, id):
        #print('references_edit in models, refid:  ', id)
        json_refs = []
        cursor = self.conn.cursor()
        sql = """SELECT *
            FROM reference
            WHERE reference_id = %s"""
        cursor.execute(sql, id)
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_ref = {'reference_id': row[0], 'reference': row[1],
                'source': row[2], 'verified': row[3], 'filename': row[4],
                'url': row[5], 'section': row[6]}
            json_refs.append(json_ref)
            json_ref = {}
        return json_refs

#######################################################################
# REFERENCE - EDIT PAGE FOR ALL DISTRICTS
######################################################################
    def districts_by_reference(self, refid):
        json_refs = []
        cursor = self.conn.cursor()
        sql = """SELECT r.district_id, d.district_name
            FROM district_to_reference r
            INNER JOIN district d ON d.district_id = r.district_id
            WHERE r.reference_id = %s """
        cursor.execute(sql, refid)
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_ref = {'district_id': row[0], 'district_name': row[1]}
            json_refs.append(json_ref)
            json_ref = {}
        return json_refs

#######################################################################
# REFERENCE - EDIT PAGE FOR CATEGORIES
######################################################################
    def categories_by_reference(self, refid):
        json_refs = []
        cursor = self.conn.cursor()
        sql = """SELECT r.category_id, c.category_name, c.category_description
            FROM category_to_reference r
            INNER JOIN category c ON c.category_id = r.category_id
            WHERE r.reference_id = %s """
        cursor.execute(sql, refid)
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_ref = {'category_id': row[0],
                'category_name': row[1], 'category_description': row[2]}
            json_refs.append(json_ref)
            json_ref = {}
        return json_refs

#######################################################################
# REFERENCE - EDIT PAGE FOR SPECIIAL COLLECTIONS
######################################################################
    def specialCollections_by_reference(self, refid):
        json_refs = []
        cursor = self.conn.cursor()
        sql = """SELECT r.spcol_id, s.spcol_name, s.spcol_description
            FROM specialCollection_to_reference r
            INNER JOIN special_collection s ON s.spcol_id = r.spcol_id
            WHERE r.reference_id = %s """
        cursor.execute(sql, refid)
        self.conn.close()
        rows = cursor.fetchall()
        #Convert to JSON format
        for row in rows:
            json_ref = {'special_id': row[0],
                'special_name': row[1], 'special_description': row[2]}
            json_refs.append(json_ref)
            json_ref = {}
        return json_refs


###############################################################################
###############################################################################
# REFERENCE EDIT - UPDATE DATABASE
###############################################################################
###############################################################################
    def references_newRefid(self):
        # Get a new reference_id
        #print('refid1 in models: ')
        cursor = self.conn.cursor()
        sql = """SELECT MAX(reference_id)
           FROM reference"""
        cursor.execute(sql)
        tup = cursor.fetchone()
        newRefid = str(tup[0] + 1)
        self.conn.close()
        #cursor.close()

        #print('newRefid in models, refid:  ', newRefid)

        return newRefid

    def references_edit_new(self, reference, source, filename, url, yn):
        #print('references_edit_new in models, refid:  ', refid)
        # Get a new reference_id
        cursor = self.conn.cursor()
        sql = """SELECT MAX(reference_id)
           FROM reference"""
        cursor.execute(sql)
        tup = cursor.fetchone()
        refid = str(tup[0] + 1)
        # Insert main dta for new reference
        sql = """INSERT
                INTO reference (reference_id, reference, source, filename, url, verified)
                VALUES(%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (refid, reference, source, filename, url, yn))
        self.conn.commit()
        self.conn.close()
        #cursor.close()

        return refid

    def references_edit_delete(self, refid):
        #print('references_edit_delete in models, refid:  ', refid)
        cursor = self.conn.cursor()
        #print('In references_delete')
        # Delete the current reference
        sql = """DELETE
                FROM reference
                WHERE reference_id = %s """
        cursor.execute(sql, refid)
        self.conn.commit()

        sql = """DELETE
                FROM district_to_reference
                WHERE reference_id = %s """
        cursor.execute(sql, refid)
        self.conn.commit()

        sql = """DELETE
                FROM category_to_reference
                WHERE reference_id = %s """
        cursor.execute(sql, refid)
        self.conn.commit()

        sql = """DELETE
                FROM specialCollection_to_reference
                WHERE reference_id = %s """
        cursor.execute(sql, refid)
        self.conn.commit()

        sql = """SELECT MAX(reference_id)
           FROM reference"""
        cursor.execute(sql)
        tup = cursor.fetchone()
        refid = str(tup[0] + 1)

        self.conn.close()
        #cursor.close()

        return refid

    ###############################################################################
    ###############################################################################
    # REFERENCE EDIT - SAVE
    ###############################################################################
    ###############################################################################
    def references_edit_save(self, refid, reference, source, filename, url, yn):
        #print('references_edit_save in models, refid:  ', refid)
        cursor = self.conn.cursor()
        #IF THE REFERENCE_ID EXISTS WE UPDATE ELSE WE INSERT
        sql = """SELECT reference_id
           FROM reference
           WHERE reference_id = %s """
        cursor.execute(sql, (refid))
        tup = cursor.fetchone()

        if tup == None:
            #print("inserting")
            sql = """INSERT
                INTO reference (reference_id, reference, source, filename, url, verified)
                VALUES(%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (refid, reference, source, filename, url, yn))
        else:
            print("updating")
            sql = """UPDATE reference
                 SET reference = %s, source = %s, filename = %s, url = %s, verified = %s
                 WHERE reference_id = %s"""
            cursor.execute(sql, (reference, source, filename, url, yn, refid))
        self.conn.commit()
        self.conn.close()

    def references_edit_save_districts(self, refid, district_ids):
        #print('references_edit_save_districts in models, refid:  ', refid)
        cursor = self.conn.cursor()
        sql = """DELETE
           FROM district_to_reference
           WHERE reference_id = %s """
        cursor.execute(sql, (refid))
        self.conn.commit()

        for district_id in district_ids:
             sql = """INSERT IGNORE
                INTO district_to_reference (district_id, reference_id)
                VALUES(%s, %s)"""
             cursor.execute(sql, (district_id, refid))
             self.conn.commit()
        #cursor.close()
        cursor.close()

    def references_edit_save_categories(self, refid, category_ids):
        #print('references_edit_save_categories in models, refid:  ', refid)
        cursor = self.conn.cursor()
        sql = """DELETE
           FROM category_to_reference
           WHERE reference_id = %s """
        cursor.execute(sql, (refid))
        self.conn.commit()

        for category_id in category_ids:
             sql = """INSERT IGNORE
                INTO category_to_reference (category_id, reference_id)
                VALUES(%s, %s)"""
             cursor.execute(sql, (category_id, refid))
             self.conn.commit()
        cursor.close()

    def references_edit_save_specials(self, refid, special_ids):
        #print('references_edit_save_specials in models, refid:  ', refid)
        cursor = self.conn.cursor()
        sql = """DELETE
           FROM specialCollection_to_reference
           WHERE reference_id = %s """
        cursor.execute(sql, (refid))
        self.conn.commit()

        for special_id in special_ids:
             sql = """INSERT IGNORE
                INTO specialCollection_to_reference (spcol_id, reference_id)
                VALUES(%s, %s)"""
             cursor.execute(sql, (special_id, refid))
             self.conn.commit()
        cursor.close()
