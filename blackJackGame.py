import random
import time
from dotenv import load_dotenv
import os
import openai
from pydantic import BaseModel

class BlackJackTip(BaseModel):
    decision: str
    confidence: float
    details: str

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
    aces = 0

    for card in cards:
        value = card[1:]
        if value in special_cards:
            value_of_cards += 10
        elif value == "A":
            aces += 1
            value_of_cards += 11
        else:
            value_of_cards += int(value)

    while value_of_cards > 21 and aces > 0:
        value_of_cards -= 10
        aces -= 1

    return value_of_cards

def dealer_round(deck, dealer_points, player_points, dealer_cards):
    print(f"Dealer cards: {' | '.join(dealer_cards)}")
    time.sleep(1)
    
    while dealer_points < 17:
        dealer_cards.append(deck.pop())
        dealer_points = calculate_points(dealer_cards)
        print(f"New dealer card: {dealer_cards[-1]}")
        time.sleep(1)

    if dealer_points > 21:
        print("You win, the dealer busted! The game will be restarted.")
        return True
    elif dealer_points > player_points:
        print("You lost, dealer won! The game will be restarted.")
        return True
    elif dealer_points < player_points:
        print("You win! You have more points than dealer! The game will be restarted.")
        return True
    else:
        print("Draw! You and the dealer have the same points! The game will be restarted.")
        return True

def call_ai_tip(player_cards, dealer_cards):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    player_cards_str = ", ".join(player_cards)
    if len(dealer_cards) == 2:
        dealer_cards_str = dealer_cards[0]
    else:
        dealer_cards_str = ", ".join(dealer_cards)

    client = openai.OpenAI(api_key=api_key)

    ai_response = client.responses.parse(
        model="gpt-5.5",
        input=f"""
                You are a Blackjack assistant.

                Your role is to help the player make the best possible decision using standard Blackjack strategy, mathematics, and probability.

                You only know the cards visible to the player.

                Player cards:
                {player_cards_str}

                Dealer visible card:
                {dealer_cards_str}

                Based on the available information, recommend exactly one action:

                - Hit
                - Stand

                Briefly explain your reasoning in no more than three sentences.
                """,
        text_format=BlackJackTip
    )
    parsed_output = ai_response.output_parsed

    print(f"AI Decision: {parsed_output.decision}")
    print(f"Confidence: {parsed_output.confidence}")
    print(f"Details: {parsed_output.details}")

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
            response = input(f"You have {' | '.join(player_cards)}\nType S to stand, H to hit, A to AI tip or E to exit\n")
            if response.lower() == 'e':
                break
            elif response.lower() == 's':
                print(f"Your cards: {' | '.join(player_cards)}")

                if dealer_round(deck, dealer_points, player_points, dealer_cards):
                    print(f"Dealer cards: {' | '.join(dealer_cards)}")
                    print(f"Your cards: {' | '.join(player_cards)}")
                    break
            elif response.lower() == 'a':
                call_ai_tip(player_cards, dealer_cards)
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