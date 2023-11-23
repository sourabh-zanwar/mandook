# -*- coding: utf-8 -*-

import random

class Cards():
    '''
    For shuffling and disctribution of cards
    '''
    def __init__(self):
        self.__cards = self.shuffle()
        
    def distribute_card(self,players):
        for player in players:
            player.set_card(self.__cards.pop(0))
            player.store_details()
            
    def shuffle(self):
        card_face = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        card_numbers = [x for x in range(1,14)]
        cards = []
        for face in card_face:
            for number in card_numbers:
                #cards.append(number + ' ' + face)
                cards.append((number,face))
        random.shuffle(cards)
        return cards