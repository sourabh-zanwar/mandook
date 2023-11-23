#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 15:31:09 2022

@author: sourabhzanwar
"""
import random
import numpy as np
from compare_cards import compare_all_hands


card_face = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
card_numbers = [x for x in range(2,14)]

n_players = int(input('Enter number of players: '))
mandook_count = dict([(x+1,0) for x in range(int(n_players))])

mandook_count = [0 for x in range(int(n_players))]

amount_in_hand = [20 for x in range(int(n_players))]


table = n_players

while 5 not in mandook_count:
    
    print("New round")
    
    cards = []
    for face in card_face:
        for number in card_numbers:
            #cards.append(number + ' ' + face)
            cards.append((number,face))
            
    random.shuffle(cards)

    cards_in_hand = dict([(x+1,[]) for x in range(int(n_players))])
        
    
    for i in range(6):
        if 5 in mandook_count:
            break
        else:
            for player,dist_cards in cards_in_hand.items():
                dist_cards.append(cards.pop(0))
            curr_in = []
            scores = compare_all_hands(cards_in_hand, i+1)
            for pl in range(n_players):
                curr_in.append(int(input(f"Player {pl+1} (0: out; 1:in): ")))
                
            if sum(curr_in) == 1:
                mandook_count[curr_in.index(1)] = mandook_count[curr_in.index(1)] + 1
            
            else:
                # compare cards
                compare_hands(cards_in_hand, i)
            
    table = table + n_players
            
            
print("\n#################################################\n")
print(f"Player {mandook_count.index(5)+1} wins mandook!")
print("\n#################################################")


def custom_sort(input_list):
    # Sort based on the first element of the tuple, then the second element
    sorted_list = sorted(input_list, key=lambda x: (x[0], x[1]))
    return sorted_list

# Example usage:
my_list = [(3, 1,'abcg'), (1, 2,'absd3cg'), (2, 2,'abcgi7zgzbjhwc'), (3, 0,'abcg8uhibjh'), (1, 1,'abcg4e')]
result = custom_sort(my_list)
print(result)