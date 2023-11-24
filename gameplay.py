# -*- coding: utf-8 -*-

import os

from Player import Player
from Cards import Cards
from CompareCards import CompareCards

from util.utils import generate_random_string

class GamePlay():
    def __init__(self, number_of_players):
        self.session_id = generate_random_string(10)
        os.makedirs('./card_store/'+ self.session_id)
        self.comparison = CompareCards()
        self.players = [Player(self.session_id) for x in range(number_of_players)]
        self.cards = Cards()
    
    def get_player_status(self):
        for player in self.players:
            status = int(input(f'Player {player.id}\nPlease enter in(1) or out(0): '))
            if status == 1:
                player.set_status()
        print("========================\nPlayers Status\n========================")
        print("Player ID\tPlayer Status\tPlayer Amount")
        for player in self.players:
            player.store_details()
            print(player.id+'\t'+str(player.get_status())+'\t'+str(player.get_balance()))
    
    def play_round(self,mufflies=False):
        in_players = [x for x in self.players if x.get_status()]
        self.comparison.rank_players(in_players)
        rank_dictionary = {}
        for player in in_players:
            player.store_details()
            rank = player.get_rank()
            if rank in rank_dictionary.keys():
                v = rank_dictionary[rank] + [player]
                rank_dictionary[rank] = v
            else:
                rank_dictionary[rank] = [player]
        if mufflies:
            min_rank = min(rank_dictionary.keys())
            if len(rank_dictionary[min_rank])>1:
                print("It's a tie!\n")
            else:
                print(f'{rank_dictionary[min_rank][0].id} wins with {str(rank_dictionary[min_rank][0].get_cards())}')
        else:
            max_rank = max(rank_dictionary.keys())
            if len(rank_dictionary[max_rank])>1:
                print("It's a tie!\n")
            else:
                print(f'{rank_dictionary[max_rank][0].id} wins with {str(rank_dictionary[max_rank][0].get_cards())}')
    
    def play(self):
        
        while 5 not in [x.get_mandook() for x in self.players]:
            self.cards.shuffle()
            for i in range(6):
                self.cards.distribute_card(self.players)
                
                self.get_player_status()
                if i == 0:
                    self.round_1()
                elif i == 1:
                    self.round_2()
                elif i == 2:
                    self.round_3()
                elif i == 3:
                    self.round_4()
                elif i == 4:
                    self.round_5()
                elif i == 5:
                    self.round_6()
            
                self.comparison.rank_players(self.players, n_round=i)
                if i == 0 or i == 2:
                    muff = True
                else:
                    muff = False
                self.play_round(muff)
    
    def round_1(self):
        for player in self.players:
            self.comparison.rank_hand_single(player)
    
    def round_2(self):
        for player in self.players:
            suit = int(input('Choose the Suit you want your third card to be:\n1. Spades\n2.Hearts\n3.Diamonds\n4. Clubs\n'))
            
            if suit == 1:
                suit = 'Spades'
            elif suit == 2:
                suit = 'Hearts'
            elif suit == 3:
                suit = 'Diamonds'
            elif suit == 4:
                suit = 'Clubs'
                
            number = int(input('Enter the number of card you want: '))
            added_card = (number,suit)
            player.set_add_temp_card(added_card)
            self.comparison.rank_hand_three(player, curr_round=2)
    
    def round_3(self):
        for player in self.players:
            self.comparison.rank_hand_three(player)
            
    def round_4(self):
        for player in self.players:
            print(f'Player {player.id} select the card you want to discard:')
            cards = player.get_cards()
            for i in range(len(cards)):
                print(f'{i+1}. {cards[i]}')
            discard = int(input('Select the card to discard'))
            discarded_card = cards[discard-1]
            player.set_remove_temp_card(discarded_card)
            self.comparison.rank_hand_three(player, curr_round=4)
    
    def round_5(self):
        for player in self.players:
            self.comparison.rank_hand_five(player)
    
    def round_6(self):
        for player in self.players:
            cards = player.get_cards()
            print('Select the cards you want to choose for three cards in round 6')
            for i in range(cards):
                print(f'{i+1}. {cards[i]}')
            triple_cards = []
            for i in range(3):
                add_card = int(input('Select card no. {i+1}: '))
                triple_cards.append(cards[add_card-1])
            cards = [x for x in cards if x not in triple_cards]
            print('Select the cards you want to choose for two cards in round 6')
            for i in range(cards):
                print(f'{i+1}. {cards[i]}')
            double_cards = []
            for i in range(2):
                add_card = int(input('Select card no. {i+1}: '))
                triple_cards.append(cards[add_card-1])
            cards = [x for x in cards if x not in double_cards]
            player.set_sixth_round_cards(cards, double_cards, triple_cards)
            ### Next compare for 6 hand cards
            
