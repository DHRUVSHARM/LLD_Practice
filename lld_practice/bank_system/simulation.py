"""
All your implementation code for the bank system simulation goes here.
"""


"""
level 1 - done
level 2 - done
level 3 - done
level 4 - pass
"""



# for managing the account 
class Account:
    def __init__(self, account_id):
        self.account_id:str = account_id
        self.balance:int = 0
        self.outgoing:int = 0 # outgoing money from the account 
        self.payments:dict[str , str] = {} # map the payment id to the amount 
        # to get the payments associated within an account we can do obj.payments[payment_id] = status
        
        # self.balance_history:dict[int , int] = {} # historic balance is 0
        # will move the balance history to a global one 

class Simulation:
    def __init__(self):
        self.accounts: dict[str , Account] = {}
        self.payment_count = 0
        self.pending_cashbacks = []
        # cashback need to be applied at scheduled time, account_id(to reduce), payment_id(to change status) , cashback_amtzs
        self.cashback_delay = 86400000
        self.history = {} # history[accountid][timestamp] = balance # will store older active, inactive accounts and None after merge (removal)
        
    def create_account(self, timestamp, account_id):
        # create a new account with balance 0 
        self._process_cashback(timestamp)

        if account_id in self.accounts:
            return False
        account = Account(account_id)
        self.accounts[account_id] = account
        # record balance
        # self.accounts[account_id].balance_history[timestamp] = 0 # first entry is 0 
        if account_id not in self.history:
            # only create if not present
            self.history[account_id] = {}
        
        self.history[account_id][timestamp] = self.accounts[account_id].balance
        
        return True

    def deposit(self, timestamp, account_id, amount):
        self._process_cashback(timestamp)

        if account_id not in self.accounts:
            return None
        self.accounts[account_id].balance += amount

        # record balance 
        self.history[account_id][timestamp] = self.accounts[account_id].balance
        
        return self.accounts[account_id].balance

    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        self._process_cashback(timestamp)

        if source_account_id not in self.accounts or target_account_id not in self.accounts or source_account_id == target_account_id:
            return None

        if self.accounts[source_account_id].balance - amount < 0 :
            return None
        
        # can move
        self.accounts[source_account_id].outgoing += amount
 
        self.accounts[source_account_id].balance -= amount
        self.accounts[target_account_id].balance += amount


        # update record  for both 
        # self.accounts[source_account_id].balance_history[timestamp] = self.accounts[source_account_id].balance
        self.history[source_account_id][timestamp] = self.accounts[source_account_id].balance
        # self.accounts[target_account_id].balance_history[timestamp] = self.accounts[target_account_id].balance
        self.history[target_account_id][timestamp] = self.accounts[target_account_id].balance

        return self.accounts[source_account_id].balance
        # not this returned is the money that is left in the source account after transfer
        

    def top_spenders(self, timestamp , n)->list[str]:
        self._process_cashback(timestamp)
        # return the top n accounts ranked by outgoing money (need to keep track from transfer)
        # ["account2(300)", "account1(100)"] , decreasing by ammount, then account id 
        result = sorted(self.accounts.items() , key=lambda x : (-x[1].outgoing , x[0]))[:n]
        ans = []
        for id , obj in result:
            ans.append(f"{id}({obj.outgoing})")

        return ans        
    
    def _process_cashback(self, timestamp):
        # remove and process all the cashbacks till <= timestamp
        # easisest would be to make a copy
        remaining = []
        for time, account_id, payment_id, cashback in self.pending_cashbacks:
            if time <= timestamp:
                # apply
                self.accounts[account_id].balance += cashback
                # self.accounts[account_id].balance_history[time] = self.accounts[account_id].balance 
                self.history[account_id][time] = self.accounts[account_id].balance
                self.accounts[account_id].payments[payment_id] = "CASHBACK_RECEIVED"
            else:
                # add to remaining 
                remaining.append([time, account_id, payment_id, cashback])
        self.pending_cashbacks = remaining


    def pay(self, timestamp, account_id, amount):
        # withdraw amount from account , and payment id to be returned 
        # if no account or insufficient funds return None
        # we will keep global counter to generate the id 
        
        self._process_cashback(timestamp)
        if account_id not in self.accounts or self.accounts[account_id].balance - amount < 0:
            return None # failed 
        
        self.accounts[account_id].balance -= amount # remove from the account 
        # self.accounts[account_id].balance_history[timestamp] = self.accounts[account_id].balance
        self.history[account_id][timestamp] = self.accounts[account_id].balance
        self.accounts[account_id].outgoing += amount # outgoing add

        self.payment_count += 1
        payment_id = f"payment{self.payment_count}"
        self.accounts[account_id].payments[payment_id] = "IN_PROGRESS"

        # schedule cashback 
        # cashback need to be applied at scheduled time, account_id(to reduce), payment_id(to change status) , cashback_amt
        self.pending_cashbacks.append([timestamp + self.cashback_delay , account_id , payment_id , (amount * 2) // 100])

        return payment_id


    def get_payment_status(self, timestamp, account_id, payment_id):
        self._process_cashback(timestamp)
        if account_id not in self.accounts:
            return None
        
        if payment_id not in self.accounts[account_id].payments:
            return None
        
        return self.accounts[account_id].payments[payment_id] # get status if exists 
    

    def merge_accounts(self, timestamp, account_id_1 , account_id_2):
        self._process_cashback(timestamp)
        
        if account_id_1 not in self.accounts or account_id_2 not in self.accounts or account_id_1 == account_id_2:
            return False
        
        # can merge the accounts 
        # account id1 to account id2
        self.accounts[account_id_1].balance += self.accounts[account_id_2].balance
        # self.accounts[account_id_1].balance_history[timestamp] = self.accounts[account_id_1].balance
        self.history[account_id_1][timestamp] = self.accounts[account_id_1].balance

        self.accounts[account_id_1].outgoing += self.accounts[account_id_2].outgoing
        
        # pending payments should be put in the current account 
        payments_2 = self.accounts[account_id_2].payments 
        for p_id, status in payments_2.items():
            self.accounts[account_id_1].payments[p_id] = status

        # edit the pending cashbacks
        # cashback need to be applied at scheduled time, account_id(to reduce), payment_id(to change status) , cashback_amt
        for index, element in enumerate(self.pending_cashbacks):
            t , aid, pid, amt = element
            if aid == account_id_2:
                self.pending_cashbacks[index][1] = account_id_1 # assign to account 1

        # also add to the pending cashbacks by noting time, actually no need it is centrally managed already 
        # remove the account 
        self.history[account_id_2][timestamp] = None
        self.accounts.pop(account_id_2)
         

        return True



    def get_balance(self, timestamp , account_id, time_at):
        self._process_cashback(timestamp)
        if account_id not in self.history or time_at < 0:
            return None

        # record_times = sorted(self.accounts[account_id].balance_history.items())
        record_times = sorted(self.history[account_id].items())
        # (time, balance)

        if time_at < record_times[0][0]:
            return None
        
        prev , index = 0 , 1
        while index < len(record_times) and record_times[index][0] <= time_at:
            prev, index = index, index + 1
        
        # we are at end and the index is storing greater value than timeat
        return record_times[prev][1]
