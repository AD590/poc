
"""
Cookie Clicker Simulator
"""
import simpleplot
 
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(10)

import poc_clicker_provided as provided
import math

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_produced = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0,None,0.0,0.0)]
    def __str__(self):
        """
        Return human readable state
        """
        str1 = '\nTime:\t\t\t' + str(self._current_time) + '\n'
        str2 = 'Current cookies:\t' + str(self._current_cookies) + '\n'
        str3 = 'CPS:\t\t\t' + str(self._current_cps) + '\n'
        str4 = 'Total cookies:\t\t' + str(self._total_cookies_produced) + '\n'
        return str1 + str2 + str3 + str4
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
    
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        return max(0.0, math.ceil((cookies - self._current_cookies) / self._current_cps))
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_time += time
            cookies_produced = time * self._current_cps
            self._current_cookies += cookies_produced
            self._total_cookies_produced += cookies_produced
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies_produced))
            
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    build = build_info.clone()
   # print build.build_items()
    state = ClickerState()
    while state.get_time() < duration:
        item = strategy(state.get_cookies(), state.get_cps(), duration - state.get_time(), build)
        if item == None:
            break
        item_cost = build.get_cost(item)
        item_additional_cps = build.get_cps(item)
        time = state.time_until(item_cost)
        if (state.get_time() + time) > duration:
            break
        else:
            state.wait(time)
            state.buy_item(item,item_cost,item_additional_cps)
            build.update_item(item)
    state.wait(duration - state.get_time())   
    item = strategy(state.get_cookies(), state.get_cps(), 0.0, build)
     
    while(item != None and state.get_cookies() >= build.get_cost(item)):
        state.buy_item(item, build.get_cost(item), build.get_cps(item))
        build.update_item(item)
        item = strategy(state.get_cookies(), state.get_cps(), 0.0, build)
    return state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    return the cheapest item afforded or will be afforded in time ('time_left') with constant producing rate 'cps'
    """
    
    item_list = build_info.build_items()
    cost = float('inf')
    for item in item_list:
       # print item, build_info.get_cost(item), cost
        if build_info.get_cost(item) < cost:
            cost = build_info.get_cost(item)
            cheapest_item = item
    if cookies + cps * time_left >= cost: 
        return cheapest_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    return the most expensive item afforded or will be afforded in time ('time_left') with constant producing rate 'cps'  
    """
    item_list = build_info.build_items()
    cost = float('-inf')
    expensive_item = None
    afford_cost = cookies + cps * time_left
    for item in item_list:
        item_cost = build_info.get_cost(item)
        if item_cost <= afford_cost and item_cost >= cost:
            expensive_item = item
            cost = item_cost
    return expensive_item

def strategy_best(cookies, cps, time_left, build_info):
    """
    return the afforded item will make the most cookies in time ('time left')
    """
    item_list = build_info.build_items()
    best_item = None
    most_extra_cookies = float('-inf')
    cps_acceleration = float('-inf')
    for item in item_list:
        item_cost = build_info.get_cost(item)
        item_additional_cps = build_info.get_cps(item)
        afford_time = min(time_left, max(0,(item_cost - cookies) / cps))
        extra_cookies = (time_left - afford_time) * item_additional_cps 
        if extra_cookies > most_extra_cookies and extra_cookies > 0 and item_additional_cps / item_cost  > cps_acceleration:
            most_extra_cookies = extra_cookies
            cps_acceleration = item_additional_cps / item_cost
            best_item = item
    
    return best_item

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #item = [item[1] for item in history]
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

    
run()

