# -*- coding: utf-8 -*-


import random
import string
from itertools import chain
import copy
import os
import json

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string



##################

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
        info_dict = {
            'id': self.id,
            'amount': self.balance,
            'cards': self.cards_in_hand,
            'current_status': self.status,
            'mandook': self.mandook
            }
        with open('./cards_store/'+self.session+'/{self.id}.json', 'w') as fp:
            json.dump(info_dict, fp)
        
    


class CompareCards():
    def __init__(self):
        self.single_suit_mappings = {
            'Spades':4,
            'Hearts':3,
            'Diamonds':2,
            'Clubs':1
            }
        
    def rank_hand_single(self, player):   
        cards = player.get_cards()
        suit = cards[0][1]
        number = cards[0][0]
        if number == 1:
            number = 14
        
        player.set_score((number, self.single_suit_mappings[suit]))
    
    def rank_hand_three(self, player, curr_round=3):   
        if curr_round == 2:
            cards = player.get_temp_cards()
        elif curr_round == 4:
            cards = player.get_temp_cards()
        else:
            cards = player.get_cards()
        
        # Sort the cards by rank and suit
        cards.sort(key=lambda card: (card[0], card[1]))
        
        #print(cards)
        hand_score = None

        # Check for a Trail
        if cards[0][0] == cards[1][0] == cards[2][0]:
            hand_score =  (6, cards[2][0], 'Trail', cards[2][1], cards[2][2])  # 6 represents Trail, and cards[2][0] is the rank of the Trail

        # Check for a Pure Sequence  
        elif cards[0][0] + 1 == cards[1][0] and cards[1][0] + 1 == cards[2][0] and cards[0][1] == cards[1][1] == cards[2][1]:
            if cards[0][0] == 1 and cards[1][0] == 2:
                hand_score =  (5, 15, 'Pure Sequence with Ace low', cards[2][1], cards[2][2])
            else:
                hand_score =  (5, cards[2][0], 'Pure Sequence', cards[2][1], cards[2][2])
        # Check for Pure sequence with Q-K-A
        elif cards[0][0] == 1 and cards[1][0] == 12 and cards[2][0] == 13 and cards[0][1] == cards[1][1] == cards[2][1]:
            hand_score =  (5, 14, 'Pure Sequence with Ace High', cards[2][1], cards[2][2])

        # Check for a Impure Sequence  
        elif cards[0][0] + 1 == cards[1][0] and cards[1][0] + 1 == cards[2][0]:
            if cards[0][0] == 1 and cards[1][0] == 2:
                hand_score =  (4, 15, cards[2][1], 'Impure Sequence with Ace low', cards[2][1], cards[2][2])
            else:
                hand_score =  (4, cards[2][0], 'Impure Sequence', cards[2][1], cards[2][2])
        # Check for impure sequence with Q-K-A
        elif cards[0][0] == 1 and cards[1][0] == 12 and cards[2][0] == 13:
            hand_score =  (4, 14, 'Impure Sequence with Ace High', cards[2][1], cards[2][2])

        # Check for a Color (all cards of the same suit)
        elif cards[0][1] == cards[1][1] == cards[2][1]:
            hand_score =  (3, cards[2][0], 'Color', cards[2][1], cards[2][2])  # 3 represents Color, and cards[2][0] is the highest rank

        # Check for a Pair
        elif cards[0][0] == cards[1][0] or cards[1][0] == cards[2][0]:
            hand_score =  (2, cards[1][0], 'Pair', cards[2],[1], cards[2][2])  # 2 represents Pair, and cards[1][0] is the rank of the Pair

        # High Card    
        else:
            hand_score =  (1, cards[2][0], 'High Card', cards[2][1], cards[2][2])  # 1 represents High Card, and cards[2][0] is the highest rank
        
        # CHeck if 'Ace' is in the cards
        if hand_score[1] == 1:
            hand_score = (hand_score[0],14, hand_score[-1], cards[2][1], cards[2][2])
        
        player.set_score(hand_score)   
        
    def find_pairs_with_differences(self,cards):
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

    def rank_hand_five(self, player):
        cards = [x[0] for x in player.get_cards()]
                
        if 14 in cards:
            cards2 = []
            for card in cards:
                if card==14:
                    cards2.append(1)
                else:
                    cards2.append(card)
                    
            run_jump_1 = self.find_pairs_with_differences(cards)
            run_jump_2 = self.find_pairs_with_differences(cards2)
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
            run_jump = self.find_pairs_with_differences(cards)
            
        if run_jump[-1] == 1:
            return (run_jump[0][0], 0, f'Trail of {run_jump[0][0]}')
        else:
            return (0,0,'No Run Jump')
    
    def rank_players(self, players, n_round, mufflies=False):
        player_dictionary = {}
        player_scores = []
        for player in players:
            key = tuple(list(player.get_score()) + [player.id])
            player_dictionary[key] = player
            player_scores.append(key)
        player_scores = sorted(player_scores, key=lambda x: (x[0], x[1], x[3], x[4]), reverse=not mufflies)
        
        rank = 1
        initialised = False
        for i in range(len(player_scores)):
            if initialised == True:
                if round != 2 and round !=2 and round!=3:
                    if player_scores[i][0]==player_scores[i-1][0] and player_scores[i][1]==player_scores[i-1][1]:
                        player_dictionary[player_scores[i]].set_rank(rank)
                    else:
                        rank = rank + 1
                        player_dictionary[player_scores[i]].set_rank(rank)
                else:
                    if player_scores[i][0]==player_scores[i-1][0] and player_scores[i][1]==player_scores[i-1][1] and player_scores[i][3]==player_scores[i-1][3] and player_scores[i][4]==player_scores[i-1][4]:
                        player_dictionary[player_scores[i]].set_rank(rank)
                    else:
                        rank = rank + 1
                        player_dictionary[player_scores[i]].set_rank(rank)
            else:
                player_dictionary[player_scores[i]].set_rank(rank)
                initialised = True

##################


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
            
        

plaay = GamePlay(3)
plaay.play()
