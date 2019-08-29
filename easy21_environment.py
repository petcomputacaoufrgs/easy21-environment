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


    def is_bust(self, player):
        if player.points > 21 or player.points < 0:
            return True
        else:
            return False

    def turn(self, action, player):
        player.rounds += 1

        if player.rounds == 1:
            card_hit = draw_first()
            player.add_card(card_hit)
            return

        if action == 'hit':
            card_hit = draw_card()
            player.add_card(card_hit)

    def step(self, action):
        reward = 0
        done = False

        if action != 'stick':
            self.turn(action, self.player)

            if self.is_bust(self.player):
                return self.player.points, action, -1, True
            else:
                return self.player.points, action, reward, done

        if action == 'stick':
            done = True

            if self.shitty_round(self.dealer) == -1:
                reward = 1
                return self.player.points, action, reward, done

            # If neither went bust
            if self.player.points > self.dealer.points:
                reward = 1
            elif self.player.points < self.dealer.points:
                reward = -1
            else:
                reward = 0

            #print("Reward", reward)
            return self.player.points, action, reward, done

    def shitty_round(self, player):
        curr_action = ''

        while curr_action != 'stick':
            curr_action = player.choose_action()
            self.turn(curr_action, player)

            if self.is_bust(player):
                #print("{} bust at {} points".format(player.name, player.points))
                return -1 # == -1 if player/dealer bust
        return 1



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
#game.episode()
