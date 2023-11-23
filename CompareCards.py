from itertools import chain


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
