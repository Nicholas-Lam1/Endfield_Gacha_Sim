import random
import numpy as np

# Constants
SOFT_PITY_BASE_RATE = 0.008  
SOFT_PITY_INCREMENT = 0.05
HARD_PITY_INTERVAL = 80
LIMITED_PITY_INTERVAL = 120
DUPLICATE_PITY_INTERVAL = 240
FIVE_STAR_RATE = 0.08
GUARANTEED_5_STAR_INTERVAL = 10

SIX_STAR_ARSENAL = 2000
FIVE_STAR_ARSENAL = 200
FOUR_STAR_ARSENAL = 20
ARSENAL_PULL_COST = 1980

def gacha_simulation(pull_quantity = None, pot_quantity = None, arsenal_quantity = None, sample_size = 100000):
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
    arsenal_totals = []
    pull_totals = []

    if arsenal_quantity is not None:
        arsenal_quantity *= 1980

    for iteration in range(sample_size):
        pulls = 0
        got_limited = False
        limited_6_star_count = 0
        total_6_star_count = 0
        guaranteed_5_star_counter = 0
        total_5_star_count = 0
        total_4_star_count = 0
        pity_counter = 0
        arsenal_counter = 0
        pity_rate = SOFT_PITY_BASE_RATE

        if pull_quantity is not None:
            loop_exit_condition = lambda: pulls >= pull_quantity
        elif pot_quantity is not None:
            loop_exit_condition = lambda: limited_6_star_count >= pot_quantity
        elif arsenal_quantity is not None:
            loop_exit_condition = lambda: arsenal_counter >= arsenal_quantity
        else:
            raise ValueError("At least one of pull_quantity, pot_quantity, or arsenal_quantity must be provided.")

        # while limited_6_star_count < pot_quantity:
        #   pulls += 1 
        # while arsenal_counter < arsenal_quantity:
        #   pulls += 1
        # for pulls in range(1, pull_quantity + 1):
        while not loop_exit_condition():
            pulls += 1
            pity_counter += 1

            # Add limited 6* for every 240 pulls
            if pulls % DUPLICATE_PITY_INTERVAL == 0:
                limited_6_star_count += 1 
                total_6_star_count += 1
                arsenal_counter += 2000
                pity_rate = SOFT_PITY_BASE_RATE

            # Add limited 6* on the 120th pull
            if not got_limited and pulls == LIMITED_PITY_INTERVAL:
                limited_6_star_count += 1
                total_6_star_count += 1
                arsenal_counter += 2000
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
                arsenal_counter += 2000

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
                    arsenal_counter += 2000

                # Else, up soft pity by 5% and finish pull
                else:
                    if(pity_counter > 65):
                        pity_rate += SOFT_PITY_INCREMENT

                    # If nine 4* operators have been pulled, pull 5* operator
                    if guaranteed_5_star_counter == GUARANTEED_5_STAR_INTERVAL - 1:
                        total_5_star_count += 1
                        guaranteed_5_star_counter = 0
                        arsenal_counter += 200

                    # Else, try and pull 5*, if failed, pull 4*
                    elif random.random() < FIVE_STAR_RATE:
                        total_5_star_count += 1
                        guaranteed_5_star_counter = 0
                        arsenal_counter += 200
                    
                    else:
                        total_4_star_count += 1
                        guaranteed_5_star_counter += 1
                        arsenal_counter += 20

        limited_6_totals.append(limited_6_star_count)
        total_6_totals.append(total_6_star_count)
        total_5_totals.append(total_5_star_count)
        total_4_totals.append(total_4_star_count)
        arsenal_totals.append(arsenal_counter)
        pull_totals.append(pulls)
        # print(f"Iteration {interation}")

    # Average counts of operators across all iterations
    mean_limited_6 = np.mean(limited_6_totals)
    mean_6 = np.mean(total_6_totals)
    mean_5 = np.mean(total_5_totals)
    mean_4 = np.mean(total_4_totals)
    mean_arsenal = np.mean(arsenal_totals)
    mean_pulls = np.mean(pull_totals)

    mean_arsenal_pulls = mean_arsenal / ARSENAL_PULL_COST

    print()
    if pull_quantity != None:
        print(f"{sample_size} Simultated Runs of {pull_quantity} Pulls")
    elif pot_quantity != None:
        print(f"{sample_size} Simultated Runs of Pulling {pot_quantity} Rate-Up Pots")
    elif arsenal_quantity != None:
        print(f"{sample_size} Simultated Runs of Pulling {arsenal_quantity} Arsenal Pulls")
    print("---------------------------------------------")
    if pull_quantity == None:
        print(f"Mean number of pulls performed: {mean_pulls}")
    print(f"Mean number of limited 6*: {mean_limited_6}")
    print(f"Mean number of 6* (Including limited 6*): {mean_6}")
    print(f"Mean number of 5*: {mean_5}")
    print(f"Mean number of 4*: {mean_4}")
    print(f"Mean arsenal tokens: {mean_arsenal}")
    print(f"Mean arsenal pull count: {mean_arsenal_pulls}")
    print("---------------------------------------------")

print("\r\nAK Endfield Gacha Simulator\r\n")
while True:
    print("What would you like to simulate:")
    print("1. Rewards for # of pulls")
    print("2. # of pulls to get X amount of rate-up pots")
    print("3. # of pulls to get X amount of 10x arsenal pulls")
    choice = int(input("Please enter a number (1, 2, or 3): "))
    val = 0
    match choice:
        case 1:
            val = int(input("Please enter number of pulls to simulate: "))
        case 2:
            val = int(input("Please enter number of rate-up pots to simulate: "))
        case 3:
            val = int(input("Please enter number of 10x arsenal pulls to simulate: "))
        case _:
            print("Unknown value, please try again")

    if val > 0:
        match choice:
            case 1:
                gacha_simulation(pull_quantity=val)
            case 2:
                gacha_simulation(pot_quantity=val)
            case 3:
                gacha_simulation(arsenal_quantity=val)
    else:
        print("Unknown value, please try again")

    input("\nPress enter to return to menu\n")

