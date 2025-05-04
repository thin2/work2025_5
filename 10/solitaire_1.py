import random
def shuffle_deck(seed_value):
    random.seed(seed_value)
    deck = [i for i in range(32)]  # 52 cards
    random.shuffle(deck)
    return deck
utput=[]
remove_deck = []
clubs_A = []
clubs_K = []
hearts_A = []
hearts_K = []
diamonds_A = []
diamonds_K = []
spades_A = []
spades_K = []
SUITS = {
    'Hearts': 0x1F0B0,
    'Diamonds': 0x1F0C0,
    'Clubs': 0x1F0D0,
    'Spades': 0x1F0A0
}

VALUES = ['A', '7', '8', '9', '10', 'J', 'Q', 'K']
PICTURES = {10, 11, 12, 23, 24, 25, 36, 37, 38, 49, 50, 51}
def card_to_unicode(card):
    cards = [
    '🂱', '🂷', '🂸', '🂹', '🂺', '🂻', '🂽', '🂾',  # Hearts
    '🃁', '🃇', '🃈', '🃉', '🃊', '🃋', '🃍', '🃎',  # Diamonds
    '🃑', '🃗', '🃘', '🃙', '🃚', '🃛', '🃝', '🃞',  # Clubs
    '🂡', '🂧', '🂨', '🂩', '🂪', '🂫', '🂭', '🂮'   # Spades
    ]

    return cards[card]
suit_mapping = {
    1: (hearts_A, hearts_K),
    2: (diamonds_A, diamonds_K),
    3: (clubs_A, clubs_K),
    4: (spades_A, spades_K),
}
dict={
    1:'first',
    2:'second',
    3:'third',
    4:'4th',
    5:'5th',
    6:'6th',
    7:'7th',
    8:'8th',
    9:'9th',
    10:'10th',
}

card_values = {
    0: 'A',
    12: 'K',
}
if __name__ == '__main__':
    seed_value = int(input("Enter the seed value: "))
    deck = shuffle_deck(seed_value)
    list_card_1 = []
    list_card_2 = []
    list_card_3 = []
    list_card_4 = []
    for i, card in enumerate(deck[::-1]):
        if i%4==0:
            list_card_1.append(card_to_unicode(card))
        elif i%4==1:
            list_card_2.append(card_to_unicode(card))
        elif i%4==2:
            list_card_3.append(card_to_unicode(card))
        elif i%4==3:
            list_card_4.append(card_to_unicode(card))
    print(list_card_1)
    print(list_card_2)
    print(list_card_3)
    print(list_card_4)