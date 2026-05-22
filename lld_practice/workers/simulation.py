# workers system
# people management system 
# level 1 done
# level 2 done 
# level 3 done 

from dataclasses import dataclass
from typing import Optional

@dataclass
class Promotion:
    position:str
    compensation:int
    start_timestamp:int

@dataclass
class Session:
    start:int
    end:int
    compensation:int


class Worker:
    def __init__(self, worker_id:str, position:str, compensation:int):
        self.worker_id = worker_id
        self.position = position
        self.compensation = compensation

        self.in_office = False # currently not in office
        self.entry_time = None # entry time set when in office is true 
        self.total_time = 0 # total to calculate comp , added when leaving office 

        self.promotion:None|Promotion = None # means no pending promotion , # if promotion, then we store as a tuple of (position, timestamp, new_comp)
        # sessions is a running log connected to a worker 
        self.sessions:list[Session] = []


class Simulation:
    def __init__(self):
        self.workers : dict[str, Worker] = {}
    
    def add_worker(self, worker_id:str, position:str, compensation:int):
        if worker_id in self.workers:
            return "false" # already existss
        new_worker = Worker(worker_id , position , compensation)
        self.workers[worker_id] = new_worker
        return "true"

    def register(self, worker_id:str, timestamp:int):
        """
        register a worker for entering or leaving the office
        if not in office , entering mark the enter timestamp 
        if in office, exiting  , calculated total time and it
        assuming timestamps are valid like >= last recorded entry time 
        """
        if worker_id not in self.workers:
            return "invalid_request"
        
        if self.workers[worker_id].in_office:
            # in office, need to exit
            # here we can also record the session since at this time we know for [entry_time, timestamp) we have compensation 
            # can be used to back calculate the comp as a session 
            # we only need to record completed sessions, and since there can be overlaps, that is why we are not 
            # storing the total time naively

            self.workers[worker_id].sessions.append(Session(self.workers[worker_id].entry_time , timestamp , self.workers[worker_id].compensation))
            self.workers[worker_id].in_office = False
            self.workers[worker_id].total_time += (timestamp - self.workers[worker_id].entry_time)
            self.workers[worker_id].entry_time = None
            

        else:
            # out of office need to enter
            if self.workers[worker_id].promotion is not None and timestamp >= self.workers[worker_id].promotion.start_timestamp:
                # apply promotion on this entry 
                self.workers[worker_id].position = self.workers[worker_id].promotion.position
                self.workers[worker_id].compensation = self.workers[worker_id].promotion.compensation
                # clear promotion pending 
                self.workers[worker_id].promotion = None

            self.workers[worker_id].in_office = True
            self.workers[worker_id].entry_time = timestamp

        return "registered"


    def get(self, worker_id:str):
        if worker_id not in self.workers:
            return ""
        return str(self.workers[worker_id].total_time)
    

    def top_n_workers(self, n, position):
        """
        It returns the top n workers with the given position, ranked by total completed time in office.
        """
        sorted_workers = sorted(self.workers.items() , key = lambda x : (-x[1].total_time , x[0]))
        # for same total time and positon, tie break by asc worker id 

        res = []
        for worker_id, worker in sorted_workers:
            if worker.position == position:
                res.append(f"{worker_id}({worker.total_time})")
                if len(res) == n:
                    break

        return "" if len(res) == 0 else ", ".join(res)
    
    def promote(self, worker_id:str, new_position:str, new_compensation:int, start_timestamp:int):
        # promotion is always applied at a new entry >= start_timestamp
        # if worker not exists or promotion already scheduled, reject 
        if worker_id not in self.workers or self.workers[worker_id].promotion is not None:
            # invalid if promotion already scheduled, we can couple it to the worker 
            return "invalid_request"
        
        # will be applied the next time we enter with >= start_timestamp
        self.workers[worker_id].promotion = Promotion(new_position , new_compensation , start_timestamp)

        return "success"

    def calc_salary(self, worker_id:str, start_timestamp:int, end_timestamp:int):
        # this will calculate the salary earned by worker in the interval given 
        # will need to store a log of the salary earned for this 
        if worker_id not in self.workers:
            return ""
        
        total_comp = 0
        """
        s           e
            s1          e1

        s           e
            s1e1
        """
        for session in self.workers[worker_id].sessions:
            # need to consider overlaps 
            if session.end <= start_timestamp or session.start >= end_timestamp:
                # no overlap 
                continue
            new_start = max(session.start , start_timestamp)
            new_end = min(session.end, end_timestamp)

            total_comp += (new_end - new_start) * session.compensation

        return str(total_comp)