import sys
import sqlite3
from extra_modules import Card_Check, check_phone_correct
from courier import *
from user import *
from admin import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QWidget, QMessageBox
import os


con = sqlite3.connect("data_base_1.db")
cur = con.cursor()
ADMIN_LOGIN = 'a'
ADMIN_PASSWORD = 'a'


class Authorization(QWidget):
    def __init__(self):
        super(Authorization, self).__init__()
        uic.loadUi('auth_design.ui', self)
        self.setWindowTitle('Авторизация')
        self.password.setEchoMode(QLineEdit.Password)
        self.setFixedSize(400, 400)
        self.registration.clicked.connect(self.run_registration)
        self.entrance.clicked.connect(self.run)

    def run(self):
        login = self.login.text()
        self.loginx = self.login.text()
        password = self.password.text()
        logins_user = cur.execute("""SELECT user_info.user_login FROM user_info""").fetchall()
        logins_user = [''.join(elem) for elem in logins_user]
        logins_courier = cur.execute("""SELECT courier_info.courier_login FROM courier_info""").fetchall()
        logins_courier = [''.join(elem) for elem in logins_courier]
        password_user = cur.execute("""SELECT user_info.user_password FROM user_info""").fetchall()
        password_user = [''.join(elem) for elem in password_user]
        password_courier = cur.execute("""SELECT courier_info.courier_password FROM courier_info""").fetchall()
        password_courier = [''.join(elem) for elem in password_courier]
        if login in logins_user and password in password_user:
            self.error.setText('')
            self.user_start()
        elif login in logins_courier and password in password_courier:
            self.error.setText('')
            self.courier_start()
        elif login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            self.error.setText('')
            self.admin_start()
        else:
            self.error.setText('Логин или пароль не найдены.')
            self.error.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
            return False

    def run_registration(self):
        self.widget = Registration()
        self.widget.show()
        self.close()

    def user_start(self):
        self.login = self.loginx
        self.login_id = cur.execute(f"""SELECT
                 user_info.id FROM user_info WHERE user_info.user_login = '{self.login}'""").fetchall()[0][
            0]
        self.user = User_Main_Window(self.login)
        self.user.show()
        self.close()

    def admin_start(self):
        self.admin = Admin_Main_Window()
        self.admin.show()
        self.close()

    def courier_start(self):
        self.login = self.loginx
        self.login_id = cur.execute(f"""SELECT
         courier_info.id FROM courier_info WHERE courier_info.courier_login = '{self.login}'""").fetchall()[0][0]
        self.courier = Courier_Main_Window(self.login, self.login_id)
        self.courier.show()
        self.close()


class Registration(QWidget):
    def __init__(self):
        super(Registration, self).__init__()
        uic.loadUi('register_design.ui', self)
        self.setWindowTitle('Регистрация')
        self.password1.setEchoMode(QLineEdit.Password)
        self.password2.setEchoMode(QLineEdit.Password)
        self.register_2.clicked.connect(self.run)

    def run(self):
        if check_phone_correct(self.phone.text()) is False:
            self.error_3.setText('Ошибка: неверно введён номер телефона')
            self.error_3.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_3.setText('')

        if '@' not in self.email.text() and '.' not in self.email.text() or len(self.email.text()) == 0:
            self.error_1.setText('Ошибка: неверный формат электронной почты')
            self.error_1.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_1.setText('')

        if len(self.fio.text().split()) < 2 or len(self.fio.text().split()) > 3:
            self.error_2.setText('Ошибка: неверный формат ФИО. Вы должны указать полное ФИО или только имя и фамилию')
            self.error_2.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_2.setText('')
        card = Card_Check(self.card_num.text())

        if self.adress.text() == '':
            self.error_4.setText('Ошибка: неверный формат адреса')
            self.error_4.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_4.setText('')

        if card.process_data() is not None:
            self.error_5.setText(card.process_data())
            self.error_5.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_5.setText('')
        if len(self.card_date.text()) != 5 or '/' not in self.card_date.text():
            self.error_6.setText('Ошибка: неверный формат срока действия карты')
            self.error_6.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_6.setText('')
        if len(self.cvc.text()) != 3 or self.cvc.text().isdigit() is False:
            self.error_7.setText('Ошибка: неверный формат cvc')
            self.error_7.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_7.setText('')

        if len(self.card_holder.text().split()) != 2 or self.card_holder.text().isupper() is False:
            self.error_8.setText('Ошибка: укажите данные в формате IVAN IVANOV')
            self.error_8.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_8.setText('')

        if len(self.password1.text()) > 6:
            self.length.setChecked(True)
        else:
            self.length.setChecked(False)
        if self.password1.text() == self.password2.text():
            self.length_2.setChecked(True)
        else:
            self.length_2.setChecked(False)
        logins_user = cur.execute("""SELECT user_info.user_login FROM user_info""").fetchall()
        logins_user = [''.join(elem) for elem in logins_user]
        if self.login.text() == '':
            self.error_9.setText('Ошибка: неверный формат логина')
            self.error_9.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        elif self.login.text() in logins_user or self.login.text() == ADMIN_LOGIN:
            self.error_9.setText('Ошибка: логин занят')
            self.error_9.setStyleSheet("""color: #aa0000; \n font: 10pt "MS Shell Dlg 2";""")
        else:
            self.error_9.setText('')

        if self.error_1.text() == '' and self.error_2.text() == '' and self.error_3.text() == '' \
                and self.error_4.text() == '' and self.error_5.text() == '' and self.error_6.text() == '' \
                and self.error_7.text() == '' and self.error_8.text() == '' and self.length.isChecked() \
                and self.length_2.isChecked():
            email = str(self.email.text())
            fio = str(self.fio.text())
            adress = str(self.adress.text())
            phone = str(self.phone.text())
            card_num = str(self.card_num.text())
            card_date = str(self.card_date.text())
            cvc = str(self.cvc.text())
            card_holder = str(self.card_holder.text())
            password = str(self.password1.text())
            login = str(self.login.text())
            print(1)
            cur.execute(f"""INSERT INTO user_info(user_login, user_password,
             user_fio, user_adress, user_card_num, user_card_working_date, user_card_name_holder, user_cvc,
              user_phone_number) VALUES ('{login}', '{password}', '{fio}', '{adress}',
'{card_num}', '{card_date}', '{card_holder}', '{cvc}', '{phone}');""")
            con.commit()
            self.user = User_Main_Window(login)
            self.user.show()
            self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if self.check_file_correction() is False:
            self.show_dialog()
            raise ImportError
        uic.loadUi('main_design.ui', self)
        self.setWindowTitle('YandexEda')
        self.widget = Authorization()
        self.widget.show()

    def check_file_correction(self):
        thisdir = "./"
        if not ("admin.py" in os.listdir(thisdir)):
            return False
        elif not ("admin_interface.ui" in os.listdir(thisdir)):
            return False
        elif not ("auth_design.ui" in os.listdir(thisdir)):
            return False
        elif not ("extra_modules.py" in os.listdir(thisdir)):
            return False
        elif not ("courier.py" in os.listdir(thisdir)):
            return False
        elif not ("courier_interface.ui" in os.listdir(thisdir)):
            return False
        elif not ("data_base_1.db" in os.listdir(thisdir)):
            return False
        elif not ("design.ui" in os.listdir(thisdir)):
            return False
        elif not ("main.py" in os.listdir(thisdir)):
            return False
        elif not ("main_design.ui" in os.listdir(thisdir)):
            return False
        elif not ("register_design.ui" in os.listdir(thisdir)):
            return False
        elif not ("shopping_list.txt" in os.listdir(thisdir)):
            return False
        elif not ("user.py" in os.listdir(thisdir)):
            return False
        elif not ("user_interface.ui" in os.listdir(thisdir)):
            return False
        elif not ("111.png" in os.listdir(thisdir)):
            return False
        return True

    def show_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Критическая ошибка")
        msg.setText("Файлы программы повреждены. Открытие невозможно")
        msg.setIcon(QMessageBox.Critical)

        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth = MainWindow()
    sys.exit(app.exec())