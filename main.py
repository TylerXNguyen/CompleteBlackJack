# pycharms python for work
import numpy as np
import random
from IPython.display import clear_output
# clear_output()

def createStop(num_decks):
    # This function provides a value for when the shoe is stopped and reshuffled
    # Takes a value from normal distribution between midpoint and end of entire shoe
    # inputs:
    # num_decks (int) - amount of decks to use
    ## outputs:
    # (int) - number for card to stop at'

    a = (num_decks * 52 / 2)  # midpoint bound
    b = (num_decks * 52 / 2) + (num_decks * 52 / 4)  # upper bound

    # Step 2: Calculate the mean and standard deviation
    mean = (a + b) / 2  # Midpoint
    std_dev = (b - a) / 6  # Standard deviation; adjust as needed

    # Step 3: Generate random numbers with a normal distribution
    data = np.random.normal(mean, std_dev, 1)

    maxIndex = num_decks * 52 - 20  # 20 is value determined by min amount of cards to play last hand
    return_value = int(data[0])  # number to return

    while return_value >= maxIndex:
        # step incase the cut is too deep (not enough cards)
        # Recursive
        return_value = createStop(num_decks)

    return return_value


def createShoe(num_decks):
    # This function makes a list of all the cards based on how many decks to shuffle
    # inputs:
    # num_decks (int) - amount of decks to use
    ## outputs:
    # (list) - combination of shuffled cards in the shoe
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, [1, 11]]
    suits = ['♠', '♣', '♦', '♥']
    deck = [f'[{r}{s}]' for r in ranks for s in suits]
    decks = deck * num_decks
    random.shuffle(decks)

    return decks


def printUpdatedBalance(amt_to_change):
    # This function prints the balance and what happened in the correct format
    # inputs:
    # amt_to_change (float) - value that will change the balance
    # outputs:
    # A formatted print of the balance and the effect while also changing the global variable
    global balance

    print(f'Old Balance: ${balance} + ${amt_to_change}')
    balance += amt_to_change
    print(f'New Balance: ${balance}')
    print()


def checkPlayerHandSum(player_hand_index):
    # This function finds the value of the sum of the player's hand
    # inputs:
    # player_hand_index (int) - the index for which hand the player to calculate
    # output:
    # a 2 element list that shows the soft and hard value summed up of the hand, if the 2 values are the same, then there is no soft or hard value
    global card_Values
    global player_hand

    # Calculates player cards values
    player_values = [card_Values[card[1:2]] for card in
                     player_hand[player_hand_index]]  # gets corresponding value for each card
    normalized_plist = [
        card if isinstance(card, list) else [card, card]
        for card in player_values
    ]  # makes it so if there's ace, have a hard and soft value
    sumphand = [sum(value) for value in zip(*normalized_plist)]  # sums up the hard and soft values

    return (sumphand)


def printHands():
    # This function prints both dealer and player hands
    global dealer_hand
    global dealer_values
    global player_hand
    global hand_finished

    output = '\tDealer: '

    if hand_finished == 0:
        # only showing first dealer card
        if dealer_hand[0][1:2] != 'A':
            # When dealer not showing ace
            output += f'{dealer_hand[0]} \t\t\t ({dealer_values[0]})'
        else:
            # When dealer shows an ace
            output += f'{dealer_hand[0]} \t\t\t (11/1)'
    elif hand_finished == 1:
        # after dealer finishes turn
        for dcard in dealer_hand:
            # prints every card in the dealer's hand
            output += dcard
            output += ' '

        output += '\t\t\t'

        # Prints dealer value depending on logic
        if sumdhand[0] == sumdhand[1]:
            # When there is no ace
            output += f'({sumdhand[0]})'
        elif sumdhand[0] == 21:
            # Player Blackjack
            output += 'BLACKJACK!'
        elif sumdhand[0] <= 21:
            # Player has at least one ace
            output += f'({sumdhand[0]})/({sumdhand[1]})'
        elif sumdhand[0] > 21:
            # Player has at 2 aces
            output += f'({sumdhand[1]})'
        else:
            print('ERROR CHECK')
            output += '\n'

    for i in range(len(player_hand)):
        # go through each of the player's hand
        # Calculates player cards values
        player_values = [card_Values[card[1:2]] for card in player_hand[i]]  # gets corresponding value for each card
        normalized_plist = [
            card if isinstance(card, list) else [card, card]
            for card in player_values
        ]  # makes it so if there's ace, have a hard and soft value
        sumphand = [sum(value) for value in zip(*normalized_plist)]  # sums up the hard and soft values

        output += f'\n\tHand {i + 1}: '

        for j in range(len(player_hand[i])):
            output += player_hand[i][j]
            output += ' '

        output += '\t\t '

        # Prints player hand depending on logic
        if sumphand[0] == sumphand[1]:
            # When there is no ace
            output += f'({sumphand[0]})'
        elif sumphand[0] == 21:
            # Player Blackjack
            output += 'BLACKJACK!'
        elif sumphand[0] <= 21:
            # Player has at least one ace
            output += f'({sumphand[0]})/({sumphand[1]})'
        elif sumphand[0] > 21:
            # Player has at 2 aces
            output += f'({sumphand[1]})'
        else:
            print('ERROR CHECK')
            output += '\n'

    print(output)


def checkForWin():
    # Check for Win
    global sumdhand
    global sumphand
    global dealer_hand
    global dealer_values
    global card_Values
    global player_hand
    global player_values
    global shoe_index
    global shoe
    global hand_finished

    while sumdhand[0] < 17 and sumdhand[1] < 17:
        # keeps hitting until soft 17
        # Recalculate dealer hand
        dealer_values = [card_Values[card[1:2]] for card in dealer_hand]  # gets corresponding value for each card
        normalized_dlist = [
            card if isinstance(card, list) else [card, card]
            for card in dealer_values
        ]  # makes it so if there's ace, have a hard and soft value
        sumdhand = [sum(value) for value in zip(*normalized_dlist)]  # sums up the hard and soft values
        # dealer hits until soft 17
        if sumdhand[0] > 21:
            # dealer busts
            hand_finished = 1
        elif sumdhand[0] < 17 and sumdhand[1] < 17:
            # continue hitting
            dealer_hand.append(shoe[shoe_index])
            shoe_index += 1


def printAdjustWinner():
    global sumphand
    global sumdhand
    global bet
    global sum_player_hand

    if sumdhand[0] > 21 or sumphand[0] > sumdhand[1]:
        # dealer busts or player higher value than dealer
        print('---------------------Player Wins---------------------')
        printUpdatedBalance(bet * (1))
    elif sum_player_hand[1] > 21 or sumdhand[0] > sumphand[0]:
        # over 21
        print('---------------------Player Lost---------------------')
        printUpdatedBalance(bet * (-1))
    elif sumdhand[0] == sumphand[0]:
        # push tie
        print('---------------------PUSH---------------------')
    else:
        print('error no option logic for finding winner')


card_Values = {
    '1': 10,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': [11, 1]
}

# Change these for how the game should work
num_decks = 6
max_hands = 4
num_hands_to_play = 30000

# Variables for initializing
hands = 0  # index to point at how many hands of black jack were played
stopIndex = createStop(num_decks)
balance = 100
bet = 1
dealer_hand = []
player_hand = []
shoe = createShoe(num_decks)

while hands < num_hands_to_play:
    shoe_index = 0  # index to point at which card in the list of shoe

    while shoe_index < stopIndex:
        # until the cards hit the end of the stop part of the shoe
        if hands == num_hands_to_play:
            print('Max amount of hands to be played')
            break

        while hands < num_hands_to_play:
            # While game is going on

            dealer_hand.clear()
            player_hand.clear()
            # deals out 4 cards
            dealer_hand = [shoe[shoe_index + 1], shoe[shoe_index + 3]]
            player_hand = [[shoe[shoe_index], shoe[shoe_index + 2]]]
            shoe_index += 4

            # For testing
            # player_hand = [['[K♣]', '[A♠]']]
            # For testing

            # Calculates dealer cards values
            dealer_values = [card_Values[card[1:2]] for card in dealer_hand]  # gets corresponding value for each card
            normalized_dlist = [
                card if isinstance(card, list) else [card, card]
                for card in dealer_values
            ]  # makes it so if there's ace, have a hard and soft value
            sumdhand = [sum(value) for value in zip(*normalized_dlist)]  # sums up the hard and soft values
            # Calculates player cards values
            player_values = [card_Values[card[1:2]] for card in
                             player_hand[0]]  # gets corresponding value for each card
            normalized_plist = [
                card if isinstance(card, list) else [card, card]
                for card in player_values
            ]  # makes it so if there's ace, have a hard and soft value
            sumphand = [sum(value) for value in zip(*normalized_plist)]  # sums up the hard and soft values

            # Print inital hands
            if dealer_hand[0][1:2] != 'A':
                # When dealer not showing ace
                print(f'Dealer: {dealer_hand[0]} \t \t \t ({dealer_values[0]})')
            else:
                # When dealer shows an ace
                print(f'Dealer: {dealer_hand[0]} \t \t \t (11/1)')
            if sumphand[0] == sumphand[1]:
                # When there is no ace
                print(f'Player: {player_hand[0][0]} {player_hand[0][1]} \t \t ({sumphand[0]})')
            elif sumphand[0] == 21:
                # Player Blackjack
                print(f'Player: {player_hand[0][0]} {player_hand[0][1]} \t \t BLACKJACK!')
            elif sumphand[0] <= 21:
                # Player has at least one ace
                print(f'Player: {player_hand[0][0]} {player_hand[0][1]} \t \t ({sumphand[0]})/({sumphand[1]})')
            elif sumphand[0] > 21:
                # Player has at 2 aces
                print(f'Player: {player_hand[0][0]} {player_hand[0][1]} \t \t ({sumphand[1]})')
            else:
                print('ERROR CHECK')

            if sumphand[0] == 21 and sumdhand[0] == 21:
                # Checks if dealer has blackjack
                print(f'\nDealer Reveal: {dealer_hand[0]} {dealer_hand[1]} \t PUSH!')
                printUpdatedBalance(bet * 0)
                break
            elif sumdhand[0] != 21 and sumphand[0] == 21:
                # Player Win
                print(f'\nDealer Reveal: {dealer_hand[0]} {dealer_hand[1]} \t Player WIN!')
                printUpdatedBalance(bet * (3 / 2))
                break
            elif sumdhand[0] == 21 and sumphand[0] != 21:
                # Player Win
                print(f'\nDealer Reveal: {dealer_hand[0]} {dealer_hand[1]} \t LOSE!')
                printUpdatedBalance(-1)
                break

            p_actions = ['stand', 'hit']  # possible player actions

            # if double is allowed

            # if len(player_hand) > 1:
            #    if player_hand[-2][0][1:2] != 'A' and player_hand[-2][1][1:2] != 'A':
            # makes sure the last hand was not an ace split
            #        p_actions.append('double')
            # else:
            #    p_actions.append('double')

            # if dealer is showing Ace
            if dealer_hand[0][1:2] == 'A':
                # Dealer shows ace (Insurance)
                p_actions.append('insurance')

            if player_hand[0][0] == player_hand[0][1]:
                # allows first split
                p_actions.append('split')

            hand_finished = 0  # 0 if still doing player inputs, 1 if hand done
            hand_index = 0  # 0 is first index, depending on how many split which current hand
            p_inputs = ''

            # logic to play hand and get user inpupt
            while hand_index < len(player_hand):
                # For each hand (that is split)
                while hand_finished == 0:
                    # for each hand that is unfinished keep playing (hitting/etc.)
                    p_actions = ['stand', 'hit']

                    if len(player_hand) > 1:
                        # add double option if just dealt hand
                        if player_hand[-2][0][1:2] != 'A' and player_hand[-2][1][1:2] != 'A':
                            # makes sure the last hand was not an ace split
                            p_actions.append('double')
                    else:
                        # if first hand (no split)
                        if len(player_hand[hand_index]) == 2:
                            p_actions.append('double')

                    if dealer_hand[0][1:2] == 'A':
                        # add insurance option after just dealt hand
                        p_actions.append('insurance')

                    if player_hand[0][0] == player_hand[0][1]:
                        # add split option
                        print('-----')

                    # recalculate player hand values
                    player_values = [card_Values[card[1:2]] for card in
                                     player_hand[0]]  # gets corresponding value for each card
                    normalized_plist = [
                        card if isinstance(card, list) else [card, card]
                        for card in player_values
                    ]  # makes it so if there's ace, have a hard and soft value
                    sumphand = [sum(value) for value in zip(*normalized_plist)]  # sums up the hard and soft values

                    p_inputs = input(f'Possible Actions: {p_actions}\n')
                    if p_inputs == 'stand' and 'stand' in p_actions:
                        # player decides to stand
                        # Check for Win
                        checkForWin()
                        hand_finished = 1
                        printHands()
                        if sumphand[0] > sumdhand[0]:
                            # player wins
                            print('---------------------Player Won---------------------')
                            printUpdatedBalance(bet)
                        elif sumphand[0] < sumdhand[0]:
                            # player loses
                            print('---------------------Player Lost---------------------')
                            printUpdatedBalance(bet * (-1))
                        else:
                            # player ties
                            print('---------------------PUSH---------------------')
                    elif p_inputs == 'hit' and 'hit' in p_actions:
                        # player decides to hit
                        player_hand[hand_index].append(shoe[shoe_index])
                        shoe_index += 1
                        # Check if player goes over 21
                        sum_player_hand = checkPlayerHandSum(hand_index)
                        printHands()
                        if sum_player_hand[1] > 21:
                            # over 21
                            print('---------------------Player Lost---------------------')
                            printUpdatedBalance(bet * (-1))
                            hand_finished = 1
                    elif p_inputs == 'double' and 'double' in p_actions:
                        # player decides to double

                        print('Player Doubles')
                        player_hand[hand_index].append(shoe[shoe_index])
                        shoe_index += 1
                        # Check if player goes over 21
                        sum_player_hand = checkPlayerHandSum(hand_index)

                        printHands()
                        if sum_player_hand[1] > 21:
                            # over 21
                            printUpdatedBalance(bet * (-2))
                            printHands()
                            print('---------------------Player Lost---------------------')
                        hand_finished = 1
                    elif p_inputs == 'split' and 'split' in p_actions:

                        print('Player Splits')

                        printHands()
                    else:
                        # player types something wrong in
                        print('\nPlease enter a valid input')

                print(f'\nbalance: {balance}\n')
                hand_index += 1  # finishes logic for hand

            print('')
            hands += 1  # start increment of hands played

    print(f'Hands Played {hands}')
    if hands < num_hands_to_play:
        print('Reshuffling Shoe\n')