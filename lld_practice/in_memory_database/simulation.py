# in memory db 
"""
for each record : 
key -> field -> value
database = {
    "user1": {
        "name": "Dhruv",
        "age": "25"
    }
}
"""

class Simulation:
    def __init__(self):
        self.db = {}
        self.backups = {} # maps the timestamp : keys : fields : remaining ttl 
        """
        backups[timestamp] = {
            key1: [value, remaining ttl],
            key2 : [value, remaining, ttl]
        }
        
        """

    def set(self, key, field, value):
        if key not in self.db:
            self.db[key] = {}
        
        self.db[key][field] = [value , None, None]
        return ""

    def get(self, key, field):
        if key not in self.db or field not in self.db[key]:
            return ""
        
        return self.db[key][field][0]

    def delete(self, key, field):
        # delete the field , from the record 
        if key not in self.db or field not in self.db[key]:
            return "false"

        self.db[key].pop(field)
        return "true"
    
    def scan(self, key):
        # return all fields for a key sort, lexicographically by the field name 
        if key not in self.db:
            return ""
        
        res = sorted(self.db[key].items() , key=lambda x : (x[0]))
        return ", ".join([f"{field_name}({value[0]})" for field_name, value in res]) if len(res) else ""

    def scan_by_prefix(self, key, prefix):
        if key not in self.db:
            return ""

        res = []
        for field_name , value in self.db[key].items():
            if field_name.startswith(prefix):
                res.append((field_name , value[0]))
        
        res.sort()
        return ", ".join([f"{field_name}({value})" for field_name, value in res]) if len(res) else ""
    
    """
    reverse mapping timestamp : {
        key : {field : value}
    }

    # for tracking expiry 
    add the expiry date 
    # can maintain active dictionary

    active : {(key , field, value)}

    older values can have very long expiry 
    set None to indicate 

    """

    def set_at(self, timestamp, key, field, value):
        # set a entry with a timestamp but does not expire  
        if key not in self.db:
            self.db[key] = {}

        self.db[key][field] = [value , timestamp , None] # append [l , h) 
        return ""

    def set_at_with_ttl(self, timestamp, key, field, value, ttl):
        # set a entry with timestamp + ttl expiry
        if key not in self.db:
            self.db[key] = {}
        
        self.db[key][field] = [value , timestamp , timestamp + ttl] # [l , h)
        return ""

    def get_at(self, timestamp, key, field):
        # returns the field value at the timestamp 
        if key not in self.db or field not in self.db[key]:
            return ""
        
        value, time , ttl = self.db[key][field]
        if time is None:
            return value
        
        if ttl is None:
            return value
        
        return value if time <= timestamp < ttl else ""
    
    """
    delete_at(timestamp, key, field)
    scan_at(timestamp, key)
    scan_by_prefix_at(timestamp, key, prefix)
    """

    def delete_at(self, timestamp, key, field):
        if key not in self.db or field not in self.db[key]:
            return "false"
        
        value, time, expiry = self.db[key][field]
        if time is None or expiry is None:
            self.db[key].pop(field)
            return "true"
        
        if time <= timestamp < expiry:
            self.db[key].pop(field)
            return "true"
        else:
            return "false"

    def scan_at(self, timestamp , key):
        # return all fields for a key sort, lexicographically by the field name 
        if key not in self.db:
            return ""
        
        res = []
        for field_name, details in self.db[key].items():
            value , time, expiry = details
            if time is None or expiry is None:
                res.append((field_name , value))
            elif time <= timestamp < expiry:
                res.append((field_name , value))

        res.sort()
        return ", ".join([f"{field_name}({value})" for field_name, value in res]) if len(res) else ""
    

    def scan_by_prefix_at(self, timestamp, key , prefix):
        # return all fields for a key sort, lexicographically by the field name 
        if key not in self.db:
            return ""
        
        res = []
        for field_name, details in self.db[key].items():
            if not field_name.startswith(prefix):
                continue
            
            value , time, expiry = details
            if time is None or expiry is None:
                res.append((field_name , value))
            elif time <= timestamp < expiry:
                res.append((field_name , value))

        res.sort()
        return ", ".join([f"{field_name}({value})" for field_name, value in res]) if len(res) else ""

    
    def backup(self, timestamp):
        # return the number of keys that have at least one alive field in the backup 
        
        """
        backups[timestamp] = {
            key1: {
                f1 : [value, remaining ttl],
                f2 : [value, remaining_ttl]
            },
        }
        
        """
        if timestamp not in self.backups:
          
            self.backups[timestamp] = {}    
    
            for key in self.db.keys():
                

                for field_name, details in self.db[key].items():
                    value, time, expiry = details
                    # put in if the field is alive
                    if time is None or expiry is None or expiry - timestamp > 0:
                    
                        if key not in self.backups[timestamp]:
                            self.backups[timestamp][key] = {}

                        self.backups[timestamp][key][field_name] = [value , (expiry - timestamp) if time is not None and expiry is not None else None]

        alive_count = 0
        for k in self.backups[timestamp]:
            if len(self.backups[timestamp][k].values()) > 0:
                alive_count += 1

        return alive_count


    def restore(self, timestamp , timestamp_to_restore):
        # restore at <= timestamp_to_restore, closest to it from left 
        # and 
        backup_timestamp = -1
        for t in sorted(self.backups.keys()):
            if t > timestamp_to_restore:
                break
            backup_timestamp = t
        
        if backup_timestamp == -1:
            # go back to empty 
            self.db = {}
            return ""
        
        # we need to restore db to the backup_timestamp
        # backups gives the keys that are not expired with remaining ttl 
        # easiest way is to do full overwrite

        backup_db = self.backups[backup_timestamp]
        self.db = {}

        for key, field_details in backup_db.items():
            if key not in self.db:
                self.db[key] = {}
            for field_name, field_value in field_details.items():
                value, remaining_ttl = field_value
                self.db[key][field_name] = [value , timestamp , timestamp + remaining_ttl if remaining_ttl is not None else None]

        return ""        
