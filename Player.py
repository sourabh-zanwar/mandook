# -*- coding: utf-8 -*-

from util.utils import generate_random_string
import json

class Player():
    '''
    Attributes required:
        Cards in hand
        unique ID
        balance
    
    Methods required:
        get_cards
        set_cards
        get_balance
        set_balance
        set_status
        get_status
    
    Temp_variables
        in/out
        current_rank
        current_score
        temporary cards
        round_6_cards

    '''
    def __init__(self, session_id):
        self.id = generate_random_string(16)
        self.balance = 20
        self.cards_in_hand = []
        self.curr_score = ()
        self.curr_rank = 0
        self.temp_cards = []
        self.status = 0
        self.mandook = 0
        self.round_6_cards = {}
        self.session_id = session_id
        self.info_dict = {}
        
    def get_cards(self):
        return self.cards_in_hand
    
    def set_card(self, new_card):
        self.cards_in_hand.append(new_card)
        
    def reset_card(self):
        self.cards_in_hand = []
    
    def get_balance(self):
        return self.balance
    
    def set_balance(self, change):
        self.balance += change
    
    def get_rank(self):
        return self.rank
    
    def set_rank(self, rank):
        self.rank = rank
    
    def get_score(self):
        return self.score
    
    def set_score(self, new_score):
        self.score = new_score
        
    def set_add_temp_card(self, card_to_add):
        self.temp_cards = self.cards_in_hand + [card_to_add]
    
    def set_remove_temp_card(self, card_to_remove):
        self.temp_cards = [x for x in self.cards_in_hand if x != card_to_remove]
        
    def get_temp_cards(self):
        return self.temp_cards
    
    def get_status(self):
        return self.status
    
    def set_status(self):
        self.status = 1
    
    def reset_status(self):
        self.status = 0
        
    def get_mandook(self):
        return self.mandook
    
    def set_mandook(self):
        self.mandook += 1
    
    def set_sixth_round_cards(self, single_card, double_card, triple_card):
        self.round_6_cards = {
            'single': single_card,
            'double': double_card,
            'triple': triple_card
            }
        
    def get_sixth_round_cards(self):
        return self.round_6_cards
    
    def store_details(self):
        self.info_dict = {
            'id': self.id,
            'amount': self.balance,
            'cards': self.cards_in_hand,
            'current_status': self.status,
            'mandook': self.mandook
            }
        with open('./card_store/' + self.session_id +'/' + self.id + '.json', 'w') as fp:
            json.dump(self.info_dict, fp)
        
    
