import random
import time

def main():
    if start_game().lower() =="e":
            print("Bye bye!")
    else:
        deck = create_shuffled_deck(1)
        player_cards, dealer_cards = send_cards(deck)

        print("So... let's go play!")
        time.sleep(1)

        game(deck, player_cards, dealer_cards)

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

def calculate_points(cards):
    special_cards = ["J", "Q", "K"]

    value_of_cards = 0

    for i in range(len(cards)):
        if i == 0:
            if cards[i][1:] in special_cards:
                value_of_cards = 10
            elif cards[i][1:] == "A":
                value_of_cards = 1
            else:
                value_of_cards = int(cards[i][1:])
        else:
            if cards[i][1:] in special_cards + ["10"]:
                if value_of_cards == 1:
                    value_of_cards += 20
                else:
                    value_of_cards += 10
            elif cards[i][1:] == "A":
                if value_of_cards == 10:
                    value_of_cards += 11
                else:
                    value_of_cards += 1
            else:
                value_of_cards += int(cards[i][1:])

    return value_of_cards

def dealer_round(deck, dealer_points, player_points, dealer_cards):
    print(f"Dealer cards: {' | '.join(dealer_cards)}")
    time.sleep(1)
    
    end_round = False

    while end_round == False:
        if dealer_points > 21:
            print("You win, the dealer busted! The game will be restarted.")
            end_round = True
            return end_round
        elif dealer_points > player_points:
            print("You lost, dealer won! The game will be restarted.")
            end_round = True
            return end_round
        else:
            dealer_cards.append(deck.pop())
            dealer_points = calculate_points(dealer_cards)
            print(f"New dealer card: {dealer_cards[-1]}")
            time.sleep(1)
            continue

def game(deck, player_cards, dealer_cards):
    
    player_points = calculate_points(player_cards)
    dealer_points = calculate_points(dealer_cards)

    if (player_points == 21 and len(player_cards) == 2) and dealer_points != 21:
        print("Congratulations, you won with a BlackJack! The game will be restarted.")
    elif (player_points == 21 and len(player_cards) == 2) and (dealer_points == 21 and len(dealer_cards) == 2):
        print("Draw! You and dealer have Blackjack! The game will be restarted.")
    elif dealer_points == 21:
        print("You lost! Dealer has a BlackJack! The game will be restarted.")
        print(f"Dealer cards: {' | '.join(dealer_cards)}")
    else:
         while True:
            response = input(f"You have {' | '.join(player_cards)}\nType S to stand, H to hint or E to exit\n")
            if response.lower() == 'e':
                break
            elif response.lower() == 's':
                print(f"Your cards: {' | '.join(player_cards)}")

                if dealer_round(deck, dealer_points, player_points, dealer_cards):
                    print(f"Dealer cards: {' | '.join(dealer_cards)}")
                    print(f"Your cards: {' | '.join(player_cards)}")
                    break
            else:
                print(f"Your cards: {' | '.join(player_cards)}")
                time.sleep(1)

                new_player_card = deck.pop()
                player_cards.append(new_player_card)

                print(f"New card: {player_cards[-1]}")
                time.sleep(1)

                player_points = calculate_points(player_cards)

                if player_points > 21:
                    print(f"Your cards: {' | '.join(player_cards)}")
                    print("You lost! Your points passed 21! The game will be restarted.")
                    break
                elif player_points == 21:
                    print(f"Your cards: {' | '.join(player_cards)}")
                    print("21! Congratulations, you won! The game will be restarted.")
                    break
                else:
                    continue

if __name__ == "__main__":
    main()