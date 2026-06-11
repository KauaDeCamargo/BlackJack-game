import random
import time

def main():
    if start_game().lower() =="e":
            print("Bye bye!")
    else:
        deck_shuffled = create_shuffled_deck(1)
        player_cards, dealer_cards = send_cards(deck_shuffled)
        player_points, dealer_points = calculate_points(player_cards, dealer_cards)
        print(player_cards)
        print(dealer_cards)
        print(player_points)
        print(dealer_points)

def start_game():
    print("-" * 10)
    print("Hello, welcome to Camargo Casino!")
    print("In the house, we still have the BlackJack game. New games is coming soon...")
    print("We are a new Casino. Bets aren't open yet! If you want to bet, wait for features.")
    print("-" * 10)
    
    begin_response = input("Type 'S' to start BlackJack or 'E' to exit.\n")
    
    return begin_response
    
def create_shuffled_deck(num_decks):
    print("Shuffle deck...")
    time.sleep(2)

    suits = ["♠", "♥", "♦", "♣"]
    numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    numbers = numbers * num_decks

    deck = [suit + numero for suit in suits for numero in numbers]

    random.shuffle(deck)

    print("Deck shuffled!")
    return deck

def send_cards(deck):
    player_cards = []
    dealer_cards = []

    print("Sending cards...")
    time.sleep(2)

    player_cards.append(deck.pop())
    print(f"Your first card: {player_cards[0]}")
    time.sleep(1)

    dealer_cards.append(deck.pop())
    print(f"Dealer first card: {dealer_cards[0]}")
    time.sleep(1)

    player_cards.append(deck.pop())
    print(f"Your cards: {' | '.join(player_cards)}")
    time.sleep(1)

    dealer_cards.append(deck.pop())
    print(f"Dealer cards: {dealer_cards[0]} | HIDE")
    time.sleep(1)

    return player_cards, dealer_cards

def calculate_points(player_cards, dealer_cards):
    print("So... let's go play!")
    time.sleep(1)

    special_cards = ["J", "Q", "K"]

    player_points = 0
    dealer_points = 0

    for i in range(2):
        if i == 0:
            if player_cards[i][1:] in special_cards:
                player_points = 10
            elif player_cards[i][1:] == "A":
                player_points = 1
            else:
                player_points = int(player_cards[i][1:])
        else:
            if player_cards[i][1:] in special_cards:
                if player_points == 1:
                    player_points += 20
                else:
                    player_points += 10
            elif player_cards[i][1:] == "A":
                if player_points == 10:
                    player_points += 11
                else:
                    player_points += 1
            else:
                player_points += int(player_cards[i][1:])
    
    for i in range(2):
        if i == 0:
            if dealer_cards[i][1:] in special_cards:
                dealer_points = 10
            elif dealer_cards[i][1:] == "A":
                dealer_points = 1
            else:
                dealer_points = int(dealer_cards[i][1:])
        else:
            if dealer_cards[i][1:] in special_cards:
                if dealer_points == 1:
                    dealer_points += 20
                else:
                    dealer_points += 10
            elif dealer_cards[i][1:] == "A":
                if dealer_points == 10:
                    dealer_points += 11
                else:
                    dealer_points += 1
            else:
                dealer_points += int(dealer_cards[i][1:])

    return player_points, dealer_points

if __name__ == "__main__":
    main()