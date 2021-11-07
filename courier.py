from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import sqlite3


con = sqlite3.connect("data_base_1.db")
cur = con.cursor()


class Courier_Main_Window(QWidget):
    def __init__(self, login, id):
        self.user_id = id
        super().__init__()
        uic.loadUi('courier_interface.ui', self)
        self.setWindowTitle('Главная Страница-YandexEda-Courier')
        self.accept.hide()
        self.about_order.hide()
        fio = cur.execute(f"""SELECT courier_info.courier_fio FROM 
        courier_info WHERE courier_info.courier_login  = '{login}'""").fetchall()[0][0]
        self.hello_name.setText(f'Здравствуйте, {fio.split()[1]}')
        self.hello_name.setStyleSheet("""color: #1b1b1b; \n font: 12pt "MS Shell Dlg 2";""")
        orders = cur.execute(f"""SELECT order_list.id FROM
         courier_list, order_list WHERE (courier_list.courier_exact_id = '{id}') AND (courier_list."order" = order_list.id)""").fetchall()
        for elem in set(orders):
            elem = elem[0]
            self.list_1.addItem(f'Заказ {elem}')
        pr_orders = cur.execute(f"""SELECT order_list.id FROM
         courier_list, order_list WHERE (courier_list.courier_exact_id is NULL)
          AND (courier_list."order" = order_list.id) AND (courier_list.courier = {id})""").fetchall()
        for elem in pr_orders:
            elem = elem[0]
            self.list.addItem(f'Заказ {elem}')
        self.list.itemActivated.connect(self.itemActivated_event)
        self.list_1.itemActivated.connect(self.itemActivated_event_1)

    def itemActivated_event_1(self, item):
        if item.text() == '':
            return False
        self.order_id = int(item.text().split()[1])
        self.item = item
        login_user = cur.execute(f"""SELECT order_list.user_login FROM order_list WHERE order_list.id = '{item.text().split()[1]}'""").fetchall()[0][0]
        user_data = cur.execute(f"""SELECT user_info.user_fio, user_info.user_phone_number, user_info.user_adress, order_list.item, order_list.total_price FROM 
                user_info, order_list WHERE (user_info.user_login  = '{login_user}') AND (order_list.id = '{item.text().split()[1]}')""").fetchall()[0]
        self.about_order.show()
        self.about_order.setText(f'Покупатель: {user_data[0]} \n'
                                 f'Номер телефона: {user_data[1]} \nПо адресу: {user_data[2]}'
                                 f'\nСписок заказанных товаров: {", ".join(user_data[3].split(", "))}\n'
                                 f'Стоимость заказа: {user_data[4]} рублей')
        self.about_order.setStyleSheet("""color: #ffffff; \n font: 12pt "MS Shell Dlg 2"; \n background-color: #393939;""")
        self.accept.setText('Отклонить заказ')
        self.accept.show()
        self.accept.clicked.connect(self.deny)

    def itemActivated_event(self, item):
        if item.text() == '':
            return False
        self.order_id = int(item.text().split()[1])
        self.item = item
        login_user = cur.execute(
            f"""SELECT order_list.user_login FROM order_list WHERE order_list.id = '{item.text().split()[1]}'""").fetchall()[
            0][0]
        user_data = cur.execute(f"""SELECT user_info.user_fio, user_info.user_phone_number, user_info.user_adress, order_list.item, order_list.total_price FROM 
                        user_info, order_list WHERE (user_info.user_login  = '{login_user}') AND (order_list.id = '{item.text().split()[1]}')""").fetchall()[
            0]
        self.about_order.show()
        self.about_order.setText(f'Покупатель: {user_data[0]} \n'
                                 f'Номер телефона: {user_data[1]} \nПо адресу: {user_data[2]}'
                                 f'\nСписок заказанных товаров: {", ".join(user_data[3].split(", "))}\n'
                                 f'Стоимость заказа: {user_data[4]} рублей')
        self.about_order.setStyleSheet(
            """color: #ffffff; \n font: 12pt "MS Shell Dlg 2"; \n background-color: #393939;""")
        self.accept.setText('Принять заказ')
        self.accept.show()
        self.accept.clicked.connect(self.Accept)

    def deny(self):
        cur.execute(f"""UPDATE courier_list SET courier_exact_id = NULL WHERE "order" = {self.order_id};""")
        con.commit()
        index = self.list_1.indexFromItem(self.item).row()
        self.list_1.takeItem(index)
        self.list_2.addItem(self.item)

    def Accept(self):
        cur.execute(f"""UPDATE courier_list SET courier_exact_id = '{self.user_id}' WHERE "order" = {self.order_id};""")
        con.commit()
        index = self.list.indexFromItem(self.item).row()
        self.list.takeItem(index)
        self.list_1.addItem(self.item)