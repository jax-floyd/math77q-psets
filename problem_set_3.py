import time
import random
from itertools import combinations
from collections import Counter
from matplotlib import pyplot as plt

'''
    # 1
'''
def shuffled_deck():
    suits = ['S', 'H', 'D', 'C']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)

    return deck

def deal_five(deck = shuffled_deck()):
    return [deck.pop() for i in range(5)] # <-- 5 card hand

def deal_six(deck = shuffled_deck()):
    return [deck.pop() for i in range(6)] # <-- 6 card hand

# Helpers determine hand ranking
def is_royal_flush(hand):

    royal_flush = ['10', 'J', 'Q', 'K', 'A']
    hand_values = [card[0] for card in hand]
    hand_suits = [card[1] for card in hand]
    
    if set(royal_flush) <= set(hand_values) and len(set(hand_suits)) == 1:
        return True
    
    return False

def is_straight_flush(hand):
    
    if is_straight(hand) and is_flush(hand):
        return True
    
    return False

def is_four_of_a_kind(hand):

  rank_counts = {}
  for card in hand:
    rank = card[0]
    if rank in rank_counts:
      rank_counts[rank] += 1
    else:
      rank_counts[rank] = 1

  for rank, count in rank_counts.items():
    if count == 4:
      return True

  return False

def is_full_house(hand):
    
    ranks = [card[0] for card in hand]
    rank_counts = Counter(ranks)
    return len(rank_counts) == 2 and 2 in rank_counts.values() and 3 in rank_counts.values()

def is_flush(hand):
    
    suits = set([card[1] for card in hand])
    
    if not is_straight(hand):
        return len(suits) == 1
    else:
        return False

def is_straight(hand):
    
    cards = set([card[0] for card in hand])
    if len(cards) >= 5: # <-- Check for 5 consecutive values
        face_to_rank = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        ranks = [face_to_rank[card] for card in cards]
        
        if 2 in ranks and 3 in ranks and 4 in ranks and 5 in ranks and 14 in ranks: # <-- Low ace straight
            return True

        # Check if the set contains five consecutive values
        ranks = sorted(ranks)
        if ranks[0] == ranks[1] - 1 and ranks[1] == ranks[2] - 1 and ranks[2] == ranks[3] - 1 and ranks[3] == ranks[4] - 1:
            return True

    # If we didn't find a straight, return False
    return False

def is_trips(hand):
    
    rank_counts = {}
    for card in hand:
      rank = card[0]
      if rank in rank_counts:
        rank_counts[rank] += 1
      else:
        rank_counts[rank] = 1

    for rank, count in rank_counts.items():
      if count == 3:
        return True

    return False
    
def is_two_pair(hand):
  
  rank_counts = {} # <-- Create dictionary that maps each card rank to the number of times it appears in the hand
  for card in hand:
    rank = card[0]
    if rank in rank_counts:
      rank_counts[rank] += 1
    else:
      rank_counts[rank] = 1

  num_pairs = 0
  for count in rank_counts.values():
    if count == 2:
      num_pairs += 1

  return num_pairs == 2

def is_pair(hand):
    
    rank_counts = {}
    for card in hand:
      rank = card[0]
      if rank in rank_counts:
        rank_counts[rank] += 1
      else:
        rank_counts[rank] = 1

    num_pairs = 0
    for count in rank_counts.values():
      if count == 2:
        num_pairs += 1

    return num_pairs == 1

def determine_hand_rank(hand):
    
    if is_royal_flush(hand):
        return 'Royal Flush'
    elif is_straight_flush(hand):
        return 'Straight Flush'
    elif is_four_of_a_kind(hand):
        return 'Quads'
    elif is_full_house(hand):
        return 'Boat'
    elif is_flush(hand):
        return 'Flush'
    elif is_straight(hand):
        return 'Straight'
    elif is_trips(hand):
        return 'Trips'
    elif is_two_pair(hand):
        return 'Two Pair'
    elif is_pair(hand):
        return 'Pair'
    else: # <-- High card
        return 'High Card'

def simulate_hands(n_sims = 10000000):
    
    hand_ranks_to_relative_values = {9: 'Royal Flush', 8: 'Straight Flush', 7: 'Quads', 6: 'Boat', 5: 'Flush', 4: 'Straight', 3: 'Trips', 2: 'Two Pair', 1: 'Pair', 0: 'High Card'}
    hand_to_probability = {'Royal Flush': 0, 'Straight Flush': 0, 'Quads': 0, 'Boat': 0, 'Flush': 0, 'Straight': 0, 'Trips': 0, 'Two Pair': 0, 'Pair': 0, 'High Card': 0}
    relative_values_to_hand_ranks = {'Royal Flush': 9, 'Straight Flush': 8, 'Quads': 7, 'Boat': 6, 'Flush': 5, 'Straight': 4, 'Trips': 3, 'Two Pair': 2, 'Pair': 1, 'High Card': 0}
    
    for i in range(n_sims):
        deck = shuffled_deck()
        deal = deal_six(deck)
        hand_combinations = combinations(deal, 5) # <-- All 6 choose 5 combinations of the deal

        combination_ranks = set([determine_hand_rank(combo) for combo in hand_combinations]) # <-- Holds hand ranks of all combinations
        combination_rank_values = [relative_values_to_hand_ranks[rank] for rank in combination_ranks]

        top_combo = hand_ranks_to_relative_values.get(max(combination_rank_values))
        hand_to_probability[top_combo] += 1
            
    for hand in hand_to_probability:
        print(f"The probability of a {hand} is {hand_to_probability[hand] / (n_sims)}")

'''
    # 2
'''

gene = {'fg_pct': 0.5, 'offensive_rebound_pct': 0.2, 'defensive_rebound_pct': 0.5} # <-- Gene you need to box out my guy
olivia = {'fg_pct': 0.4, 'offensive_rebound_pct': 0.5, 'defensive_rebound_pct': 0.8}

def shoot(player): # <-- Returns T if make, F is miss

    r = random.random()
    if r < player['fg_pct']:
        return True
    else:
        return False

def rebound(player, rebound_class): # <-- Returns T if player successfully rebounded, else F. Considers offensive / defensive board

    r = random.random()
    if rebound_class == 'offensive':
        if r < player['offensive_rebound_pct']:
            return True
        else:
            return False
        
    elif rebound_class == 'defensive':
        if r < player['defensive_rebound_pct']:
            return True
        else:
            return False

def play_a_point(possession, total_shots_taken, olivia_rebounds, gene_rebounds): # <-- Function simulates game play UNTIL one point has been scored. Returns player who won the point

    if possession == 'olivia': # <-- If Olivia is inputted, Olivia starts with possession
        # print("Olivia has posession")
        # print("Olivia takes a shot")
        olivia_shot = shoot(olivia) # <-- Olivia neccessarily shoots first
        if olivia_shot:
            # print("Olivia's shot went in!")
            return {'winner': 'olivia', 'total_shots_taken': total_shots_taken + 1, 'olivia_rebounds': olivia_rebounds, 'gene_rebounds': gene_rebounds} # <-- Olivia scores. We return a tuple of the point winner and total # of shots taken during point
            
        else: # <-- Consider rebound cases to determine possession
            # print("Olivia's shot did not go in")
            # print("Olivia tries for an offensive rebound")
            olivia_attempted_board = rebound(olivia, 'offensive') # <-- Olivia attempts offensive board
            if olivia_attempted_board:
                # print("Olivia got the rebound")
                return play_a_point('olivia', total_shots_taken + 1, olivia_rebounds + 1, gene_rebounds) # <-- Pass in total shots taken to recursive call
            else:
                # print("Gene got the rebound")
                return play_a_point('gene', total_shots_taken + 1, olivia_rebounds, gene_rebounds + 1) # <-- Pass in total shots taken to recursive call
            
    elif possession == 'gene': # <-- If Gene is inputted, Gene starts with possession
        # print("Gene has possession")
        # print("Gene takes a shot")
        gene_shot = shoot(gene)
        if gene_shot:
            # print("Gene's shot went in!")
            return {'winner': 'gene', 'total_shots_taken': total_shots_taken + 1, 'olivia_rebounds': olivia_rebounds, 'gene_rebounds': gene_rebounds} # <-- Gene scores. We return a tuple of the point winner and total # of shots taken during point
        
        else: # <-- Consider rebound cases to determine possession
            # print("Gene's shot did not go in")
            # print("Gene tries for an offensive rebound")
            gene_attempted_board = rebound(gene, 'offensive') # <-- Gene attempts offensive board. This will occur at low probability because Gene doesn't box out
            if gene_attempted_board:
                # print("Gene got the rebound")
                return play_a_point('gene', total_shots_taken + 1, olivia_rebounds, gene_rebounds + 1)
            else:
                # print("Olivia got the rebound")
                return play_a_point('olivia', total_shots_taken + 1, olivia_rebounds + 1, gene_rebounds)

def play_a_game():

    starting_possession = 'olivia'
    total_shots_taken = 0
    olivia_pts = 0
    olivia_boards = 0
    gene_pts = 0
    gene_boards = 0
    point_outcomes = []
    
    while total_shots_taken < 100:
        
        if total_shots_taken == 0:
            point = play_a_point(starting_possession, 0, 0, 0) # <-- Olivia neccessarily starts each game with ball
            point_outcome = point['winner']
            
        else:
            point = play_a_point(point_outcome, 0, 0, 0)
            point_outcome = point['winner']
            
        total_shots_taken += point['total_shots_taken']
        olivia_boards += point['olivia_rebounds']
        gene_boards += point['gene_rebounds']
        
        if point['winner'] == 'olivia':
            olivia_pts += 1
        elif point['winner'] == 'gene':
            gene_pts += 1
            
    game_dict = {'winner': None, 'olivia_points': olivia_pts, 'olivia_rebounds': olivia_boards, 'gene_points': gene_pts, 'gene_rebounds': gene_boards}
    
    if olivia_pts > gene_pts:
        game_dict['winner'] = 'olivia'
        return game_dict
    elif olivia_pts < gene_pts:
        game_dict['winner'] = 'gene'
        return game_dict
    else: # <-- Tie case
        game_dict['winner'] = 'tie'
        return game_dict

def simulate_games(n_sims = 100000):
    
    return [play_a_game() for i in range(n_sims)]

def display_hist_palette():
    
    fig, axs = plt.subplots(2, 2, figsize = (14, 7))
    axs[0, 0].hist(gene_buckets, bins = [i for i in range(50)], color = '#0060ff')
    axs[0, 0].set_title("Distribution of Gene's Point Totals")
    axs[0, 1].hist(olivia_buckets, bins = [i for i in range(50)], color = '#FF0060')
    axs[0, 1].set_title("Distribution of Olivia's Point Totals")
    axs[1, 0].hist(gene_boards, bins = [i for i in range(50)], color = '#0060ff')
    axs[1, 0].set_title("Distribution of Gene's Rebound Totals")
    axs[1, 1].hist(olivia_boards, bins = [i for i in range(50)], color = '#FF0060')
    axs[1, 1].set_title("Distribution of Olivia's Rebound Totals")

    plt.show()

if __name__ == '__main__':
    
    simulate_hands()
    print()
    
    olivia_wins = [game for game in simulate_games() if game['winner'] == 'olivia']
    print(f'Out of 100,0000 games, Olivia won {len(olivia_wins)}.')

    gene_buckets = [game['gene_points'] for game in simulate_games()]
    olivia_buckets = [game['olivia_points'] for game in simulate_games()]
    gene_boards = [game['gene_rebounds'] for game in simulate_games()]
    olivia_boards = [game['olivia_rebounds'] for game in simulate_games()]

    display_hist_palette()
    
