import sys
import sqlite3
from card_check import Card_Check
from courier import *
from user import *
from admin import *
con = sqlite3.connect("data_base_1.db")
cur = con.cursor()
ADMIN_LOGIN = 'ADMIN'
ADMIN_PASSWORD = 'ADMIN'


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
        self.user = User_Main_Window()
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
        if self.check_phone_correct(self.phone.text()) is False:
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
            cur.execute(f"""INSERT INTO user_info(user_login, user_password,
             user_fio, user_adress, user_card_num, user_card_working_date, user_card_name_holder, user_cvc,
              user_phone_number) VALUES ('{login}', '{password}', '{fio}', '{adress}',
'{card_num}', '{card_date}', '{card_holder}', '{cvc}', '{phone}');""")
            con.commit()
            self.user = User_Main_Window()
            self.user.show()
            self.close()

    def check_phone_correct(self, n):
        if len(n) == 0:
            return False
        mts = list(range(910, 919 + 1)) + list(range(980, 989 + 1))
        megafon = list(range(920, 939 + 1))
        beline = list(range(960, 969 + 1)) + list(range(902, 906 + 1))
        try:
            n = n.strip()
            if n[0:2] != '+7':
                if n[0] != '8':
                    print(3 / 0)
            n = n.replace(' ', '')
            n = n.replace('\t', '')
            flag = False
            flag1 = False
            if n.count('(') > 1 or n.count(')') > 1:
                print(3 / 0)
            elem1 = 0
            elem2 = 0
            for elem in n:
                if elem == '(':
                    flag = True
                    elem1 = n.index(elem)
                if elem == ')':
                    if flag:
                        flag1 = True
                        elem2 = n.index(elem)
                        break
            if elem2 != 0:
                n = n.replace(n[elem1], '')
                n = n.replace(n[elem2 - 1], '')
            if n.count('(') > 0 or n.count(')') > 0:
                print(3 / 0)

            if n[-1] == '-':
                print(3 / 0)
            n = n.split('-')
            if '' in n:
                n[n.index('')] = '-'
            n = ''.join(n)
            if '-' in n:
                print(3 / 0)
            if n[0] == '8':
                n = '+7' + n[1:]
            if len(n) == 12:
                if n[1:].isdigit():
                    format = int(n[2:5])
                    if format not in mts and format not in megafon and format not in beline:
                        return False
                    return True
                else:
                    print(3 / 0)
            else:
                print(len(1))
        except ZeroDivisionError:
            return False
        except TypeError:
            return False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_design.ui', self)
        self.setWindowTitle('YandexEda')
        self.widget = Authorization()
        self.widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth = MainWindow()
    sys.exit(app.exec())