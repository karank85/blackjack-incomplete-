import pygame
from pygame_functions import *
import os
import random

program_icon = pygame.image.load(os.path.join("Assets", "blackjack.jpg"))

pygame.display.set_icon(program_icon)

pygame.font.init()


class Player:
    def __init__(self, name):
        self.balance = 1000
        self.cards = []

    def add_card(self, other):
        self.cards.append(other)
        return None

    def placeBet(self, x):
        self.balance -= x

    def returnBalance(self):
        return self.balance

    def returnCards(self):
        return self.cards


WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CARD_WIDTH, CARD_HEIGHT = 100, 200
VALUE_FONT = pygame.font.SysFont("comicsans", 20)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

VALUE_DICT = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "K": 10,
    "Q": 10,
}


def all_hands():
    suit = {"S", "H", "D", "C"}
    rank = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}
    ans_dct = dict()
    for suits in suit:
        for ranks in rank:
            tup = (ranks, suits)
            ans_dct[tup] = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"{ranks}{suits}.png")),
                                                  (CARD_WIDTH, CARD_HEIGHT))
    return ans_dct


BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'unnamed.jpg')), (WIDTH, HEIGHT))
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlackJack (In development stage)")

FPS = 60


def draw_window(cards, first_total, second_total):
    WINDOW.blit(BACKGROUND_IMG, (0, 0))
    WIDTH_DISPLAY = WIDTH // 2
    HEIGHT_DISPLAY = HEIGHT // 2
    for card in cards:
        WINDOW.blit(card, (WIDTH_DISPLAY, HEIGHT_DISPLAY))
        WIDTH_DISPLAY += 30
        HEIGHT_DISPLAY -= 30

    VALUE_TEXT = VALUE_FONT.render(f"Value: {first_total}/{second_total}", 1, WHITE)
    WINDOW.blit(VALUE_TEXT, (WIDTH_DISPLAY, HEIGHT_DISPLAY + 10))



    pygame.display.update()
    WORD_BOX = makeTextBox(0, 0, 300, 0, "Please enter a number: ", 0, 22)
    showTextBox(WORD_BOX)
    entry = textBoxInput(WORD_BOX)


#def random_card(no_samples):
#    card_keys = list(ALL_CARDS.keys())
#    random_index = random.sample(card_keys, no_samples)
#    ans_lst = []
#    for index in random_index:
#        ans_lst.append(index)
#    return ans_lst


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, RED)
    WINDOW.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1000)


def main():
    ALL_CARDS = all_hands()
    clock = pygame.time.Clock()
    total = 0
    new_total = 0
    run = True
    hand_cards = []
    card_keys = list(ALL_CARDS.keys())
    random_index = random.sample(card_keys, 2)
    selected_card1 = random_index[0]
    selected_card2 = random_index[1]
    if "A" not in selected_card1[0] and "A" not in selected_card2[0]:
        total += VALUE_DICT[selected_card1[0]] + VALUE_DICT[selected_card2[0]]
        new_total += VALUE_DICT[selected_card1[0]] + VALUE_DICT[selected_card2[0]]
    elif "A" in selected_card1[0] and "A" not in selected_card2[0]:
        total += 11 + VALUE_DICT[selected_card2[0]]
        new_total += 1 + VALUE_DICT[selected_card2[0]]
    else:
        total += VALUE_DICT[selected_card1[0]] + 11
        new_total += 1 + VALUE_DICT[selected_card1[0]]

    hand_cards.append(ALL_CARDS[selected_card1])
    del ALL_CARDS[selected_card1]
    hand_cards.append(ALL_CARDS[selected_card2])
    del ALL_CARDS[selected_card2]

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_SPACE]:
                    card_keys = list(ALL_CARDS.keys())
                    random_index = random.sample(card_keys, 1)
                    selected_card = random_index[0]
                    hand_cards.append(ALL_CARDS[selected_card])
                    if "A" not in selected_card[0]:
                        total += VALUE_DICT[selected_card[0]]
                        new_total += VALUE_DICT[selected_card[0]]
                    else:
                        total += 11
                        new_total += 1
                    del ALL_CARDS[selected_card]
                if keys_pressed[pygame.K_r]:
                    main()

        draw_window(hand_cards, total, new_total)
        if total > 21 and new_total > 21:
            draw_winner("Dealer won!")
            break
        elif total == 21 or new_total == 21:
            draw_winner("You won!")
            break

    main()


if __name__ == "__main__":
    main()
