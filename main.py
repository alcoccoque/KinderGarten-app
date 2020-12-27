import re
import model
import sqlite3

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class ErrorPopup(Popup):
    pass


class AddKid(Screen):
    fullname = ObjectProperty(None)
    parentname = ObjectProperty(None)
    kgarten = ObjectProperty(None)
    month = ObjectProperty(None)

    def insert_kid(self):
        if self.validate_input():
            model.insert(self.fullname.text, self.parentname.text, self.kgarten.text, self.month.text)
            print("Child added")
            self.fullname.text, self.parentname.text, self.kgarten.text, self.month.text = "", "", "", ""
        else:
            error_pop = ErrorPopup()
            error_pop.ids.error.text = "Failed to insert kid in database.try again"
            error_pop.title = "Insert Error"
            error_pop.open()

    def validate_input(self):
        if self.fullname.text != "" and self.parentname.text != "" and self.kgarten.text != "" and self.month.text != "":
            print("True")
            return True
        else:
            print("False")
            return False


class RemoveKid(Screen):
    kid_id = ObjectProperty(None)

    def remove_kid(self):
        if self.validate_input():
            model.remove(self.kid_id.text)
            print("Child removed")
            self.kid_id.text = ""
        else:
            error_pop = ErrorPopup()
            error_pop.ids.error.text = "Failed to remove student in database.try again"
            error_pop.title = "Removing Error"
            error_pop.open()

    def validate_input(self):
        if self.kid_id.text != "":
            print("True")
            return True
        else:
            print("False")
            return False


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)


class Change(Screen):
    month = ObjectProperty(None)
    numOfVisitDays = ObjectProperty(None)
    kid_id = ObjectProperty(None)

    def change_numOfVisitDays(self):
        if self.validate_input():
            model.change(self.month.text, self.numOfVisitDays.text, self.kid_id.text)
            print("Days changed")
            self.month.text, self.numOfVisitDays.text, self.kid_id.text = "", "", ""
        else:
            error_pop = ErrorPopup()
            error_pop.ids.error.text = "Failed to remove student in database.try again"
            error_pop.title = "Removing Error"
            error_pop.open()

    def validate_input(self):
        if self.month.text != "" and self.numOfVisitDays.text != "" and self.kid_id.text != "":
            print("True")
            return True
        else:
            print("False")
            return False


class Bookkeeping(Screen, BoxLayout):
    data_items_bk = ListProperty([])
    data_items_pa = ListProperty([])
    # ID_M = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Bookkeeping, self).__init__(**kwargs)
        self.get_users(1)

    def get_users(self, ID_M):
        Bookkeeping.deleteinfo(self)
        bk_rows = model.show_by_month(ID_M)
        pa_rows = model.get_users()
        for row in bk_rows:
            for col in row:
                self.data_items_bk.append(col)
                print(col)
        for row in pa_rows:
            for col in row:
                self.data_items_pa.append(col)

    def deleteinfo(self):
        self.data_items_bk.clear()
        self.data_items_pa.clear()


class Manager(ScreenManager):
    pass


class MainScreenManager(ScreenManager):
    pass


class Login(Screen):
    login_name = ObjectProperty(None)
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)

    def login(self):
        try:
            name, password = model.login()
            print(name, password)
            if name == self.login_name.text and password == self.password.text:
                self.manager.current = "main_screen"
                self.password.text, self.login_name.text = "", ""
                print("User logged in")
            else:
                print("Login failure")
                pop_error = ErrorPopup()
                pop_error.title = "Login failure"
                pop_error.ids.error.text = "Failed to login.Check credentials"
                pop_error.open()

        except sqlite3.OperationalError as err:
            pop_error = ErrorPopup()
            pop_error.title = "Login failure"
            pop_error.ids.error.text = err.message + " .Failed to login user"
            pop_error.open()


class MainScreen(Screen):
    pass


class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in \
                              substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class MainApp(App):
    def build(self):
        manager = Manager()
        return manager


if __name__ == '__main__':
   # con = sqlite3.connect('kg_db.db')
   # cur = con.cursor()
   # data = cur.execute("SELECT * FROM personalAccount")
   # data = data.fetchall()
   # print(data)
   # data2 = cur.execute("SELECT * FROM bookeeping")
   # data2 = data2.fetchall()
   # print(data2)
   MainApp().run()
