import time

class MyTimer():
    def __init__(self, period=1, num_states=2, init_state=0, auto_refresh=False):
        """return a my_timer object
period: a float, time in seconds after refresh when passes will return True
num_states: a non-negative interger, number of different states the timer can have
init_stats: a non-negative interger, the initial state of the timer
auto_refresh: a boolean, if True, .get_states will automatically call the refresh function if .passed() is True"""
        self.time = 0.0
        self.period = period
        self.num_states = num_states
        self.state = init_state
        self.auto_refresh = auto_refresh

    def passed(self):
        """return true if the time difference between now and time of last
refresh is longer than self.period"""
        if time.time() - self.time > self.period:
            return True
        else:
            return False

    def refresh(self, new_period=None):
        self.time = time.time()
        self.state += 1
        if self.state >= self.num_states:
            self.state = 0
        if new_period != None:
            self.period = new_period

    def getState(self):
        if self.auto_refresh:
            if self.passed():
                self.refresh()
        return self.state
