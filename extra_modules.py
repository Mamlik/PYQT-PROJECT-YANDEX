class Card_Check:
    def __init__(self, card):
        self.card = card

    def get_card_number(self, card):
        card_num = card
        if not (card_num.isdigit() and len(card_num) == 16):
            raise ValueError("Неверный формат номера")
        return card_num

    def double(self, x):
        res = x * 2
        if res > 9:
            res = res - 9
        return res

    def luhn_algorithm(self, card):
        odd = map(lambda x: self.double(int(x)), card[::2])
        even = map(int, card[1::2])
        if (sum(odd) + sum(even)) % 10 == 0:
            return True
        else:
            raise ValueError("Недействительный номер карты")

    def process_data(self):
        try:
            number = self.get_card_number(self.card)
        except ValueError as e:
            return f"Ошибка! {e}"


def check_phone_correct(n):
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