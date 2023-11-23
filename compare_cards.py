#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 20:02:11 2023

@author: sourabhzanwar
"""

def rank_hand_single(cards, player_id):   
    suit = cards[0][1]
    number = cards[0][0]
    if number == 1:
        number = 14
    suit_mappings = {
        'Spades':4,
        'Hearts':3,
        'Diamonds':2,
        'Clubs':1
        }
    return (number, suit_mappings[suit], player_id, f'{suit} {number}')


def rank_hand_three(cards, player_id):   
    
    # cards = [x.replace('A','1').replace('J','11').replace('Q','12').replace('K','13') for x in cards]

    # cards = [(int(x[:-1]),str(x[-1])) for x in cards]
    
    # Sort the cards by rank and suit
    cards.sort(key=lambda card: (card[0], card[1]))
    
    #print(cards)
    hand_score = None

    # Check for a Trail
    if cards[0][0] == cards[1][0] == cards[2][0]:
        hand_score =  (6, cards[2][0], player_id, 'Trail')  # 6 represents Trail, and cards[2][0] is the rank of the Trail

    # Check for a Pure Sequence  
    elif cards[0][0] + 1 == cards[1][0] and cards[1][0] + 1 == cards[2][0] and cards[0][1] == cards[1][1] == cards[2][1]:
        if cards[0][0] == 1 and cards[1][0] == 2:
            hand_score =  (5, 15, player_id, 'Pure Sequence with Ace low')
        else:
            hand_score =  (5, cards[2][0], player_id, 'Pure Sequence')
    # Check for Pure sequence with Q-K-A
    elif cards[0][0] == 1 and cards[1][0] == 12 and cards[2][0] == 13 and cards[0][1] == cards[1][1] == cards[2][1]:
        hand_score =  (5, 14, player_id, 'Pure Sequence with Ace High')

    # Check for a Impure Sequence  
    elif cards[0][0] + 1 == cards[1][0] and cards[1][0] + 1 == cards[2][0]:
        if cards[0][0] == 1 and cards[1][0] == 2:
            hand_score =  (4, 15, cards[2][1], player_id, 'Impure Sequence with Ace low')
        else:
            hand_score =  (4, cards[2][0], player_id, 'Impure Sequence')
    # Check for impure sequence with Q-K-A
    elif cards[0][0] == 1 and cards[1][0] == 12 and cards[2][0] == 13:
        hand_score =  (4, 14, player_id, 'Impure Sequence with Ace High')

    # Check for a Color (all cards of the same suit)
    elif cards[0][1] == cards[1][1] == cards[2][1]:
        hand_score =  (3, cards[2][0], player_id, 'Color')  # 3 represents Color, and cards[2][0] is the highest rank

    # Check for a Pair
    elif cards[0][0] == cards[1][0] or cards[1][0] == cards[2][0]:
        hand_score =  (2, cards[1][0], player_id, 'Pair')  # 2 represents Pair, and cards[1][0] is the rank of the Pair

    # High Card    
    else:
        hand_score =  (1, cards[2][0], player_id, 'High Card')  # 1 represents High Card, and cards[2][0] is the highest rank
    
    # CHeck if 'Ace' is in the cards
    if hand_score[1] == 1:
        hand_score = tuple([hand_score[0],14, player_id, hand_score[-1]])
    
    return hand_score


def compare_hands(player1, player2, num_cards_in_hand):
    if num_cards_in_hand+1 == 1:
        rank1, rank2 = rank_hand_single(player1), rank_hand_single(player2)
    else:
        rank1, rank2 = rank_hand_three(player1), rank_hand_three(player2)
    #print(f'Player 1 ranks {rank1[0]}, {rank1[1]}, {rank1[-1]}')
    #print(f'Player 2 ranks {rank2[0]}, {rank2[1]}, {rank2[-1]}')

    # Compare the ranks first
    if rank1[0] > rank2[0]:
        return "Player 1 wins"
    elif rank1[0] < rank2[0]:
        return "Player 2 wins"
    else:
        # If ranks are the same, compare the highest ranks, then the highest suits
        if rank1[1] > rank2[1]:
            return "Player 1 wins"
        elif rank1[1] < rank2[1]:
            return "Player 2 wins"
        else:
            # if rank1[2] > rank2[2]:
            #     return "Player 1 wins"
            # elif rank1[2] < rank2[2]:
            #     return "Player 2 wins"
            # else:
            #     return "It's a tie"
            return "It's a tie"
        

def compare_all_hands(cards_in_hand, num_cards_in_hand):
    scores = list()
    for player,cards in cards_in_hand.items():
        if num_cards_in_hand == 1:
            scores.append(rank_hand_single(cards, player))
        else:
            scores.append(rank_hand_three(cards, player))
    scores = sorted(scores, key=lambda x: (x[0], x[1]))
    return scores



from itertools import chain

def find_pairs_with_differences(cards):
    cards.sort()
    result_pairs = []
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            if abs(cards[i] - cards[j]) == 2:
                for k in range(len(cards)):
                    for l in range(k + 1, len(cards)):
                        if abs(cards[k] - cards[l]) == 1 and (cards[i], cards[j]) != (cards[k], cards[l]) and i != k and i != l and j != k and j != l:
                            pair1 = (cards[i], cards[j])
                            pair2 = (cards[k], cards[l])
                            result_pairs.append((pair1, pair2))

    # Filter out pairs where the remaining integer is smaller
    filtered_pairs = [pairs for pairs in result_pairs if min(pairs[0] + pairs[1]) == min(cards)]
    
    if filtered_pairs:
        filtered_pairs = list(chain(*filtered_pairs[0]))
        return ([x for x in cards if x not in filtered_pairs] + filtered_pairs,1)
    else:
        return (cards, 0)

def compare_hand_five(cards):
    cards = [x[0] for x in cards]
    cards2 = []
    for card in cards:
        if card==14:
            cards2.append(1)
        else:
            cards2.append(card)
            
    if 14 in cards:
        run_jump_1 = find_pairs_with_differences(cards)
        run_jump_2 = find_pairs_with_differences(cards2)
        if run_jump_1[-1] == 1 and run_jump_2[-1] != 1:
            run_jump = run_jump_1
        elif run_jump_1[-1] != 1 and run_jump_2[-1] == 1:
            run_jump = run_jump_2
        elif run_jump_1[-1] == 1 and run_jump_2[-1] == 1:
            if run_jump_1[0][0] > run_jump_2[0][0]:
                run_jump = run_jump_1
            elif run_jump_1[0][0] < run_jump_2[0][0]:
                run_jump = run_jump_2
            else:
                run_jump = run_jump_1
    else:
        run_jump = find_pairs_with_differences(cards)
        
    if run_jump[-1] == 1:
        return (run_jump[0][0], 0, f'Trail of {run_jump[0][0]}')
    else:
        return (0,0,'No Run Jump')
    
compare_hand_five()