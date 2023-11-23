def rank_hand(cards):   
    
    # cards = [x.replace('A','1').replace('J','11').replace('Q','12').replace('K','13') for x in cards]

    # cards = [(int(x[:-1]),str(x[-1])) for x in cards]
    
    # Sort the cards by rank and suit
    cards.sort(key=lambda card: (card[0], card[1]))
    
    #print(cards)
    hand_score = None

    # Check for a Trail
    if cards[0][0] == cards[1][0] == cards[2][0]:
        hand_score =  (6, cards[2][0], 'Trail')  # 6 represents Trail, and cards[2][0] is the rank of the Trail

    # Check for a Pure Sequence  
    elif cards[0][0] + 1 == cards[1][0] and cards[1][0] + 1 == cards[2][0] and cards[0][1] == cards[1][1] == cards[2][1]:
        if cards[0][0] == 1 and cards[1][0] == 2:
            hand_score =  (5, 15, 'Pure Sequence with Ace low')
        else:
            hand_score =  (5, cards[2][0], 'Pure Sequence')
    # Check for Pure sequence with Q-K-A
    elif cards[0][0] == 1 and cards[1][0] == 12 and cards[2][0] == 13 and cards[0][1] == cards[1][1] == cards[2][1]:
        hand_score =  (5, 14, 'Pure Sequence with Ace High')

    # Check for a Impure Sequence  
    elif cards[0][0] + 1 == cards[1][0] and cards[1][0] + 1 == cards[2][0]:
        if cards[0][0] == 1 and cards[1][0] == 2:
            hand_score =  (4, 15, cards[2][1], 'Impure Sequence with Ace low')
        else:
            hand_score =  (4, cards[2][0], 'Impure Sequence')
    # Check for impure sequence with Q-K-A
    elif cards[0][0] == 1 and cards[1][0] == 12 and cards[2][0] == 13:
        hand_score =  (4, 14, 'Impure Sequence with Ace High')

    # Check for a Color (all cards of the same suit)
    elif cards[0][1] == cards[1][1] == cards[2][1]:
        hand_score =  (3, cards[2][0], 'Color')  # 3 represents Color, and cards[2][0] is the highest rank

    # Check for a Pair
    elif cards[0][0] == cards[1][0] or cards[1][0] == cards[2][0]:
        hand_score =  (2, cards[1][0], 'Pair')  # 2 represents Pair, and cards[1][0] is the rank of the Pair

    # High Card    
    else:
        hand_score =  (1, cards[2][0], 'High Card')  # 1 represents High Card, and cards[2][0] is the highest rank
    
    # CHeck if 'Ace' is in the cards
    if hand_score[1] == 1:
        hand_score = tuple([hand_score[0],14,hand_score[2]])
    
    return hand_score




def compare_hands(player1, player2):
    rank1, rank2 = rank_hand(player1), rank_hand(player2)
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


# Example usage:
player1 = [(1, 'Hearts'), (1, 'Spades'), (13, 'Diamonds')]
player2 = [(1, 'Hearts'), (1, 'Spades'), (13, 'Diamonds')]


result = compare_hands(player1, player2)
print(result)  # This will print "Player 2 wins"
