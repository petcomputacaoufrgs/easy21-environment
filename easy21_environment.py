import numpy as np


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def __str__(self):
        return "Color = " + self.color + "\n" + str(self.value)


class Player:
    def __init__(self, points, name):
        self.points = points
        self.name = name

    def take_turn(self, action):
        if action == 'hit':
            card_hit = draw_card()
            self.add_card(card_hit)

    def add_card(self, card):
        if card.color == 'red':
            card.value *= -1

        self.points += card.value

    def __str__(self):
        return self.name + " has {} points.".format(self.points)


class Game:

    def __init__(self):
        """ Easy21 """

        self.player = Player(0, "Player")
        self.dealer = Player(0, "Dealer")

        self.game_over = False

    def turn(self, action, player):
        if action == 'hit':
            card_hit = draw_card()
            player.add_card(card_hit)

    def main_loop(self):
        player_bust = False
        dealer_bust = False

        reward = 0

        curr_action = ''

        while not player_bust and curr_action != 'stick':
            curr_action = input('You currently have {} points.\nDo you stick or hit?\n'.format(self.player.points))
            self.turn(curr_action, self.player)

            if self.player.points > 21 or self.player.points < 0:
                print("bust at {} points".format(self.player.points))
                player_bust = True

        if player_bust:
            reward = -1
        else:
            curr_action = ''

            while not dealer_bust and curr_action != 'stick':
                if self.dealer.points >= 17:
                    curr_action = 'stick'
                else:
                    curr_action = 'hit'

                self.dealer.take_turn(curr_action)

                if self.dealer.points > 21 or self.dealer.points < 0:
                    dealer_bust = True
                    print("Dealer bust at {} points".format(self.dealer.points))

            if dealer_bust:
                reward = 1

        if not dealer_bust and not player_bust:
            print("Player points", str(self.player.points))
            print("Dealer points", str(self.dealer.points))
            if self.player.points > self.dealer.points:
                reward = 1
            elif self.player.points < self.dealer.points:

                reward = -1
            else:
                reward = 0

        print('Reward:')
        print(reward)


def draw_card():
    colors = ['red', 'black']
    probabilities = [1 / 3, 2 / 3]  # chance to draw red = 1/3, chance to draw black = 2/3

    random_value = np.random.choice(list(range(1, 10)))
    random_color = np.random.choice(colors, p=probabilities)

    random_card = Card(random_value, random_color)

    return random_card


def draw_first():
    random_value = np.random.choice(list(range(1, 10)))

    first_card = Card(random_value, 'black')
    return first_card

game = Game()
game.main_loop()