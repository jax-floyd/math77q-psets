'''
    #1
'''
import random

def shoe(n_decks = 1): # <-- Standard deck
    suits = ['S', 'H', 'D', 'C']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(rank, suit) for rank in ranks for suit in suits for i in range(n_decks)]

def shuffle(deck):
    random.shuffle(deck)
    return deck

def sum_cards(hand): # <-- Sums cards in a hand according to baccarat paradigm

    sum = 0
    baccarat_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 0, 'J': 0, 'Q': 0, 'K': 0, 'A': 1}
    for card in hand:
        value = baccarat_values[card[0]]
        sum += value
        
    if sum > 9:
        sum = str(sum)
        sum = sum[-1]
        sum = int(sum)

    return sum

def does_player_draw(player_hand, banker_hand):

    player_value = sum_cards(player_hand)
    banker_value = sum_cards(banker_hand)
    
    # If either the player or the banker has a natural (8 or 9), the game ends and the player cannot draw
    if player_value == 8 or player_value == 9 or banker_value == 8 or banker_value == 9:
        return False
    # If the player's hand is 0-5, they must draw a third card
    if 0 <= player_value <= 5:
        return True
    # If the player's hand is 6 or 7, they must stand
    if 6 <= player_value <= 7:
        return False

def does_banker_draw(player_hand, banker_hand):
    
    player_value = sum_cards(player_hand)
    banker_value = sum_cards(banker_hand)
    
    # If either the player or the banker has a natural (8 or 9), the game ends and the banker cannot draw
    if player_value == 8 or player_value == 9 or banker_value == 8 or banker_value == 9:
        return False
    
    # If the player has not drawn a third card, the rules for whether the banker should draw are different
    if len(player_hand) == 2:
        # If the banker's hand is 0-5, they must draw a third card
        if 0 <= banker_value <= 5:
            return True
        # If the banker's hand is 6 or 7, they must stand
        elif 6 <= banker_value <= 7:
            return False
    
    # If the player has drawn a third card, the rules for whether the banker should draw are as follows:
    elif len(player_hand) == 3:
        # If the banker's hand is 3, they must draw if the player's third card was anything other than an 8
        if banker_value in [0, 1, 2, 3]:
            if player_hand[-1][0] != '8':
                return True
            else:
                return False
        # If the banker's hand is 4, they must draw if the player's third card was a 2, 3, 4, 5, 6, or 7
        if banker_value == 4:
            if player_hand[-1][0] in ['2', '3', '4', '5', '6', '7']:
                return True
            else:
                return False
        # If the banker's hand is 5, they must draw if the player's third card was a 4, 5, 6, or 7
        if banker_value == 5:
            if player_hand[-1][0] in ['4', '5', '6', '7']:
                return True
            else:
                return False
        # If the banker's hand is 6, they must draw if the player's third card was a 6 or 7
        if banker_value == 6:
            if player_hand[-1][0] in ['6', '7']:
                return True
            else:
                return False
        # If the banker's hand is 7, they must stand
        if banker_value == 7:
            return False

def play_baccarat_hand(n_decks = 8): # <-- Plays 1 hand of standard 8 deck baccarat

    game = {'player_hand': None, 'player_deal_sum': None,'player_draw_sum': None, 'banker_hand': None, 'banker_deal_sum': None, 'banker_draw_sum': None, 'outcome': None}

    baccarat_shoe = shuffle(shoe(n_decks))

    game['player_hand'] = [baccarat_shoe.pop() for i in range(2)] # <-- Player dealt first
    game['banker_hand'] = [baccarat_shoe.pop() for i in range(2)]
    game['player_deal_sum'] = sum_cards(game['player_hand'])
    game['banker_deal_sum'] = sum_cards(game['banker_hand'])
    
    # Decide drawing
    if does_player_draw(game['player_hand'], game['banker_hand']): # Either player draws
        game['player_hand'].append(baccarat_shoe.pop())
        game['player_draw_sum'] = sum_cards(game['player_hand'])

    if does_banker_draw(game['player_hand'], game['banker_hand']):
        game['banker_hand'].append(baccarat_shoe.pop())
        game['banker_draw_sum'] = sum_cards(game['banker_hand'])

    return game

def evaluate_game(game):
    
    if game['player_draw_sum'] == None and game['banker_draw_sum'] == None: # <-- Natural occurred before player could draw or dealer could draw
        if game['player_deal_sum'] > game['banker_deal_sum']:
            game['outcome'] = 'P'
        elif game['player_deal_sum'] < game['banker_deal_sum']:
            game['outcome'] = 'B'
        elif game['player_deal_sum'] == game['banker_deal_sum']:
            game['outcome'] = 'T'
        
    elif game['player_draw_sum'] == None and game['banker_draw_sum'] != None:
        if game['player_deal_sum'] > game['banker_draw_sum']:
            game['outcome'] = 'P'
        elif game['player_deal_sum'] < game['banker_draw_sum']:
            game['outcome'] = 'B'
        elif game['player_deal_sum'] == game['banker_draw_sum']:
            game['outcome'] = 'T'
        
        
    elif game['player_draw_sum'] != None and game['banker_draw_sum'] == None:
        if game['player_draw_sum'] > game['banker_deal_sum']:
            game['outcome'] = 'P'
        elif game['player_draw_sum'] < game['banker_deal_sum']:
            game['outcome'] = 'B'
        elif game['player_draw_sum'] == game['banker_deal_sum']:
            game['outcome'] = 'T'
        
    elif game['player_draw_sum'] != None and game['banker_draw_sum'] != None:
        if game['player_draw_sum'] > game['banker_draw_sum']:
            game['outcome'] = 'P'
        elif game['player_draw_sum'] < game['banker_draw_sum']:
            game['outcome'] = 'B'
        elif game['player_draw_sum'] == game['banker_draw_sum']:
            game['outcome'] = 'T'
    
    else:
        print('Game not evaluated!')
    
    return game

def simulations(n_games = 100000):
    
    p_wins = 0
    b_wins = 0
    t = 0
    games = []
    for i in range(n_games):
        game = play_baccarat_hand()
        game = evaluate_game(game)
        if game['outcome'] == 'P':
            p_wins += 1
        elif game['outcome'] == 'B':
            b_wins += 1
        elif game['outcome'] == 'T':
            t += 1
        games.append(game)

    return games

def probability_given(deal_hand_value, n_sims = 10000):
    player_wins = 0
    banker_wins = 0
    ties = 0
    count = 0
    while count < n_sims:
        game = play_baccarat_hand()
        game = evaluate_game(game)
        
        if game['player_deal_sum'] != deal_hand_value:
            pass
        else:
            count += 1
            if game['outcome'] == 'P':
                player_wins += 1
            elif game['outcome'] == 'B':
                banker_wins += 1
            else:
                ties += 1
                
    print(f"P(player W | {deal_hand_value}) = {player_wins / n_sims}")
    print(f"P(banker W | {deal_hand_value}) = {banker_wins / n_sims}")
    print(f"P(T | {deal_hand_value}) = {ties / n_sims}")
    print()

def probability_low_tie_max(n_sims = 10000):
    
    ties = 0
    for i in range(n_sims):
        game = play_baccarat_hand()
        game = evaluate_game(game)
        
        allowed = ['2', '3', '4', '5', '10', 'J', 'Q', 'K', 'A']
        p = game['player_hand']
        b = game['banker_hand']
        
        
        if game['outcome'] == 'T':
            decider = 0
            for card in p:
                if card[0] not in allowed:
                    decider += 1
            for card in b:
                if card[0] not in allowed:
                    decider += 1
                    
            if decider == 0:
                ties += 1
                
    print(f"P(low-tie-max) = {ties / n_sims}")
    print()
                
def probability_dragon_7(n_sims = 10000):
    
    banker_wins = 0
    for i in range(n_sims):
        game = play_baccarat_hand()
        game = evaluate_game(game)
        
        if game['outcome'] == 'B' and len(game['banker_hand']) == 3 and game['banker_draw_sum'] == 7:
            banker_wins += 1

    print(f"P(dragon-7) = {banker_wins / n_sims}")
    print()

if __name__ == '__main__':
    print("Baccarat probabilities ...")
    probability_given(4)
    probability_given(5)
    probability_low_tie_max()
    probability_dragon_7()
    print()
    print()
    print()



'''
    #2
'''

def score_hand(hand):
    
    score = 0
    for card in hand:
        score += card[0]
        
    if (11, 'H') in hand or (11, 'D') in hand or (11, 'C') in hand or (11, 'S') in hand: # <-- Check Ace high or low. By default high but if goes bust switch to low.
        if score > 21:
            score = score - 10
    return score

def does_player_hit(player_hand, dealer_hand): # <-- Unlike dealer, player considers opponent hand
    # TODO -- We assume player will follow basic strategy card
    p_score = score_hand(player_hand)
    d_score = score_hand(dealer_hand)
    d_upcard = dealer_hand[0][0]
    
    if 5 <= p_score <= 11: # <-- Simple strat: If player has init socre between 5 and 11 hit
        return True
    elif p_score == 12:
        if d_upcard in [4, 5, 6]:
            return False
        else:
            return True
    elif p_score in [13, 14, 15, 16]:
        if d_upcard in [2, 3, 4, 5, 6]:
            return False
        else:
            return True
    elif p_score > 17:
        return False
    
def does_dealer_hit(dealer_hand):
    if score_hand(dealer_hand) >= 17:
        return False
    
    return True

def play_blackjack_infinite_decks(): # <-- Simulate single hand of blackjack, returning hand outcome
        
    hand_dict = {'init_player_score': None,
                 'init_dealer_score': None,
                 'final_player_score': None,
                 'final_dealer_score': None,
                 'outcome': None}

    deck = shuffle([(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (11, 'H'),
          (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (11, 'D'),
          (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (11, 'C'),
          (2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (11, 'S')])
    player_hand = [deck.pop(), deck.pop()]
    
    deck = shuffle([(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (11, 'H'),
          (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (11, 'D'),
          (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (11, 'C'),
          (2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (11, 'S')])
    dealer_hand = [deck.pop(), deck.pop()]
    
    player_score = score_hand(player_hand)
    dealer_score = score_hand(dealer_hand)
    hand_dict['init_player_score'] = player_score
    hand_dict['init_dealer_score'] = dealer_score

    player_decison = does_player_hit(player_hand, dealer_hand)
    while player_decison: # <-- Player will hit until decides to not
        deck = shuffle([(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (11, 'H'),
              (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (11, 'D'),
              (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (11, 'C'),
              (2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (11, 'S')])
        player_hand.append(deck.pop())
        player_decison = does_player_hit(player_hand, dealer_hand)
    
    hand_dict['final_player_score'] = score_hand(player_hand)
    
    if score_hand(player_hand) > 21: # <-- Check bust before dealer decisions
        # print(f'Dealer beats player. Player went bust with {score_hand(player_hand)}')
        hand_dict['outcome'] = 'Dealer'
        return hand_dict
    
    dealer_decision = does_dealer_hit(dealer_hand)
    while dealer_decision: # <-- Dealer will hit until decides to not
        deck = shuffle([(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (11, 'H'),
              (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (11, 'D'),
              (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (11, 'C'),
              (2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (11, 'S')])
        dealer_hand.append(deck.pop())
        dealer_decision = does_dealer_hit(dealer_hand)
    
    hand_dict['final_dealer_score'] = score_hand(dealer_hand)
    
    if score_hand(dealer_hand) > 21: # <-- Check dealer bust before hand compare
        # print(f'Player beats dealer. Dealer went bust with {score_hand(dealer_hand)}')
        hand_dict['outcome'] = 'Player'
        return hand_dict
    
    if score_hand(player_hand) > score_hand(dealer_hand):
        # print(f'Player ({score_hand(player_hand)}) beats dealer ({score_hand(dealer_hand)})')
        hand_dict['outcome'] = 'Player'
        return hand_dict
    elif score_hand(player_hand) < score_hand(dealer_hand):
        # print(f'Dealer ({score_hand(dealer_hand)}) beats player ({score_hand(player_hand)})')
        hand_dict['outcome'] = 'Dealer'
        return hand_dict
    else:
        # print(f'Player ({score_hand(player_hand)}) and dealer ({score_hand(dealer_hand)}) tie')
        hand_dict['outcome'] = 'Push'
        return hand_dict

def play_blackjack_one_deck(): # <-- Simulate single hand of blackjack, returning hand outcome
    
    deck = [(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (11, 'H'),
          (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (11, 'D'),
          (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (11, 'C'),
          (2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (11, 'S')]
    
    shuffle(deck)
    hand_dict = {'init_player_score': None,
                 'init_dealer_score': None,
                 'final_player_score': None,
                 'final_dealer_score': None,
                 'outcome': None}

    
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    
    player_score = score_hand(player_hand)
    dealer_score = score_hand(dealer_hand)
    hand_dict['init_player_score'] = player_score
    hand_dict['init_dealer_score'] = dealer_score

    player_decison = does_player_hit(player_hand, dealer_hand)
    while player_decison: # <-- Player will hit until decides to not
        player_hand.append(deck.pop())
        player_decison = does_player_hit(player_hand, dealer_hand)
    
    hand_dict['final_player_score'] = score_hand(player_hand)
    
    if score_hand(player_hand) > 21: # <-- Check bust before dealer decisions
        # print(f'Dealer beats player. Player went bust with {score_hand(player_hand)}')
        hand_dict['outcome'] = 'Dealer'
        return hand_dict
    
    dealer_decision = does_dealer_hit(dealer_hand)
    while dealer_decision: # <-- Dealer will hit until decides to not
        dealer_hand.append(deck.pop())
        dealer_decision = does_dealer_hit(dealer_hand)
    
    hand_dict['final_dealer_score'] = score_hand(dealer_hand)
    
    if score_hand(dealer_hand) > 21: # <-- Check dealer bust before hand compare
        # print(f'Player beats dealer. Dealer went bust with {score_hand(dealer_hand)}')
        hand_dict['outcome'] = 'Player'
        return hand_dict
    
    if score_hand(player_hand) > score_hand(dealer_hand):
        # print(f'Player ({score_hand(player_hand)}) beats dealer ({score_hand(dealer_hand)})')
        hand_dict['outcome'] = 'Player'
        return hand_dict
    elif score_hand(player_hand) < score_hand(dealer_hand):
        # print(f'Dealer ({score_hand(dealer_hand)}) beats player ({score_hand(player_hand)})')
        hand_dict['outcome'] = 'Dealer'
        return hand_dict
    else:
        # print(f'Player ({score_hand(player_hand)}) and dealer ({score_hand(dealer_hand)}) tie')
        hand_dict['outcome'] = 'Push'
        return hand_dict

def play_blackjack_six_decks(): # <-- Simulate single hand of blackjack, returning hand outcome
    
    deck = [(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (11, 'H'),
          (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (11, 'D'),
          (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (11, 'C'),
          (2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (11, 'S')]
    shoe = [card for card in deck for i in range(6)]
    shuffle(shoe)

    hand_dict = {'init_player_score': None,
                 'init_dealer_score': None,
                 'final_player_score': None,
                 'final_dealer_score': None,
                 'outcome': None}
    
    player_hand = [shoe.pop(), shoe.pop()]
    dealer_hand = [shoe.pop(), shoe.pop()]
    
    player_score = score_hand(player_hand)
    dealer_score = score_hand(dealer_hand)
    hand_dict['init_player_score'] = player_score
    hand_dict['init_dealer_score'] = dealer_score

    player_decison = does_player_hit(player_hand, dealer_hand)
    while player_decison: # <-- Player will hit until decides to not
        player_hand.append(shoe.pop())
        player_decison = does_player_hit(player_hand, dealer_hand)
    
    hand_dict['final_player_score'] = score_hand(player_hand)
    
    if score_hand(player_hand) > 21: # <-- Check bust before dealer decisions
        # print(f'Dealer beats player. Player went bust with {score_hand(player_hand)}')
        hand_dict['outcome'] = 'Dealer'
        return hand_dict
    
    dealer_decision = does_dealer_hit(dealer_hand)
    while dealer_decision: # <-- Dealer will hit until decides to not
        dealer_hand.append(shoe.pop())
        dealer_decision = does_dealer_hit(dealer_hand)
    
    hand_dict['final_dealer_score'] = score_hand(dealer_hand)
    
    if score_hand(dealer_hand) > 21: # <-- Check dealer bust before hand compare
        # print(f'Player beats dealer. Dealer went bust with {score_hand(dealer_hand)}')
        hand_dict['outcome'] = 'Player'
        return hand_dict
    
    if score_hand(player_hand) > score_hand(dealer_hand):
        # print(f'Player ({score_hand(player_hand)}) beats dealer ({score_hand(dealer_hand)})')
        hand_dict['outcome'] = 'Player'
        return hand_dict
    elif score_hand(player_hand) < score_hand(dealer_hand):
        # print(f'Dealer ({score_hand(dealer_hand)}) beats player ({score_hand(player_hand)})')
        hand_dict['outcome'] = 'Dealer'
        return hand_dict
    else:
        # print(f'Player ({score_hand(player_hand)}) and dealer ({score_hand(dealer_hand)}) tie')
        hand_dict['outcome'] = 'Push'
        return hand_dict

def play_blackjack_arbitrary_shoe(shoe): # <-- Input deck with any order, n_remaining, etc and play hand

    hand_dict = {'init_player_score': None,
                 'init_dealer_score': None,
                 'final_player_score': None,
                 'final_dealer_score': None,
                 'outcome': None}


    player_hand = [shoe.pop(), shoe.pop()]
    dealer_hand = [shoe.pop(), shoe.pop()]

    player_score = score_hand(player_hand)
    dealer_score = score_hand(dealer_hand)
    hand_dict['init_player_score'] = player_score
    hand_dict['init_dealer_score'] = dealer_score

    player_decison = does_player_hit(player_hand, dealer_hand)
    while player_decison: # <-- Player will hit until decides to not
        player_hand.append(shoe.pop())
        player_decison = does_player_hit(player_hand, dealer_hand)

    hand_dict['final_player_score'] = score_hand(player_hand)

    if score_hand(player_hand) > 21: # <-- Check bust before dealer decisions
        # print(f'Dealer beats player. Player went bust with {score_hand(player_hand)}')
        hand_dict['outcome'] = 'Dealer'
        return hand_dict

    dealer_decision = does_dealer_hit(dealer_hand)
    while dealer_decision: # <-- Dealer will hit until decides to not
        dealer_hand.append(shoe.pop())
        dealer_decision = does_dealer_hit(dealer_hand)

    hand_dict['final_dealer_score'] = score_hand(dealer_hand)

    if score_hand(dealer_hand) > 21: # <-- Check dealer bust before hand compare
        # print(f'Player beats dealer. Dealer went bust with {score_hand(dealer_hand)}')
        hand_dict['outcome'] = 'Player'
        return hand_dict

    if score_hand(player_hand) > score_hand(dealer_hand):
        # print(f'Player ({score_hand(player_hand)}) beats dealer ({score_hand(dealer_hand)})')
        hand_dict['outcome'] = 'Player'
        return hand_dict
    elif score_hand(player_hand) < score_hand(dealer_hand):
        # print(f'Dealer ({score_hand(dealer_hand)}) beats player ({score_hand(player_hand)})')
        hand_dict['outcome'] = 'Dealer'
        return hand_dict
    else:
        # print(f'Player ({score_hand(player_hand)}) and dealer ({score_hand(dealer_hand)}) tie')
        hand_dict['outcome'] = 'Push'
        return hand_dict

def conditional_probabilities(deck_setting, init_dealer_score, n_cases = 10000):

    total_of_case = 0
    seventeens = 0
    eighteens = 0
    nineteens = 0
    twenties = 0
    twentyones = 0
    busts = 0
    
    while total_of_case < n_cases:
        if deck_setting == 'infinite':
            hand = play_blackjack_infinite_decks()
        elif deck_setting == 'one':
            hand = play_blackjack_one_deck()
        elif deck_setting == 'six':
            hand = play_blackjack_six_decks()
            
        if hand['init_dealer_score'] == init_dealer_score:
            total_of_case += 1
            if hand['final_player_score'] == 17:
                seventeens += 1
            elif hand['final_player_score'] == 18:
                eighteens += 1
            elif hand['final_player_score'] == 19:
                nineteens += 1
            elif hand['final_player_score'] == 20:
                twenties += 1
            elif hand['final_player_score'] == 21:
                twentyones += 1
            elif hand['final_player_score'] > 21:
                busts += 1
    
    records = {'17': seventeens, '18': eighteens, '19': nineteens, '20': twenties, '21': twentyones, 'Bust': busts}
    for case in records:
        p = records[case] / total_of_case
        print(f'P(player = {case} | init_dealer_score = {str(init_dealer_score)}) = {p}')

def blackjack_probability(deck_setting, n_sims = 10000):
    
    blackjacks = 0
    for i in range(n_sims):
        if deck_setting == 'infinite':
            hand = play_blackjack_infinite_decks()
        elif deck_setting == 'one':
            hand = play_blackjack_one_deck()
        elif deck_setting == 'six':
            hand = play_blackjack_six_decks()
            
        if hand['init_player_score'] == 21: # <-- Natural, Blackjack
            blackjacks += 1
            
    p = blackjacks / n_sims
    print(f'P(player = blackjack) = {p}')

def hi_lo_count(deck_shoe, cards_left): # <-- Considers a shoe of arbitrary n_decks. Returns count after cards_left cards remaining
    
    count = 0
    for i in range(len(deck_shoe) - cards_left):
        value = deck_shoe[i][0]
        if value in [2, 3, 4, 5, 6]:
            count += 1
        elif value in [10, 11]:
            count -= 1
            
    return count # <-- Return count with n_cards left in shoe

def blackjack_probability_with_card_count(shoe_deck_size = 1, cards_left = 26, specified_count_with_n_left = 5, n_sims = 100):
    
    deck = [(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (10, 'H'), (11, 'H'),
          (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (10, 'D'), (11, 'D'),
          (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (10, 'C'), (11, 'C'),
          (2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (10, 'S'), (11, 'S')]

    sims = 0
    blackjacks = 0
    while sims < n_sims:
        shoe = shuffle([card for card in deck for i in range(shoe_deck_size)])
        
        acutal_count_with_n_left = hi_lo_count(shoe, cards_left)
        if acutal_count_with_n_left == specified_count_with_n_left: # <-- Deck is of desirable count with n cards left
            sims += 1
            hand = play_blackjack_arbitrary_shoe(shoe)
            if hand['init_player_score'] == 21: # <-- Natural blackjack
                blackjacks += 1
            
    p = blackjacks / sims
    print(f'P(player = blackjack | count = {specified_count_with_n_left} with {cards_left} cards left in {shoe_deck_size} deck shoe) = {p}')
    

if __name__ == '__main__':
    print("Blackjack probabilities ...")

    conditional_probabilities('infinite', 11)
    print()
    conditional_probabilities('infinite', 12)
    print()
    conditional_probabilities('infinite', 13)
    print()

    deck_settings = ['infinite', 'one', 'six']
    for setting in deck_settings:
        print(f'For {setting} deck setting ...')
        blackjack_probability(setting)

    blackjack_probability_with_card_count(shoe_deck_size = 1, cards_left = 26, specified_count_with_n_left = 5)
    print()
    blackjack_probability_with_card_count(shoe_deck_size = 1, cards_left = 26, specified_count_with_n_left = 7)
    print()
    blackjack_probability_with_card_count(shoe_deck_size = 6, cards_left = 104, specified_count_with_n_left = 15)
    print()
    blackjack_probability_with_card_count(shoe_deck_size = 6, cards_left = 104, specified_count_with_n_left = 20)
    print()
    blackjack_probability_with_card_count(shoe_deck_size = 6, cards_left = 52, specified_count_with_n_left = 15)
    print()
    blackjack_probability_with_card_count(shoe_deck_size = 6, cards_left = 52, specified_count_with_n_left = 20)
