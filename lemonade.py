#!/usr/bin/env python3
"""
LEMONADE STAND

From an original program by Bob Jamison, of the
Minnesota Educational Computing Consortium

Modified for the Apple February, 1979
by Charlie Kellner

Ported to Python 2025
"""

import random
import sys
import math


def cls():
    """Clear the screen (simulated with blank lines)"""
    print("\n" * 50)


def format_money(amount):
    """Format a number as dollars and cents (e.g., $1.23)"""
    amount = round(amount * 100 + 0.5) / 100
    result = f"${amount:.2f}"
    return result


def wait_for_continue():
    """Wait for user to press space or ESC"""
    try:
        print("PRESS SPACE TO CONTINUE, ESC TO END...", end='', flush=True)
    except (BrokenPipeError, IOError):
        return False
    
    try:
        # Check if we have a real terminal
        if not sys.stdin.isatty():
            # Not a terminal, just read a line
            try:
                input()
                return True
            except (EOFError, BrokenPipeError, IOError):
                return False
        
        if sys.platform == 'win32':
            import msvcrt
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b' ':
                        print()
                        return True
                    elif key == b'\x1b':  # ESC
                        print()
                        return False
        else:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
                if key == ' ':
                    print()
                    return True
                elif key == '\x1b':  # ESC
                    print()
                    return False
                else:
                    # Keep waiting if not space or ESC
                    return wait_for_continue()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except (EOFError, BrokenPipeError, IOError, OSError):
        # Fallback if terminal manipulation doesn't work or pipe is broken
        try:
            input()
            return True
        except (EOFError, BrokenPipeError, IOError):
            return False


def get_yes_no(prompt):
    """Get a yes/no answer from the user"""
    while True:
        response = input(prompt).strip().upper()
        if response and response[0] in ['Y', 'N']:
            return response[0]
        print(chr(7), end='')  # Bell character


def get_integer(prompt, min_val=None, max_val=None, allow_non_int=False):
    """Get an integer from the user with optional validation"""
    while True:
        response = input(prompt).strip()
        try:
            if '.' in response and not allow_non_int:
                print("COME ON, LET'S BE REASONABLE NOW!!!")
                print("TRY AGAIN")
                continue
            value = int(float(response))
            if min_val is not None and value < min_val:
                print("COME ON, BE REASONABLE!!! TRY AGAIN.")
                continue
            if max_val is not None and value > max_val:
                print("COME ON, BE REASONABLE!!! TRY AGAIN.")
                continue
            return value
        except ValueError:
            return None


def introduction():
    """Display introduction screen"""
    cls()
    # Original copyright notice commented out as in the BASIC version
    # print("      LEMONADE STAND")
    # print("COPYRIGHT 1979 APPLE COMPUTER INC.")


def title_page():
    """Display title page and get game setup"""
    cls()
    print("HI! WELCOME TO LEMONSVILLE, CALIFORNIA!")
    print()
    print("IN THIS SMALL TOWN, YOU ARE IN CHARGE OF")
    print("RUNNING YOUR OWN LEMONADE STAND. YOU CAN")
    print("COMPETE WITH AS MANY OTHER PEOPLE AS YOU")
    print("WISH, BUT HOW MUCH PROFIT YOU MAKE IS UP")
    print("TO YOU (THE OTHER STANDS' SALES WILL NOT")
    print("AFFECT YOUR BUSINESS IN ANY WAY). IF YOU")
    print("MAKE THE MOST MONEY, YOU'RE THE WINNER!!")
    print()
    print("ARE YOU STARTING A NEW GAME? (YES OR NO)")
    
    new_game = get_yes_no("TYPE YOUR ANSWER AND HIT RETURN ==> ")
    
    while True:
        n_str = input("HOW MANY PEOPLE WILL BE PLAYING ==> ")
        try:
            n = int(n_str)
            if 1 <= n <= 30:
                return new_game, n
        except ValueError:
            pass
        print(chr(7), end='')  # Bell character


def instructions():
    """Display instructions for new players"""
    cls()
    print("TO MANAGE YOUR LEMONADE STAND, YOU WILL ")
    print("NEED TO MAKE THESE DECISIONS EVERY DAY: ")
    print()
    print("1. HOW MANY GLASSES OF LEMONADE TO MAKE (ONLY ONE BATCH IS MADE EACH MORNING)")
    print("2. HOW MANY ADVERTISING SIGNS TO MAKE (THE SIGNS COST FIFTEEN CENTS EACH) ")
    print("3. WHAT PRICE TO CHARGE FOR EACH GLASS ")
    print()
    print("YOU WILL BEGIN WITH $2.00 CASH (ASSETS).")
    print("BECAUSE YOUR MOTHER GAVE YOU SOME SUGAR,")
    print("YOUR COST TO MAKE LEMONADE IS TWO CENTS ")
    print("A GLASS (THIS MAY CHANGE IN THE FUTURE).")
    print()
    
    if not wait_for_continue():
        return False
    
    cls()
    print("YOUR EXPENSES ARE THE SUM OF THE COST OF")
    print("THE LEMONADE AND THE COST OF THE SIGNS. ")
    print()
    print("YOUR PROFITS ARE THE DIFFERENCE BETWEEN ")
    print("THE INCOME FROM SALES AND YOUR EXPENSES.")
    print()
    print("THE NUMBER OF GLASSES YOU SELL EACH DAY ")
    print("DEPENDS ON THE PRICE YOU CHARGE, AND ON ")
    print("THE NUMBER OF ADVERTISING SIGNS YOU USE.")
    print()
    print("KEEP TRACK OF YOUR ASSETS, BECAUSE YOU ")
    print("CAN'T SPEND MORE MONEY THAN YOU HAVE! ")
    print()
    
    return wait_for_continue()


def continue_game(n):
    """Get continuation data for an existing game"""
    cls()
    i = 0
    print("HI AGAIN! WELCOME BACK TO LEMONSVILLE! ")
    print()
    print("LET'S CONTINUE YOUR LAST GAME FROM WHERE")
    print("YOU LEFT IT LAST TIME. DO YOU REMEMBER ")
    print("WHAT DAY NUMBER IT WAS? ", end='')
    
    day = 0
    while True:
        response = input("")
        print()
        
        try:
            a = int(response)
            if 1 <= a <= 99:
                day = a
                break
        except ValueError:
            pass
        
        response = response.strip().upper()
        if response and response[0] == 'Y':
            print("GOOD! WHAT DAY WAS IT? ", end='')
            i += 1
            continue
        elif (response and response[0] == 'N') or i > 0:
            break
        else:
            print(chr(7), end='')
            print("YES OR NO? ", end='')
            i += 1
    
    print(f"OKAY - WE'LL START WITH DAY NO. {day + 1}")
    print()
    
    assets = []
    for i in range(n):
        print()
        print()
        print(f"PLAYER NO. {i + 1}, HOW MUCH MONEY (ASSETS)")
        print()
        print("DID YOU HAVE? ", end='')
        
        response = input("")
        print()
        
        try:
            a = float(response)
        except ValueError:
            a = 0
        
        if a < 2:
            print("O.K. - WE'LL START YOU OUT WITH $2.00")
            a = 2
        elif a > 40:
            print("JUST TO BE FAIR, LET'S MAKE THAT $10.00")
            a = 10
        
        assets.append(round(a * 100 + 0.5) / 100)
    
    print()
    print(chr(7), end='')
    ready = input("...READY TO BEGIN? ")
    if ready.strip().upper().startswith('N'):
        if not instructions():
            return None, None
    
    return day, assets


def weather_report(sc):
    """Display weather report"""
    cls()
    print("LEMONSVILLE WEATHER REPORT:")
    if sc == 2:
        print("  SUNNY")
    elif sc == 7:
        print("  HOT AND DRY")
    elif sc == 10:
        print("  CLOUDY")
    elif sc == 5:
        print("  THUNDERSTORMS!")
    print()


def daily_report(day, stand, n2, price, income, glasses_made, signs, expenses, profit, assets):
    """Display daily financial report for a stand"""
    print(f"DAY {day}  STAND {stand}")
    print()
    print()
    print(f"{n2} GLASSES SOLD")
    print()
    print(f"{format_money(price / 100)} PER GLASS, INCOME {format_money(income)}")
    print()
    print(f"{glasses_made} GLASSES MADE")
    print()
    print(f"{signs} SIGNS MADE, EXPENSES {format_money(expenses)}")
    print()
    print()
    print(f"PROFIT: {format_money(profit)}")
    print(f"ASSETS: {format_money(assets)}")
    print()
    wait_for_continue()


def main():
    """Main game loop"""
    # Constants
    P9 = 10  # Base price factor
    S3 = 0.15  # Sign cost
    S2 = 30  # Base sales factor
    A2 = 2.00  # Starting assets
    C9 = 0.5  # Sign effectiveness factor
    C2 = 1  # Advertisement multiplier
    
    introduction()
    
    while True:
        # Game setup
        new_game, n = title_page()
        
        # Initialize arrays for each stand
        assets = [0.0] * n
        lemonade = [0] * n
        high_temp = [0] * n  # Not used but kept for compatibility
        bankrupt = [0] * n
        signs = [0] * n
        price = [0] * n
        glasses_made = [0] * n
        
        day = 0
        
        # Initialize assets
        for i in range(n):
            bankrupt[i] = 0
            assets[i] = A2
        
        if new_game == 'Y':
            if not instructions():
                break
        else:
            day, loaded_assets = continue_game(n)
            if day is None:
                break
            assets = loaded_assets
        
        # Random event flags
        x1 = 0  # Rain event
        x2 = 0  # Street work event
        x3 = 0  # Thunderstorm event
        x4 = 0  # Heat wave event
        
        # Main game loop
        while True:
            # Weather report
            sc = random.random()
            if sc < 0.6:
                sc = 2  # Sunny
            elif sc < 0.8:
                sc = 10  # Cloudy
            else:
                sc = 7  # Hot and dry
            
            if day < 3:
                sc = 2
            
            weather_report(sc)
            
            cls()
            
            # Start of new day
            day += 1
            print(f"ON DAY {day}, THE COST OF LEMONADE IS ", end='')
            
            c = 2
            if day > 2:
                c = 4
            if day > 6:
                c = 5
            
            print(f"$.0{c}")
            print()
            
            c1 = c * 0.01
            r1 = 1  # Weather sales multiplier
            
            # Current events
            if day == 3:
                print("(YOUR MOTHER QUIT GIVING YOU FREE SUGAR)")
            
            if day == 7:
                print("(THE PRICE OF LEMONADE MIX JUST WENT UP)")
            
            # Random events after day 2
            if day > 2:
                if sc == 10:
                    if x1 != 1:
                        j = 30 + int(random.random() * 5) * 10
                        print(f"THERE IS A {j}% CHANCE OF LIGHT RAIN,")
                        print("AND THE WEATHER IS COOLER TODAY.")
                        r1 = 1 - j / 100
                        x1 = 1
                elif sc == 7:
                    if x4 != 1:
                        x4 = 1
                        print("A HEAT WAVE IS PREDICTED FOR TODAY!")
                        r1 = 2
                elif random.random() < 0.25:
                    if x2 != 1:
                        print("THE STREET DEPARTMENT IS WORKING TODAY.")
                        print("THERE WILL BE NO TRAFFIC ON YOUR STREET.")
                        if random.random() < 0.5:
                            r2 = 2  # Street crews will buy all lemonade
                        else:
                            r1 = 0.1
                        x2 = 1
            
            # Input values for each stand
            print()
            c5 = 0  # Change flag
            
            for i in range(n):
                assets[i] = assets[i] + 0.000000001  # Prevent exact zero
                glasses_made[i] = 1
                high_temp[i] = 0
                
                sti = format_money(assets[i])
                print(f"LEMONADE STAND {i + 1} ASSETS: {sti}")
                print()
                
                if bankrupt[i] != 0:
                    print("YOU ARE BANKRUPT, NO DECISIONS")
                    print("FOR YOU TO MAKE.")
                    if n == 1 and assets[0] < c:
                        break
                    continue
                
                while True:  # Loop for potential changes
                    # Get lemonade to make
                    while True:
                        print("HOW MANY GLASSES OF LEMONADE DO YOU")
                        print("WISH TO MAKE ", end='')
                        lemonade_val = get_integer("", 0, 1000)
                        if lemonade_val is None:
                            print("COME ON, LET'S BE REASONABLE NOW!!!")
                            print("TRY AGAIN")
                            continue
                        lemonade[i] = lemonade_val
                        
                        if lemonade[i] * c1 <= assets[i]:
                            break
                        
                        sti = format_money(assets[i])
                        print(f"THINK AGAIN!!! YOU HAVE ONLY {sti}")
                        print(f"IN CASH AND TO MAKE {lemonade[i]} GLASSES OF")
                        print(f"LEMONADE YOU NEED ${lemonade[i] * c1} IN CASH.")
                    
                    # Get signs to make
                    print()
                    while True:
                        print(f"HOW MANY ADVERTISING SIGNS ({S3 * 100:.0f} CENTS")
                        print("EACH) DO YOU WANT TO MAKE ", end='')
                        signs_val = get_integer("", 0, 50)
                        if signs_val is None:
                            print("COME ON, BE REASONABLE!!! TRY AGAIN.")
                            continue
                        signs[i] = signs_val
                        
                        if signs[i] * S3 <= assets[i] - lemonade[i] * c1:
                            break
                        
                        print()
                        sti = format_money(assets[i] - lemonade[i] * c1)
                        print(f"THINK AGAIN, YOU HAVE ONLY {sti}")
                        print("IN CASH LEFT AFTER MAKING YOUR LEMONADE.")
                    
                    # Get price
                    print()
                    print("WHAT PRICE (IN CENTS) DO YOU WISH TO")
                    print("CHARGE FOR LEMONADE ", end='')
                    price_val = get_integer("", 0, 100)
                    if price_val is None:
                        print("COME ON, BE REASONABLE!!! TRY AGAIN.")
                        continue
                    price[i] = price_val
                    
                    if c5 == 1:
                        break
                    
                    # Ask if they want to change anything
                    response = input("WOULD YOU LIKE TO CHANGE ANYTHING?")
                    if response.strip().upper().startswith('Y'):
                        c5 = 1
                        continue
                    break
                
                cls()
            
            c5 = 0
            cls()
            
            # Check for thunderstorm
            if sc == 10 and random.random() < 0.25:
                x3 = 1
                r3 = 0
                sc = 5
                weather_report(sc)
                cls()
                print("WEATHER REPORT: A SEVERE THUNDERSTORM")
                print("HIT LEMONSVILLE EARLIER TODAY, JUST AS")
                print("THE LEMONADE STANDS WERE BEING SET UP.")
                print("UNFORTUNATELY, EVERYTHING WAS RUINED!!")
                for j in range(n):
                    glasses_made[j] = 0
            
            print()
            
            # Check for street crew event
            r2 = 0
            if 'r2' in locals() and r2 == 2:
                print("THE STREET CREWS BOUGHT ALL YOUR")
                print("LEMONADE AT LUNCHTIME!!")
            
            print("** LEMONSVILLE DAILY FINANCIAL REPORT **")
            
            # Calculate profits for each stand
            for i in range(n):
                if assets[i] < 0:
                    assets[i] = 0
                
                if 'r2' in locals() and r2 == 2:
                    n2 = lemonade[i]
                elif x3 == 1:
                    n2 = 0
                else:
                    # Calculate sales based on price and advertising
                    if price[i] >= P9:
                        n1 = (P9 ** 2) * S2 / (price[i] ** 2)
                    else:
                        n1 = (P9 - price[i]) / P9 * 0.8 * S2 + S2
                    
                    w = -signs[i] * C9
                    v = 1 - (math.exp(w) * C2)
                    n2 = r1 * (n1 + (n1 * v))
                    n2 = int(n2 * glasses_made[i])
                    
                    if n2 > lemonade[i]:
                        n2 = lemonade[i]
                
                # Calculate finances
                m = n2 * price[i] * 0.01  # Income
                e = signs[i] * S3 + lemonade[i] * c1  # Expenses
                p1 = m - e  # Profit
                assets[i] = assets[i] + p1
                
                if high_temp[i] == 1:
                    continue
                
                print()
                
                if bankrupt[i] == 1:
                    print(f"STAND {i + 1} BANKRUPT")
                    if not wait_for_continue():
                        break
                    continue
                
                daily_report(day, i + 1, n2, price[i], m, lemonade[i], signs[i], e, p1, assets[i])
                
                if assets[i] <= c / 100:
                    print(f"STAND {i + 1}")
                    print(" ...YOU DON'T HAVE ENOUGH MONEY LEFT")
                    print(" TO STAY IN BUSINESS YOU'RE BANKRUPT!")
                    bankrupt[i] = 1
                    if not wait_for_continue():
                        break
                    cls()
                    if n == 1 and bankrupt[0] == 1:
                        break
            
            # Check if all players are bankrupt
            if n == 1 and bankrupt[0] == 1:
                break
            
            # Reset for next day
            r1 = 1
            r2 = 0
            if 'r2' in locals():
                del r2
        
        # End of game
        cls()
        print("WOULD YOU LIKE TO PLAY AGAIN? ", end='')
        try:
            if sys.platform == 'win32':
                import msvcrt
                response = msvcrt.getch()
                if response == b'Y' or response == b'y':
                    continue
            else:
                import termios
                import tty
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    response = sys.stdin.read(1)
                    if response.upper() == 'Y':
                        continue
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            response = input()
            if response.strip().upper().startswith('Y'):
                continue
        
        cls()
        break


if __name__ == "__main__":
    main()
