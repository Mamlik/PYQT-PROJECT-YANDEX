from PyQt5 import uic, Qt
from PyQt5.QtWidgets import QWidget
import sqlite3
from PyQt5.QtCore import Qt


con = sqlite3.connect("data_base_1.db")
cur = con.cursor()


class Admin_Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('admin_interface.ui', self)
        self.setWindowTitle('Главная Страница-YandexEda-Admin')
        courier_list = cur.execute("""SELECT courier_info.courier_fio, courier_info.id FROM courier_info""").fetchall()
        courier_id = [elem[0] for elem in courier_list]
        for elem in courier_list:
            self.courier_list.addItem(f'{elem[0]},  (id {elem[1]})')
        self.courier_list.itemActivated.connect(self.type_courier_info)
        self.unsorted_orders.stateChanged.connect(self.show_unsorted_orders)
        self.canceled_orders.stateChanged.connect(self.show_canceled_orders)
        self.sorted_orders.stateChanged.connect(self.show_sorted_orders)
        self.order_list.itemActivated.connect(self.type_order_info)
        self.exp_lbl.hide()
        self.confirm_btn.hide()
        self.confirm_btn.clicked.connect(self.change_status_to_sorted)

    def type_courier_info(self, item):
        self.courier = item
        item = item.text()
        fio = item.split(',  ')[0]
        id = item.split(',  ')[1]
        id = id[4:len(id) - 1]
        courier_data = cur.execute(f"""SELECT courier_info.courier_login
        , courier_info.courier_phone FROM courier_info WHERE courier_info.id = {id}""").fetchall()[0]
        self.courier_info.setText(f'Курьер: {fio}\nНомер телефона курьера: {courier_data[1]}\nЛогин курьера: {courier_data[0]}')

    def type_order_info(self, item):
        self.item_ = item
        item = item.text()
        stats = cur.execute(
            f"""SELECT order_list.stats FROM order_list WHERE order_list.id = {item.split()[1][1:]}""").fetchall()[0][0]
        if stats == 'unsorted':
            self.exp_lbl.setText('Нажмите на кнопку, чтобы подтвердить заказ')
            self.exp_lbl.show()
            self.confirm_btn.setText('Подтвердить заказ')
            self.confirm_btn.show()
        elif stats == 'sorted':
            self.exp_lbl.setText('Выберите курьера, после чего нажмите на кнопку, чтобы назначить его на заказ')
            self.exp_lbl.show()
            self.confirm_btn.setText('Назначить курьера')
            self.confirm_btn.show()
        login_user = cur.execute(
            f"""SELECT order_list.user_login FROM order_list WHERE order_list.id = '{item.split()[1][1:]}'""").fetchall()[0][0]
        user_data = cur.execute(f"""SELECT user_info.user_fio, user_info.user_phone_number, user_info.user_adress,
         order_list.item, order_list.total_price FROM 
                                user_info, order_list WHERE (user_info.user_login  = '{login_user}')
                                 AND (order_list.id = '{item.split()[1][1:]}')""").fetchall()[0]
        courier_logins_1 = cur.execute(f"""SELECT courier_info.courier_fio FROM courier_info,
         courier_list WHERE courier_list."order" = {item.split()[1][1:]} AND courier_list.courier = courier_info.id""").fetchall()
        courier_logins = [elem[0] for elem in courier_logins_1]
        courier_login = cur.execute(f"""SELECT courier_list.courier_exact_id FROM
         courier_list WHERE courier_list."order" = {item.split()[1][1:]}""").fetchall()[0][0]
        if courier_login is None:
            courier_login = 'Нет назначенного курьера'
            courier_phone = 'Нет назначенного курьера'
        else:
            courier_phone = cur.execute(f"""SELECT courier_info.courier_phone
             FROM courier_info WHERE courier_info.id = {courier_login}""").fetchall()[0][0]
            courier_login = cur.execute(f"""SELECT courier_info.courier_fio FROM courier_info
             WHERE courier_info.id = {courier_login}""").fetchall()[0][0]
        stats = cur.execute(
            f"""SELECT order_list.stats FROM order_list WHERE order_list.id = {item.split()[1][1:]}""").fetchall()[0][0]
        self.about_order.show()
        self.about_order.setText(f'Статус заказа: {stats}\n'
                                 f'Покупатель: {user_data[0]} \n'
                                 f'Номер телефона: {user_data[1]} \nПо адресу: {user_data[2]}'
                                 f'\nСписок заказанных товаров: {", ".join(user_data[3].split(", "))}\n'
                                 f'Стоимость заказа: {user_data[4]} рублей\n \n \n \n '
                                 f'Назначено курьерам:\n \n {";    ".join(courier_logins)}\n \n \n \n \n'
                                 f'Заказ исполняет: {courier_login}\n'
                                 f'Номер телефона курьера: {courier_phone}')

    def show_unsorted_orders(self):
        if self.unsorted_orders.isChecked():
            orders = cur.execute("""SELECT order_list.id FROM order_list WHERE order_list.stats = 'unsorted'""").fetchall()
            for elem in orders:
                self.order_list.addItem(f'Заказ #{elem[0]}')
        else:
            orders = cur.execute(
                """SELECT order_list.id FROM order_list WHERE order_list.stats = 'unsorted'""").fetchall()
            for elem in orders:
                item = self.order_list.findItems(f'Заказ #{elem[0]}', Qt.MatchExactly)[0]
                index = self.order_list.indexFromItem(item).row()
                self.order_list.takeItem(index)

    def show_sorted_orders(self):
        if self.sorted_orders.isChecked():
            orders = cur.execute("""SELECT order_list.id FROM order_list WHERE order_list.stats = 'sorted'""").fetchall()
            for elem in orders:
                self.order_list.addItem(f'Заказ #{elem[0]}')
        else:
            orders = cur.execute(
                """SELECT order_list.id FROM order_list WHERE order_list.stats = 'sorted'""").fetchall()
            for elem in orders:
                item = self.order_list.findItems(f'Заказ #{elem[0]}', Qt.MatchExactly)[0]
                index = self.order_list.indexFromItem(item).row()
                self.order_list.takeItem(index)

    def show_canceled_orders(self):
        if self.canceled_orders.isChecked():
            orders = cur.execute("""SELECT order_list.id FROM order_list WHERE order_list.stats = 'canceled'""").fetchall()
            for elem in orders:
                self.order_list.addItem(f'Заказ #{elem[0]}')
        else:
            orders = cur.execute(
                """SELECT order_list.id FROM order_list WHERE order_list.stats = 'canceled'""").fetchall()
            for elem in orders:
                item = self.order_list.findItems(f'Заказ #{elem[0]}', Qt.MatchExactly)[0]
                index = self.order_list.indexFromItem(item).row()
                self.order_list.takeItem(index)

    def change_status_to_sorted(self):
        stats = cur.execute(
            f"""SELECT order_list.stats FROM order_list WHERE order_list.id = {self.item_.text().split()[1][1:]}""").fetchall()[0][0]
        if stats == 'unsorted':
            item = self.order_list.findItems(f'Заказ #{self.item_.text().split()[1][1:]}', Qt.MatchExactly)[0]
            index = self.order_list.indexFromItem(item).row()
            self.order_list.takeItem(index)
            cur.execute(f"""UPDATE order_list SET stats = 'sorted' WHERE order_list.id = {self.item_.text().split()[1][1:]}""")
            con.commit()
            self.exp_lbl.hide()
            self.confirm_btn.hide()
        elif stats == 'sorted':
            print(self.courier.text())
            id_ = self.courier.text().split(',  ')[1]
            id_ = id_[3:len(id_) - 1]
            cur.execute(f"""INSERT INTO courier_list("order", courier,
             courier_exact_id) VALUES ({self.item_.text().split()[1][1:]}, {id_}, NULL)""")
            con.commit()