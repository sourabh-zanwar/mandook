def rank_hand(cards):   
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
    return (number, suit_mappings[suit], f'{suit} {number}')


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
player1 = [(1, 'Hearts')]
player2 = [(1, 'Clubs')]


result = compare_hands(player1, player2)
print(result)  # This will print "Player 2 wins"