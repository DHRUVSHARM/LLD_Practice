# file storage design 
# level 1 done
# level 2 done 

class Simulation:
    def __init__(self):
        self.files : dict[str, int] = {}

    def add_file(self, name:str, size:int) -> str:
        # add a file with the given name and size 
        if name in self.files:
            return "false"
        self.files[name] = size
        return "true"

    def get_file_size(self, name:str) -> str:
        # return file size if name in storage 
        if name not in self.files:
            return ""
        return str(self.files[name])

    def delete_file(self, name:str)->str:
        # return deleted file size as a string 
        if name not in self.files:
            return ""
        
        deleted_size = self.files[name]
        self.files.pop(name)
        return str(deleted_size)

    def get_n_largest(self, prefix:str , n):
        # sort by the size desc, name asc
        files_sorted = sorted(self.files.items(), key=lambda element : (-element[1] , element[0]))
        count = 0
        result = []
        for file_name, file_size in files_sorted:
            if file_name.startswith(prefix):
                result.append(f"{file_name}({file_size})")
                count += 1
                if count == n:
                    break
        return "" if len(result) == 0 else ", ".join(result)