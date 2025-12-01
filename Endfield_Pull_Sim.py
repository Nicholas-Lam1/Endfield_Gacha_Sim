import random
import numpy as np
from collections import Counter

# Constants
SOFT_PITY_BASE_RATE = 0.008  
SOFT_PITY_INCREMENT = 0.05
HARD_PITY_INTERVAL = 80
LIMITED_PITY_INTERVAL = 120
DUPLICATE_PITY_INTERVAL = 240
FIVE_STAR_RATE = 0.08
GUARANTEED_5_STAR_INTERVAL = 10
PULL_QUANTITY = 
SAMPLE_SIZE = 500000

SIX_STAR_ARSENAL = 2000
FIVE_STAR_ARSENAL = 200
FOUR_STAR_ARSENAL = 20
ARSENAL_PULL_COST = 1980

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

    limited_6_totals = []
    total_6_totals = []
    total_5_totals = []
    total_4_totals = []

    for iteration in range(SAMPLE_SIZE):
        got_limited = False
        limited_6_star_count = 0
        total_6_star_count = 0
        guaranteed_5_star_counter = 0
        total_5_star_count = 0
        total_4_star_count = 0
        pity_counter = 0
        pity_rate = SOFT_PITY_BASE_RATE

        for pulls in range(1, PULL_QUANTITY + 1):
            pity_counter += 1

            # Add limited 6* for every 240 pulls
            if pulls % DUPLICATE_PITY_INTERVAL == 0 and pulls != 0:
                limited_6_star_count += 1
                total_6_star_count += 1
                pity_rate = SOFT_PITY_BASE_RATE

            # Add limited 6* on the 120th pull
            if not got_limited and pulls == LIMITED_PITY_INTERVAL:
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
                    got_limited = True
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
                        got_limited = True
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

        limited_6_totals.append(limited_6_star_count)
        total_6_totals.append(total_6_star_count)
        total_5_totals.append(total_5_star_count)
        total_4_totals.append(total_4_star_count)
        # print(f"Iteration {interation}")


    mean_limited_6 = np.mean(limited_6_totals)
    mean_6 = np.mean(total_6_totals)
    mean_5 = np.mean(total_5_totals)
    mean_4 = np.mean(total_4_totals)

    return mean_limited_6, mean_6, mean_5, mean_4

mean_limited_6, mean_6, mean_5, mean_4 = gacha_simulation()

arsenal_6 = mean_6 * SIX_STAR_ARSENAL
arsenal_5 = mean_5 * FIVE_STAR_ARSENAL
arsenal_4 = mean_4 * FOUR_STAR_ARSENAL
mean_arsenal = arsenal_6 + arsenal_5 + arsenal_4
mean_arsenal_pulls = mean_arsenal / ARSENAL_PULL_COST

print(f"{SAMPLE_SIZE} Simultated Runs of {PULL_QUANTITY} Pulls")
print("---------------------------------------------")
print(f"Mean number of limited 6*: {mean_limited_6}")
print(f"Mean number of 6* (Including limited 6*): {mean_6}")
print(f"Mean number of 5*: {mean_5}")
print(f"Mean number of 4*: {mean_4}")
print(f"Mean arsenal tokens: {mean_arsenal}")
print(f"Mean arsenal pull count: {mean_arsenal_pulls}")
print("---------------------------------------------")
