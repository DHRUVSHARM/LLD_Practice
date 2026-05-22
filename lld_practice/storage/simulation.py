# file storage design 
# level 1 done
# level 2 done 
# level 3 done
# level 4 done

from typing import NamedTuple

class FileBackup(NamedTuple):
    name:str
    size:int

class User:
    def __init__(self , user_id, capacity=None):
        self.user_id = user_id
        self.capacity = capacity
        self.files : list[str] = [] # can be list of file id to lookup files owned by this user 
        self.backup : list[FileBackup] = [] # will store the latest backup 

class File:
    def __init__(self , name , size, owner="admin"):
        self.name = name
        self.size = size
        self.owner = owner # user id of owner to lookup in users dict 

class Simulation:
    def __init__(self):
        self.files : dict[str, File] = {}
        self.users : dict[str , User] = {}

    def add_file(self, name:str, size:int) -> str:
        # add a file with the given name and size 
        if name in self.files:
            return "false"
        
        new_file = File(name , size)
        self.files[name] = new_file
        return "true"

    def get_file_size(self, name:str) -> str:
        # return file size if name in storage 
        if name not in self.files:
            return ""
        
        return str(self.files[name].size)

    def delete_file(self, name:str)->str:
        # return deleted file size as a string 
        if name not in self.files:
            return ""
        
        deleted_size = self.files[name].size
        if self.files[name].owner in self.users:
            self.users[self.files[name].owner].capacity += deleted_size
            self.users[self.files[name].owner].files.remove(name)

        self.files.pop(name)
        
        return str(deleted_size)

    def get_n_largest(self, prefix:str , n):
        # sort by the size desc, name asc
        files_sorted = sorted(self.files.items(), key=lambda element : (-element[1].size , element[0]))
        count = 0
        result = []
        for file_name, file in files_sorted:
            if file_name.startswith(prefix):
                result.append(f"{file_name}({file.size})")
                count += 1
                if count == n:
                    break
        return "" if len(result) == 0 else ", ".join(result)
    

    def add_user(self, user_id, capacity):
        # add user with a capacity 
        if user_id in self.users:
            return "false"

        new_user = User(user_id , capacity)
        self.users[user_id] = new_user
        return "true"
    
    def add_file_by(self, user_id, name, size):
        # add file owned by user_id
        if user_id not in self.users or name in self.files:
            return ""
        
        # check if exceed capacity 
        if self.users[user_id].capacity < size:
            return ""
        
        # we cannot take older file that does not have valid capacity so None checked is skipped here 
        # has to be a new file created and user_id has to be in users, so we think admin user will not be used here ?

        new_file = File(name, size, user_id)
        self.files[name] = new_file
        self.users[user_id].capacity -= size
        self.users[user_id].files.append(name)
        

        return str(self.users[user_id].capacity)
    
    def merge_user(self, user_id_1, user_id_2):
        if user_id_1 not in self.users or user_id_2 not in self.users or user_id_1 == user_id_2:
            return ""
        
        # merge id1 <--- id2
        # 2 valid capacities so should not affect, no need to pop 
        for file_id in self.users[user_id_2].files:
            self.users[user_id_1].files.append(file_id)
            self.files[file_id].owner = user_id_1
        
        self.users[user_id_1].capacity += self.users[user_id_2].capacity # add remaining capacity, repr state transfer 

        self.users.pop(user_id_2) # remove user 
        return str(self.users[user_id_1].capacity)


    def backup_user(self, user_id):
        # store latest backup at this point
        if user_id not in self.users:
            return ""
        
        # backup will need to store file objects for reconstruction 
        # also backup state should be diff than the file state
        # file state may change in the future wrongly reflecting here 
        self.users[user_id].backup = [FileBackup(self.files[file_id].name , self.files[file_id].size) for file_id in self.users[user_id].files] # store a copy 
        return str(len(self.users[user_id].backup))

    def restore_user(self, user_id):
        # restore from latest backup 
        # delete all files stored by this user from global storage also 
        # add new caps accordingly since now we are not storing these files, all files owned can be removed easily 
        # restore from backup
        # some files can be now in global via some other user (cannot happen that one file has more than one user due to add constraints)
        # so in that case we skip again respecting the single owner thing for files 
        # others add and remove the capacity accordingly 
        # since capacity can only increase via merging
        # and capacity never < 0 while adding and 2 accounts merging will also respect that constraint since rem capacities are getting added
        # we may say that backup, which is a snapshot of the past will never cause capacity < 0 
        if user_id not in self.users:
            return ""
        
        for file_id in self.users[user_id].files:
            file_obj = self.files.pop(file_id)    # remove from global storage
            self.users[user_id].capacity += file_obj.size # add removed size to remaining capacity 


        self.users[user_id].files = [] # reset owned files 

        # restore from backup 
        for file_backup_obj in self.users[user_id].backup:
            if file_backup_obj.name not in self.files:
                # deleted filed not owned by any other
                new_file = File(file_backup_obj.name, file_backup_obj.size , user_id)
                self.files[file_backup_obj.name] = new_file
                self.users[user_id].files.append(new_file.name)
                self.users[user_id].capacity -= file_backup_obj.size

        return str(len(self.users[user_id].files))

        