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
        self.rounds = 0

    def take_turn(self, action):
        self.rounds += 1

        if self.rounds == 1:
            card_hit = draw_first()
            self.add_card(card_hit)

        if action == 'hit':
            card_hit = draw_card()
            self.add_card(card_hit)


    def choose_action(self):
        curr_action = input('You currently have {} points.\nDo you stick or hit?\n'.format(self.points))
        return curr_action

    def add_card(self, card):
        if card.color == 'red':
            card.value *= -1

        self.points += card.value

    def __str__(self):
        return self.name + " has {} points.".format(self.points)


class Dealer(Player):
    def __init__(self, points, name):
        super().__init__(points, name)

    def choose_action(self):
        if self.points >= 17:
            curr_action = 'stick'
        else:
            curr_action = 'hit'

        return curr_action


class Game:

    def __init__(self):
        """ Easy21 """

        self.player = Player(0, "Player")
        self.dealer = Dealer(0, "Dealer")

        self.game_over = False

    def is_bust(self, player):
        if player.points > 21 or player.points < 0:
            return True
        else:
            return False

    def turn(self, action, player):
        if action == 'hit':
            card_hit = draw_card()
            player.add_card(card_hit)

    def shitty_round(self, player):
        curr_action = ''

        while curr_action != 'stick':
            curr_action = player.choose_action()
            self.turn(curr_action, player)

            if self.is_bust(player):
                print("{} bust at {} points".format(player.name, player.points))
                return -1 # == -1 if player/dealer bust
        return 1

    def episode(self):

        if self.shitty_round(self.player) == -1:
            reward = -1
            return reward

        # if the player didn't bust

        if self.shitty_round(self.dealer) == -1:
            reward = 1
            return reward

        # If neither busted
        if self.player.points > self.dealer.points:
            reward = 1
        elif self.player.points < self.dealer.points:
            reward = -1
        else:
            reward = 0

        print('Reward:')
        print(reward)
        return reward


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
game.episode()
