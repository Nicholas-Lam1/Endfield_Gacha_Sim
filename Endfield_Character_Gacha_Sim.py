import random
import numpy as np
from collections import Counter

def gacha_simulation():
    """
    Soft-Pity: 65 pulls (Each pull after increases 6* rate by 5%)
    Hard-Pity: Every 80 pulls
    Limited-Pity: First 120 pulls
    Dupe-Pity: Every 240 pulls

    6* Rate: 0.8%
    5* Rate: 8%

    One 5* guaranteed each 10 pulls

    Notes:
    Hard-pity is always 50/50
    6 copies required to get and then max pot character.
    """
    
    # Constants
    SOFT_PITY_BASE_RATE = 0.008  
    SOFT_PITY_INCREMENT = 0.05
    HARD_PITY_INTERVAL = 80
    LIMITED_PITY_INTERVAL = 120
    DUPLICATE_PITY_INTERVAL = 240
    FIVE_STAR_RATE = 0.08
    GUARANTEED_5_STAR_INTERVAL = 10
    SAMPLE_SIZE = 1000000

    pulls_to_6_copies = []

    for interation in range(SAMPLE_SIZE):
        pulls = 0
        limited_6_star_count = 0
        total_6_star_count = 0
        guaranteed_5_star_counter = 0
        total_5_star_count = 0
        total_4_star_count = 0
        pity_counter = 0
        pity_rate = SOFT_PITY_BASE_RATE

        while limited_6_star_count < 6:
            pulls += 1
            pity_counter += 1

            # Add limited 6* for every 240 pulls
            if pulls % DUPLICATE_PITY_INTERVAL == 0:
                limited_6_star_count += 1
                total_6_star_count += 1
                pity_rate = SOFT_PITY_BASE_RATE

            # Add limited 6* on the 120th pull
            if pulls == LIMITED_PITY_INTERVAL:
                limited_6_star_count += 1
                total_6_star_count += 1
                pity_rate = SOFT_PITY_BASE_RATE
                pity_counter = 0  
                guaranteed_5_star_counter = 0

            # If at hard pity, pull 6* operator, with 50% chance of being limited 6*
            if pity_counter == HARD_PITY_INTERVAL:
                pity_counter = 0
                if random.random() < 0.5:
                    limited_6_star_count += 1
                else:
                    pass 
                pity_rate = SOFT_PITY_BASE_RATE
                total_6_star_count += 1
                guaranteed_5_star_counter = 0

            # Otherwise, check soft pity
            else: 
                # If passed soft pity, pull 6* operator, with 50% chance of being limited 6*
                if random.random() < pity_rate:
                    pity_counter = 0
                    if random.random() < 0.5:
                        limited_6_star_count += 1
                    else:
                        pass
                    pity_rate = SOFT_PITY_BASE_RATE
                    total_6_star_count += 1
                    guaranteed_5_star_counter = 0

                # Else, up soft pity by 5% and finish pull
                else:
                    if(pity_counter > 65):
                        pity_rate += SOFT_PITY_INCREMENT

                    # If nine 4* operators have been pulled, pull 5* operator
                    if guaranteed_5_star_counter == GUARANTEED_5_STAR_INTERVAL - 1:
                        total_5_star_count += 1
                        guaranteed_5_star_counter = 0

                    # Else, try and pull 5*, if failed, pull 4*
                    elif random.random() < FIVE_STAR_RATE:
                        total_5_star_count += 1
                        guaranteed_5_star_counter = 0
                    
                    else:
                        total_4_star_count += 1
                        guaranteed_5_star_counter += 1                

        pulls_to_6_copies.append(pulls)
        # print(f"Iteration {interation}: {pulls} pulls")

    mean_pulls = np.mean(pulls_to_6_copies)
    median_pulls = np.median(pulls_to_6_copies)
    max_pulls = np.max(pulls_to_6_copies)
    min_pulls = np.min(pulls_to_6_copies)
    
    mode_data = Counter(pulls_to_6_copies).most_common(1)
    mode_pulls = mode_data[0][0]
    mode_frequency = mode_data[0][1]

    return mean_pulls, median_pulls, max_pulls, min_pulls, mode_pulls, mode_frequency

mean, median, max_val, min_val, mode, mode_freq = gacha_simulation()

print(f"Mean number of pulls to get 6 copies: {mean}")
print(f"Median number of pulls to get 6 copies: {median}")
print(f"Max number of pulls to get 6 copies: {max_val}")
print(f"Min number of pulls to get 6 copies: {min_val}")
print(f"Mode number of pulls to get 6 copies: {mode}, {mode_freq}")
