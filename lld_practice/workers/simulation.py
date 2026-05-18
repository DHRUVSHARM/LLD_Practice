# workers system
# people management system 
# level 1 done
# level 2 done 

class Worker:
    def __init__(self, worker_id:str, position:str, compensation:int):
        self.worker_id = worker_id
        self.position = position
        self.compensation = compensation

        self.in_office = False # currently not in office
        self.entry_time = None # entry time set when in office is true 
        self.total_time = 0 # total to calculate comp , added when leaving office 


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
            # need to exit
            self.workers[worker_id].in_office = False
            self.workers[worker_id].total_time += (timestamp - self.workers[worker_id].entry_time)
            self.workers[worker_id].entry_time = None
        else:
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