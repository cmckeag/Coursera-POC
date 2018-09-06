"""
Cookie Clicker Simulator
Doesn't actually run but the logic is mostly sound I think
"""

import random


# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Total cookies: " + str(self._total_cookies) + "current cookies: " + str(self._current_cookies) + "total time: " + str(self.get_time()) + "CPS: " + str(self.get_cps())
        
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
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        diff = cookies - self._current_cookies
        if diff <= 0:
            return 0.0
        return diff / self._cps
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        self._time += time
        self._current_cookies += time * self._cps
        self._total_cookies += time * self._cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies < cost:
            return
        self._current_cookies -= cost
        self._history.append((self._time, item_name, cost, self._total_cookies))
        self._cps += additional_cps
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    build = build_info.clone()
    clicker = ClickerState()
    while clicker.get_time() <= duration:
        item = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), duration - clicker.get_time(), build)
        if item is None:
            clicker.wait(duration - clicker.get_time())
            break
        item_cost = build.get_cost(item)
        wait_time = (item_cost - clicker.get_cookies()) / clicker.get_cps()
        if wait_time > duration - clicker.get_time():
            clicker.wait(duration - clicker.get_time())
            break
        clicker.wait(wait_time)
        old_cookies = clicker.get_cookies()
        clicker.buy_item(item, item_cost, build.get_cps(item))
        if clicker.get_cookies() != old_cookies:
            build.update_item(item)
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    potential_items = build_info.build_items()
    costs = [build_info.get_cost(item) for item in potential_items]
    potential_cookies = cookies + cps*time_left
    if min(costs) > potential_cookies:
        return None
    return potential_items[costs.index(min(costs))]


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    potential_items = build_info.build_items()
    costs = [build_info.get_cost(item) for item in potential_items]
    potential_cookies = cookies + cps*time_left
    if min(costs) > potential_cookies:
        return None
    items_actual = [potential_items[idx] for idx in range(len(costs)) if costs[idx] <= potential_cookies]
    costs_actual = [costs[idx] for idx in range(len(costs)) if costs[idx] <= potential_cookies]
    return items_actual[costs_actual.index(max(costs_actual))]

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    
    Just picks a random item from the list of items that you
    can afford with the time remaining.
    60% of the time it works all the time.
    """
    potential_items = build_info.build_items()
    costs = [build_info.get_cost(item) for item in potential_items]
    potential_cookies = cookies + cps*time_left
    if min(costs) > potential_cookies:
        return None
    items_actual = [potential_items[idx] for idx in range(len(costs)) if costs[idx] <= potential_cookies]
    return items_actual[random.randint(0, len(items_actual)-1)]
    
    

