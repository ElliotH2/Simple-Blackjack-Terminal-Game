# Simple Blackjack Game (Terminal-Based)
# Author: Elliot Huh | GitHub: ElliotH2
# Created: July 6, 2025
#
# Description:
# A terminal-based Blackjack game where the player competes against a dealer.
# The player starts with a user-defined balance and can wager money each round.
# The game follows standard Blackjack rules: hit or stand to get as close to 21
# as possible without going over. Aces can count as 1 or 11.
#
# Features:
# - Input validation for balance and wagers
# - Card drawing and deck management
# - Player and dealer logic
# - Win/loss balance tracking
# - Game continues until the player quits or runs out of money
#
# Run this file with Python 3 in your terminal.
# Example: python3 blackjack.py

import random

#Introduction
print("\n\n******************************************")
print("Welcome to Black Jack")
print("Pick an initial balance amount")
print("Choose how much of your balance you would like to wager")
print("Hit or stand against dealer,")
print("Whoever doesnt busts and is closer to 21 wins")
print("******************************************\n")

#Choose initial balance
while True: #Error handling initial deposit input
    try:
        initial_balance = int(input("Choose amount you want to deposit: "))
        if initial_balance > 0:
            break
        else: #The Initial balance needs to be positive int
            print("Deposit must be positive")
    except ValueError:
        print("Invalid input, numbers only")
print("\n****************************\nGame starting")

rank_values = { #Assigns values to card ranks
    'A': 11, #Ace has two values, defaults to 11
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10
}

def get_hand_value(hand):#logic to calculate total hand value
    total = 0
    aces = 0

    for cards in hand:
        for rank in rank_values:
            if cards.startswith(rank): #Cards start with rank, use numerical values
                total += rank_values[rank]
                if rank == 'A':
                    aces += 1
                break

    #Aces have two values that can be chosen 1 or 11
    #This ensures that the Ace value uses the lower value if the higher value results in a bust
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

#Logic for the deck
def deck_manager(): #Initialize deck
    ranks = list(rank_values.keys())
    suits = ['♠', '♥', '♦', '♣']
    return [f"{rank}{suit}" for rank in ranks for suit in suits] #Combine ranks with suites

balance = initial_balance #Get balance without removing the initial balance

def choose_wager(balance):
    print(f"Your Current Balance is ${balance}")

    # Choose how much of your balance you would like to wager
    while True:  # Error handling wager input
        try:
            wager = int(input("Choose how much of your balance you would like to wager: "))
            if wager <= 0:
                print("Invalid input, positive values only\n")
            elif wager > balance:
                print("You don't have enough money\n")
            elif wager == balance:
                print("You've gone all in, Good Luck")
                return wager
            else:  # Wager input needs to be positive and more than the player's balance
                return wager
        except ValueError:  # If string inputted
            print("Invalid input, numbers only\n")

def play_game(balance): #Logic for each round
    wager = choose_wager(balance)

    deck = deck_manager() #Initialize Deck
    random.shuffle(deck) #Shuffle deck

    #Player and Dealer draws there two initial cards
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    #Calculate the numerical values of both hands
    player_hand_value = get_hand_value(player_hand)
    dealer_hand_value = get_hand_value(dealer_hand)

    #Format output
    display_player_hand = ', '.join(player_hand)
    display_dealer_hand = ', '.join(dealer_hand)

    print(f"\nDealer Hand: [{display_dealer_hand}] Dealer Total Value: {dealer_hand_value}")
    print(f"Player Hand: [{display_player_hand}] Player Total Value: {player_hand_value}\n")

    while player_hand_value < 21: #While value is under 21, player can choose to hit or stand
        print("Choose 1 to hit\nChoose 2 to stand")
        player_choice = input("Your Choice: ")
        print ("\n")

        if player_choice == '1': #If user hits, draw another card
            player_hand.append(deck.pop()) #Draw new card
            player_hand_value = get_hand_value(player_hand) #Calculate new value
            display_player_hand = ', '.join(player_hand) #Format new hand
            print(f"Dealer's hand value: {dealer_hand_value}")
            print(f"You hit: [{display_player_hand}] Your New Total Value: {player_hand_value}\n")

        elif player_choice == '2': #If player stands, restate player cards
            print(f"Dealer's hand value: {dealer_hand_value}")
            print (f"You stand [{display_player_hand}] Your Total Value: {player_hand_value}\n")
            break

        else: #Loop if choice is invalid
            print("Invalid choice, enter 1 or 2\n")

    if player_hand_value > 21: #Player busts
        print ("Your Hand Value:",player_hand_value)
        print ("Bust!")
        balance -= wager #Calculate new balance
        print (f"You lost ${wager}\nNew Balance is ${balance}\n")
        return balance

    #Dealers turn
    while dealer_hand_value < 17: #Dealer hits if their hand values 16 or below
        dealer_hand.append(deck.pop()) #Draw new card
        dealer_hand_value= get_hand_value(dealer_hand) #Calculate new value
        display_dealer_hand = ', '.join(dealer_hand) #Format new hand
        print(f"Dealer hits [{display_dealer_hand}] Total Value: {dealer_hand_value}")

    #Game Results beyond player bust
    if dealer_hand_value > 21:  #If dealer busts
        print("\nDealers Hand Value:",dealer_hand_value)
        print("Dealer Bust!")
        balance += wager #Player wins wager, calculate new balance
        print (f"You won ${wager}\nNew Balance is ${balance}")
        return balance

    if player_hand_value > dealer_hand_value: #If player doesn't bust and closer to 21 than dealer
        print("\nYour Hand Value:",player_hand_value,"Against Dealers Hand Value:",dealer_hand_value)
        balance += wager  #Player wins wager, calculate new balance
        print(f"You won ${wager}\nNew Balance is ${balance}")
        return balance

    if player_hand_value < dealer_hand_value: #If player doesn't bust but dealer is closer to 21
        print("\nYour Hand Value:", player_hand_value, "Against Dealers Hand Value:", dealer_hand_value)
        balance -= wager #Player loses calculate new balance
        print(f"You Lost ${wager}\nNew Balance is ${balance}")
        return balance

    else: #Result of a tie, player doesn't win or lose any money
        print("\nYour Hand Value:", player_hand_value, "Against Dealers Hand Value:", dealer_hand_value)
        print("Tie")
        print(f"Your balance stays at ${balance}")
        return balance

def menu(balance):
    game = True  # Menu loop logic
    while game:  # After the initial game, gives player the choice to play another round

        if balance == 0:  # If you lost all your money
            print(f"\nYou initially had ${initial_balance}")
            print(f"Now you have ${balance}")
            print("You lost all your money")
            print("Game Over")
            game = False

        print("\nChoose 1 to play another round")
        print("Choose 2 to Quit")
        player_choice = input("Your Choice: ")
        print("\n")

        if player_choice == '1':
            balance = play_game(balance)

        if player_choice == '2':  # If player quits, display results
            print(f"\nYou initially had ${initial_balance}")
            print(f"Now you have ${balance}")
            balance_difference = balance - initial_balance
            if balance_difference > 0:  # If player made money
                print(f"Your up by ${balance_difference}")
            elif balance_difference < 0:  # If player lost money
                print(f"Your down by ${abs(balance_difference)}")
            else:  # If player broke even
                print("You broke even")
            print("\nThank You for playing\nGoodbye")
            game = False

balance = play_game(balance) #Initial game
menu(balance) #Loop
