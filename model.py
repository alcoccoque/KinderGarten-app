import sqlite3

from kivy.uix.label import Label
from kivy.uix.popup import Popup

con = sqlite3.connect('kg_db.db')


def create_table():
    try:
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        con.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS "Parents" (
            ID_PARENTS	INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME	    TEXT NOT_NULL
            )""")
        con.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS "kinderGarten" (
            ID_KDG	INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME	TEXT NOT NULL,
            STREET    TEXT NOT NULL
            )""")
        con.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS "personalAccount" (
            ID	        INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_KDG	    INTEGER NOT NULL,
            ID_PARENTS	INTEGER NOT NULL,
            FULL_NAME	TEXT NOT NULL,
            FOREIGN KEY(ID_PARENTS) REFERENCES Parents(ID_PARENTS) ON DELETE CASCADE ON UPDATE CASCADE
            )""")
        con.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS "booKeeping" (
            ID_BK	              INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_M        	      INTEGER NOT NULL,
            numOfVisitDays	      INTEGER NOT NULL,
            monthlyPaymentResult  REAL GENERETED always as (1000 / 22 * numOfVisitDays) stored,
            ID	                  INTEGER NOT NULL,
            FOREIGN KEY(ID) REFERENCES  personalAccount(ID) ON DELETE CASCADE ON UPDATE CASCADE
            )""")
        con.commit()
        con.execute("""CREATE TABLE IF NOT EXISTS "admin" (
            name                  TEXT NOT NULL,
            password              TEXT NOT NULL
            )""")
        con.commit()
    except sqlite3.OperationalError as exc:
        print(exc.message)


def insert(fullname, parentname, kgarten, month):
    try:
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute(f"SELECT ID_KDG FROM kinderGarten WHERE NAME = ?", [kgarten])
        KGARTEN_ID, = cur.fetchone()
        con.commit()
        cur.execute(f"SELECT FULL_NAME FROM personalAccount LEFT JOIN Parents ON personalAccount.ID_PARENTS = Parents.ID_PARENTS WHERE FULL_NAME = ? AND NAME = ?",
                    [fullname, parentname])
        if cur.fetchone() is None:
            con.commit()
            cur.execute(f"SELECT FULL_NAME FROM personalAccount LEFT JOIN bookeeping ON personalAccount.ID = bookeeping.ID WHERE FULL_NAME = ? AND ID_M = ?",
                        [fullname, month])
            if cur.fetchone() is None:
                con.commit()
                cur.execute(f"INSERT INTO Parents(NAME) VALUES(?)", [parentname])
                con.commit()
                PARENT_ID = cur.lastrowid
                cur.execute(f"INSERT INTO personalAccount(ID_KDG,ID_PARENTS,FULL_NAME) VALUES(?, ?, ?)",
                                                         [KGARTEN_ID, PARENT_ID, fullname])
                con.commit()
                cur.execute(f"INSERT INTO bookeeping(ID_M, numOfVisitDays, ID) VALUES(?,?,?)",
                            [month, 1, PARENT_ID])
                con.commit()
            else:
                print("This kid is already signed up!")
        else:
            cur.execute(f"SELECT ID FROM personalAccount WHERE FULL_NAME = ?", [fullname])
            KID_ID, = cur.fetchone()
            con.commit()
            # cur.execute(f"SELECT PARENT_ID FROM Parents LEFT JOIN Parents ON personalAccount.ID_PARENTS = Parents.ID_PARENTS WHERE FULL_NAME = ? AND NAME = ?",[fullname, parentname] )
            # PARENT_ID, = cur.fetchone()
            cur.execute(f"INSERT INTO bookeeping(ID_M, numOfVisitDays, ID) VALUES(?,?,?)",
                        [month, 1, KID_ID])
            con.commit()

    except sqlite3.OperationalError as exc:
        Popup(conttent=Label(text=str(exc.message)), size_hint=(None, None), size=(200, 200)).open()


def remove(kid_id):
    try:
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute("DELETE FROM Parents where ID_PARENTS = ?", [kid_id])
        con.commit()
    except sqlite3.OperationalError as exc:
        Popup(conttent=Label(text=str(exc.message)), size_hint=(None, None), size=(200, 200)).open()


def show_by_month(ID_M):
    cur = con.cursor()
    cur.execute("SELECT ID_BK, numOfVisitDays, monthlyPaymentResult, ID FROM bookeeping WHERE ID_M = ?", [ID_M])
    res = cur.fetchall()
    con.commit()
    return res

def change(month, numOfVisitDays, kid_id):
    cur = con.cursor()
    cur.execute("UPDATE bookeeping SET numOfVisitDays = ? WHERE ID_M = ? AND ID = ?", [numOfVisitDays, month,  kid_id])
    con.commit()

def get_users():
    cur.execute("SELECT * FROM personalAccount ORDER BY ID ASC")
    pa_rows = cur.fetchall()
    con.commit()
    return pa_rows

def login():
    cur = con.cursor()
    cur.execute("SELECT * FROM admin")
    name, password = cur.fetchone()
    return name, password

# create_table()
# con.execute("INSERT INTO admin "
#              "(  name,password)"
#              "  VALUES "
#              "(?,?)",
#              ("admin","password"))
# con.commit()
# parents = [('1', 'Valentina'), ('2', 'Victor'), ('3', 'Nikolai'), ('4', 'Vlad'), ('5', 'Katya')]
#
# kindergarten = [('1', 'Romashka'), ('2', 'Barvinok'), ('3', 'Malyatko'), ('4', 'Roshen')]
#
# personalacc = [('1', '3', '3', 'Borov Vadim Nikolaevich'),
#                ('2', '4', '2', 'Zirko Nikolai Victorovich'),
#                ('3', '3', '1', 'Uskovich Ivan Vadimovich'),
#                ('4', '1', '4', 'Zaizev Eugeniy Vladislavovich'),
#                ('5', '2', '5', 'Vladimirov Vladimir Nikolaevich')]
#
# bookeeping = [('1', '13', '1', '12'),
#               ('2', '13', '2', '12'),
#               ('3', '15', '3', '12'),
#               ('4', '19', '4', '12'),
#               ('5', '21', '5', '12')]
#
cur = con.cursor()
cur.execute(
    f"SELECT FULL_NAME FROM personalAccount JOIN Parents ON personalAccount.ID_PARENTS = Parents.ID_PARENTS WHERE FULL_NAME = ? AND NAME = ?",
    ['Vladimirov Vladimir Nikolaevich', 'Katya'])
res = cur.fetchone()
con.commit()
print(res)
# cur.executemany("INSERT INTO Parents VALUES(?, ?);", parents)
# con.commit()
# cur.executemany("INSERT INTO kinderGarten VALUES(?, ?);", kindergarten)
# con.commit()
# cur.executemany("INSERT INTO personalAccount(ID, ID_KDG, ID_PARENTS, FULL_NAME) VALUES(?, ?, ?, ?);", personalacc)
# con.commit()
# cur.executemany("INSERT INTO booKeeping(ID_BK, numOfVisitDays, ID, ID_M) VALUES(?, ?, ?, ?);", bookeeping)
# con.commit()
#
# print("\n")
# print("PARENTS")
# print("\n")
# for i in cur.execute("SELECT * from Parents"):
#     print(i)
# print("\n")
# print("KINDER_GARTEN")
# print("\n")
# for i in cur.execute("SELECT * from kinderGarten"):
#     print(i)
# print("\n")
# print("PERSONAL_ACCOUNT")
# print("\n")
# for i in cur.execute("SELECT * from personalAccount"):
#     print(i)
# print("\n")
# print("BOOKEEPING")
# print("\n")
# for i in cur.execute("SELECT * from bookeeping"):
#     print(i)
