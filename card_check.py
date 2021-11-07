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