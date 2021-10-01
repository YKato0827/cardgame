#class Card →　トランプ（suit=柄,number=数字）
#class Deck →　デッキ（deal=配る,shuffle)
#class Hand →　手札
    #*__init__
        #?player,dealer
        #?cards
        #?value
    #*hit(add_card)
    #*total(calc_value)
    #*is_brackjack()
    #*show()
#class Bet → かけ金の設定
#class Game →　ゲームの詳細　

import random
from time import sleep




#カードを用意（suit, number)
class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __repr__(self):
        return f'{self.suit} {self.number}'

#デッキを用意、カードを作りシャッフル
class Deck:
    def __init__(self):
        suits = [{'mark':'♤','rank':1},
                 {'mark':'♧','rank':2},
                 {'mark':'♥','rank':3},
                 {'mark':'♦','rank':4}
                 ]
        numbers = [
            {'num': 'A', 'value': 11},
            {'num':'2', 'value': 2},
            {'num': '3', 'value': 3},
            {'num': '4', 'value': 4},
            {'num': '5', 'value': 5},
            {'num': '6', 'value': 6},
            {'num': '7', 'value': 7},
            {'num': '8', 'value': 8},
            {'num': '9', 'value': 9},
            {'num': '10', 'value': 10},
            {'num': 'J', 'value': 10},
            {'num': 'Q', 'value': 10},
            {'num': 'K', 'value': 10},
            ]

        self.cards = []
        for suit in suits:
            for number in numbers:
                self.cards.append(Card(suit, number))

    def deal(self):
        return self.cards.pop(0)

    def shuffle(self):
        random.shuffle(self.cards)
#ここまでは全トランプゲームで流用　

#ディーラーと自分にハンドを配る
class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.total = 0

    def add_card(self, card):
        self.cards.append(card)

    def calc_value(self): #ブール型(True or False)
        self.value = 0
        ace = False
        for card in self.cards:
            self.value += int(card.number['value'])
            if card.number['num'] == 'A':
                ace = True

        if ace and self.value > 21:
            self.value -= 10

        return self.value

    def is_blackjack(self):
        return self.calc_value() == 21

    def show(self, show_two_cards=False):
        #if self.dealer:
        #   print('Dealer hand:')
        #else:
        #   print('Your hand:')

        print(f"{'ディーラー' if self.dealer else 'あなた'} の手は:")
        #f<Trueの時に返す>　if <条件> else <Falseの時に返す>

        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_two_cards and not self.is_blackjack():
                pass
            else:
                print(f"{card.suit['mark']}{card.number['num']}")
        if not self.dealer:
            print('Total:', self.calc_value())
        print()

class Bet:
    def __init__(self, player_bet=False):
        self.stock = 1000
        self.player_bet = player_bet
        print('開始所持金額は', self.stock)

    def bet(self):
        print('所持金額は'+ '\033[31m' + str(self.stock)  + '\033[0m')
        self.player_bet = int(input('いくらベットしますか：'))
        while self.player_bet > self.stock:
            print('所持金額を超えています')
            self.player_bet = int(input('いくらベットしますか：'))
        return self.player_bet

    def win_result(self, player_bet=False):
        self.stock += self.player_bet
        print('ストックは' + '\033[31m' + str(self.stock)  + '\033[0m' + 'になりました')
        return self.stock

    def lose_result(self, player_bet=False):
        self.stock -= self.player_bet
        print('ストックは' + '\033[31m' + str(self.stock)  + '\033[0m' + 'になりました')
        return self.stock

    def draw_result(self, player_bet=False):
        self.stock += 0
        print('ストックは' + '\033[31m' + str(self.stock)  + '\033[0m' + 'になりました')
        return self.stock

class Game():
    def check_winner(self, player_hand, dealer_hand, player_call, game_over=False):
        if not game_over:
            if player_hand.calc_value() > 21:
                print('あなたは21を超えました. Dealer wins!')
                player_call.lose_result(player_bet=True)
                return True
            elif dealer_hand.calc_value() > 21:
                print('ディーラーは21を超えました. You win!')
                player_call.win_result(player_bet=True)
                return True
            elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
                print('ふたりともブラックジャックです. Draw!')
                player_call.draw_result(player_bet=True)
                return True
            elif player_hand.is_blackjack():
                print('あなたはブラックジャックです! You win!')
                player_call.win_result(player_bet=True)
                return True
            elif dealer_hand.is_blackjack():
                print('ディーラーはブラックジャックです! Dealer wins!')
                player_call.lose_result(player_bet=True)
                return True
        else:
            if player_hand.calc_value() > dealer_hand.calc_value():
                print('あなたの勝ちです!')
                player_call.win_result(player_bet=True)
            elif player_hand.calc_value() == dealer_hand.calc_value():
                print('引き分けです！')
                player_call.draw_result(player_bet=True)
            else:
                print('残念、ディーラーの勝ちです...!')
                player_call.lose_result(player_bet=True)
            return True
        return False

    def play(self):
        game_to_play = 0
        game_number = 0

        while game_to_play <= 0:
            try:                    #例外エラーの処理
                game_to_play = int(input('何回プレイしますか:'))
            except ValueError:     #拾うエラーを指定（わからないときはException)
                print('数字を入力してください')

            player_call = Bet()

        while game_number < game_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for i in range(2):
                player_hand.add_card(deck.deal())
                dealer_hand.add_card(deck.deal())

            print()
            sleep(1)
            print(f"ゲームの回数 {game_number}/{game_to_play}")
            sleep(1)
            print()

            player_call.bet()

            player_hand.show()
            dealer_hand.show()

            if self.check_winner(player_hand, dealer_hand, player_call):
                continue
            print('ヒットかスタンドか選択してください')

            choice = ''
            while choice not in {'s', 'stand'} and player_hand.calc_value() < 21:
                choice = input('ヒットまたはスタンドをしてください（h/s）:').lower()
                print()
                while choice not in ['h', 's']:
                    choice = input('ヒットまたはスタンドをしてください（h/s)').lower()
                    print()
                if choice in ['h']:
                    player_hand.add_card(deck.deal())
                    player_hand.show()

            sleep(0.5)
            dealer_hand.show(show_two_cards=True)
            dealer_hand.calc_value()
            print(dealer_hand.calc_value())
            print()

            if self.check_winner(player_hand, dealer_hand, player_call):
                continue
            print('ディーラーは17までカードを引きます')
            sleep(1)

            while dealer_hand.calc_value() < 17:
                sleep(1)
                dealer_hand.add_card(deck.deal())
                dealer_hand.show(show_two_cards=True)
                dealer_hand.calc_value()
                sleep(0.5)
                print(dealer_hand.calc_value())
                print()
                sleep(1)

            if self.check_winner(player_hand, dealer_hand, player_call):
                continue

            sleep(1)
            print()
            print('結果発表')
            print()
            sleep(1)
            print('あなたのハンド:', player_hand.calc_value())
            print('ディーラーのハンド:', dealer_hand.calc_value())
            sleep(0.5)

            self.check_winner(player_hand, dealer_hand, player_call, game_over=True)

game = Game()
game.play()