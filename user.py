from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
import sqlite3


con = sqlite3.connect("data_base_1.db")
cur = con.cursor()

shopping = open('shopping_list.txt', 'r', encoding='utf-8')
data = shopping.readline()
item = data.split('; ')
shopping.close()


class User_Main_Window(QWidget):
    def __init__(self, login):
        super().__init__()
        pixmap = QPixmap('111.png')
        self.pixmap = pixmap.scaled(50, 45)
        self.main_logo = QLabel(self)
        self.main_logo.resize(50, 50)
        self.main_logo.setPixmap(self.pixmap)
        self.login = login
        uic.loadUi('user_interface.ui', self)
        self.setWindowTitle('Главная Страница-YandexEda')
        self.total.setMaximum(1000000000)
        self.order_status.hide()
        fio = cur.execute(f"""SELECT user_info.user_fio FROM 
                user_info WHERE user_info.user_login  = '{login}'""").fetchall()[0][0]
        self.hello_lbl.setText(f'Здравствуйте, {fio.split()[1]}')
        self.total.setDisabled(True)
        for elem in item:
            self.chooser_item.addItem(elem)
        self.generate_order.clicked.connect(self.show_generate_order)
        self.my_orders.clicked.connect(self.show_my_orders)
        self.confirm.clicked.connect(self.add_to_generate_order_list)
        self.mk_ord.clicked.connect(self.make_order)
        self.order_list.itemActivated.connect(self.type_order_info)

    def show_generate_order(self):
        self.order_list.clear()
        self.generate_order.setStyleSheet("""font: 10pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);""")
        self.my_orders.setStyleSheet("""font: 10pt "MS Shell Dlg 2";""")
        self.choose_item.show()
        self.chooser_item.show()
        self.confirm.show()
        self.total_lbl.show()
        self.total.show()
        self.mk_ord.show()
        self.order_status.setText('')
        self.order_status.hide()

    def show_my_orders(self):
        self.generate_order.setStyleSheet("""font: 10pt "MS Shell Dlg 2";""")
        self.my_orders.setStyleSheet("""font: 10pt "MS Shell Dlg 2"; background-color: rgb(255, 255, 255);""")
        self.choose_item.hide()
        self.chooser_item.hide()
        self.confirm.hide()
        self.total_lbl.hide()
        self.total.hide()
        self.order_status.show()
        self.mk_ord.hide()
        self.order_list.clear()
        all_orders = cur.execute(f"""SELECT order_list.id
                     FROM order_list WHERE order_list.user_login = '{self.login}'""").fetchall()
        for elem in all_orders:
            if elem[0] is not None:
                self.order_list.addItem(f'Заказ #{str(elem[0])}')

    def add_to_generate_order_list(self):
        text = self.chooser_item.currentText()
        self.order_list.addItem(text)
        text = text.split()
        value = float(self.total.value())
        value += float(text[1])
        self.total.setValue(value)

    def make_order(self):
        datax = []
        for x in range(self.order_list.count()):
            datax.append(self.order_list.item(x))
        data = []
        for elem in datax:
            data.append(elem.text())
        cur.execute(f"""INSERT INTO order_list(item, total_price,
         user_login, stats) VALUES ('{'; '.join(data)}', '{str(self.total.value())}', '{self.login}', 'unsorted')""")
        con.commit()
        self.order_list.clear()
        self.total.setValue(0)

    def type_order_info(self, item):
        try:
            item = item.text().split()
            stat = cur.execute(f"""SELECT order_list.stats
         FROM order_list WHERE order_list.id = {item[1][1:]}""").fetchall()[0][0]
            if stat == 'unsorted':
                stat = 'Заказ еще не подтверждён'
            elif stat == 'sorted':
                stat = 'Заказ подтвержден, скоро он будет доставлен'
            elif stat == 'canceled':
                stat = 'Заказ отклонён курьером, скоро с вами свяжется администратор, для разрешения спора'
            data = cur.execute(f"""SELECT order_list.item, order_list.total_price
         FROM order_list WHERE order_list.id = {item[1][1:]}""").fetchall()[0]
            items = data[0]
            price = data[1]
            courier_logins_1 = cur.execute(f"""SELECT courier_info.courier_fio FROM courier_info,
                 courier_list WHERE courier_list."order" = {item[1][1:]} AND courier_list.courier = courier_info.id""").fetchall()
            courier_logins = [elem[0] for elem in courier_logins_1]
            courier_login = cur.execute(f"""SELECT courier_list.courier_exact_id FROM
                 courier_list WHERE courier_list."order" = {item[1][1:]}""").fetchall()
            if len(courier_login) == 0:
                courier_login = 'Нет назначенного курьера'
                courier_phone = 'Нет назначенного курьера'
            elif courier_login[0][0] is None:
                courier_login = 'Нет назначенного курьера'
                courier_phone = 'Нет назначенного курьера'
            else:
                courier_login = courier_login[0][0]
                courier_phone = cur.execute(f"""SELECT courier_info.courier_phone
                     FROM courier_info WHERE courier_info.id = {courier_login}""").fetchall()[0][0]
                courier_login = cur.execute(f"""SELECT courier_info.courier_fio FROM courier_info
                     WHERE courier_info.id = {courier_login}""").fetchall()[0][0]
            self.order_status.setText(f"""{stat}\nЗаказано: {items}\nИтоговая цена заказа: {price}\nДанные о исполняющем курьере:\n
ФИО курьера: {courier_login}\nНомер телефона курьера: {courier_phone}""")
        except:
            pass