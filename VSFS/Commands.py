#!/usr/bin/python3
import sys
import os
import time
import subprocess
from pathlib import Path

_OPERATION = 1
_FILESYSTEM = 2
# List of valid operations
_OPERATIONS = [
    "list","copyin","copyout","mkdir",
    "rm", "rmdir", "defrag", "index"
]

class VSFSCommands:
 
    # Prints errors using stderr
    def print_stderr(self, *error):
        print(*error, file = sys.stderr)


    # Verifies if the entered operation is valid
    def check_operation(self, operation):
        try:
            _OPERATIONS.index(operation)
        except ValueError:
            self.print_stderr("Invalid VSFS: Operation Not Found")
            exit(1)
        else:
            return True


    # Verifies if the entered File System is valid
    def check_file_system(self, file_system):
        extension = ".notes"

        # Checking if FS exists
        try:
            with open(file_system, "r") as f:
                pass
        except FileNotFoundError:
            self.print_stderr("Invalid VSFS: File System Not Found")
            exit(1)
        else:
            if extension in file_system:
                # Checking if first line is "NOTES V1.0"
                with open(file_system, "r") as f:
                    first_line = f.readline().rstrip()
                    if (first_line == "NOTES V1.0"):
                        return True
                    else:
                        self.print_stderr("Invalid VSFS: File System Is Not Valid")
                        exit(1)


    # Verifies if the entered Internal File path is valid
    def check_internal_file(self, internal_file, file_system):
        # Checking if IF ends or starts with "/" or
        # if it is ".", "..", or "/"
        wrong_if = (internal_file[len(internal_file) - 1] == "/" 
                    or internal_file[0] == "/" 
                    or internal_file == "." 
                    or internal_file == ".."
                    or internal_file == "/")

        if (wrong_if == False):
            s = internal_file
            l = s.split('/')
            # Checking if the path provided exists
            if (len(l) > 1):
                i = 0
                dir = l[i]
                while(i != len(l)-1):
                    index = self.check_internal_directory(dir, file_system)[0]
                    if (index == -1):
                        self.print_stderr("Invalid VSFS: Invalid Path To Internal File")
                        exit(1)
                    dir = dir + "/" + l[i+1]
                    i = i + 1
            
            return True
        else:
            self.print_stderr("Invalid VSFS: Invalid Internal File")
            exit(1)


    # Verifies if the entered External File is valid
    def check_external_file(self, external_file):
        try:
            with open(external_file, "r") as f:
                pass
        except FileNotFoundError:
            self.print_stderr("Invalid VSFS: External File Not Found")
            exit(1)
        except IsADirectoryError:
            self.print_stderr("Invalid VSFS: Invalid External File")
            exit(1)
        else:
            return True


    
    # Verifies if the entered Internal Directory already exists
    # and returns exact line of ID in FS and 
    # position of ID in FS in a result array 
    def check_internal_directory(self, internal_directory, file_system):
        int_dir = "=" + internal_directory + "/"
        result = []
        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()

        # Checking if ID already exists in the FS array
        try:
            # If ID is not in the last line of FS,
            # It will end with "\n"
            index = contents.index(int_dir + "\n")
        except ValueError:
            index = -1
        else:
            int_dir = int_dir + "\n"

        if (index == -1):
            try:
                # If ID is in the last line of FS,
                # It will not end with "\n"
                index = contents.index(int_dir)
            except ValueError:
                index = -1
        
        result.append(index)
        result.append(int_dir)
        return result
        

    # Verifies if the entered command is valid
    def check_command(self, command, length):
        if(length >= 3):
            operation = command[_OPERATION]
            file_system = command[_FILESYSTEM]
            if (self.check_operation(operation) == True):
                if (self.check_file_system(file_system) == True):

                    if (length == 3 
                        and (operation == "defrag" 
                        or operation == "index"
                        or operation == "list")
                    ):
                        return True
                    elif (length == 4 
                        and (operation == "mkdir" 
                        or operation == "rm"
                        or operation == "rmdir")
                    ):

                        internal_directory = ""
                        internal_file = ""

                        if (operation == "rm"):
                            internal_file = command[3]
                            if (self.check_internal_file(internal_file, file_system) 
                                == True):
                                return True
                        elif (operation == "mkdir"):
                            internal_directory = command[3]
                            result = self.check_internal_directory(internal_directory, file_system)
                            index = result[0]
                            if (index != -1):
                                self.print_stderr("Invalid VSFS: Internal Directory" + 
                                "Already Exists")
                                exit(1)
                            else:
                                return True
                        elif (operation == "rmdir"):
                            internal_directory = command[3]
                            result = self.check_internal_directory(internal_directory, file_system)
                            index = result[0]
                            if (index == -1):
                                self.print_stderr("Invalid VSFS: Internal Directory" +
                                "Does Not Exist")
                                exit(1)
                            else:
                                return True
                    elif (length == 5 
                        and (operation == "copyin" 
                        or operation == "copyout")
                    ):

                        internal_file = ""
                        external_file = ""

                        if (operation == "copyin"):
                            external_file = command[3]
                            internal_file = command[4]
                        else:
                            external_file = command[4]
                            internal_file = command[3]

                        if (self.check_internal_file(internal_file, file_system) == True 
                            and self.check_external_file(external_file) == True
                        ):
                            return True                  
                    else:
                        self.print_stderr("Invalid VSFS: WRONG COMMAND")
                        exit(1)
        else:
            self.print_stderr("Invalid VSFS: WRONG COMMAND")
            exit(1)

    # Checks if the IF exists in FS and 
    # returns exact line of IF in FS and 
    # position of IF in FS in a result array 
    def does_if_exist(self, file_system, internal_file):
        int_file = "@" + internal_file
        result = []
        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()

        # Checking if IF already exists in the FS array
        try:
            # If IF is not in the last line of FS,
            # It will end with "\n"
            index = contents.index(int_file + "\n")
        except ValueError:
            index = -1
        else:
            int_file = int_file + "\n"

        if (index == -1):
            try:
                # If IF is in the last line of FS,
                # It will not end with "\n"
                index = contents.index(int_file)
            except ValueError:
                index = -1
        result.append(index)
        result.append(int_file)
        return result


    # Executes the 'copyin' command
    def do_copyin(self, file_system, external_file, internal_file):
        # Gathering contents of EF in an array
        with open(external_file, "r") as f:
            text = f.readlines()

        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()
        
        # Fetching index of IF 
        result = self.does_if_exist(file_system, internal_file)
        index = result[0]
        int_file = result[1]
        # Appending the new file to the FS
        if (index == -1):
            contents.append("\n" + int_file + "\n")     
        else:
            # Deleting the file and its contents if it was found
            contents = self.do_rm(file_system, internal_file)
            # Appending the new file to the FS 
            # after deleting the existing file
            int_file = int_file.strip()
            contents.append("\n" + int_file + "\n")
            
        # Adding a space to every line in the text to be copied 
        for x in text:
            x = " " + x
            contents.append(x)

        # Making changes to FS
        with open(file_system, "w") as f:
            contents = "".join(contents)
            f.write(contents)     


    # Executes the 'copyout' command
    def do_copyout(self, file_system, internal_file, external_file):
        # Gathering contents of EF in an array
        with open(external_file, "r") as f:
            text = f.readlines()

        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()

        # Fetching index of IF
        result = self.does_if_exist(file_system, internal_file)
        index = result[0]
        # Throwing error if IF is invalid
        if (index == -1):
            self.print_stderr("Invalid VSFS: Internal File Does Not Exist")
            exit(1)
        else:
            index = index + 1
            # Fetching contents if it was found
            while(index != len(contents)):
                if (contents[index][0] == " "):
                    line = contents[index][1:]
                    text.append(line)
                    index = index + 1
                else:
                    index = len(contents)
        
        # Removing new-line character from the last line
        text[len(text) - 1] = text[len(text) - 1].strip()
        # Making changes to EF
        with open(external_file, "w") as f:
            text = "".join(text)
            f.write(text)  


    # Executes the 'mkdir' command 
    def do_mkdir(self, file_system, internal_directory):  
        int_dir = "=" + internal_directory + "/"
        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines() 

        # Appending the new directory to the FS
        contents.append("\n" + int_dir)
        # Making changes to FS
        with open(file_system, "w") as f:
            contents = "".join(contents)
            f.write(contents) 


    # Executes the 'rm' command
    def do_rm(self, file_system, internal_file):
        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()
        
        # Fetching index of IF 
        result = self.does_if_exist(file_system, internal_file)
        index = result[0]
        int_file = result[1]
        if (index == -1):
            self.print_stderr("Invalid VSFS: Internal File Does Not Exist")
            exit(1)
        else:
            # Deleting the file and its contents if it was found
            while(index != len(contents)):
                if (contents[index][0] == " " 
                    or int_file == contents[index]
                ):
                    contents[index] = "#" + contents[index]
                    index = index + 1
                else:
                    index = len(contents) 

        result = contents      
        # Making changes to FS
        with open(file_system, "w") as f:
            contents = "".join(contents)
            f.write(contents)   
        return result


    # Executes the 'rmdir' command
    def do_rmdir(self, file_system, internal_directory): 
        # Getting index of the internal directory
        result = self.check_internal_directory(internal_directory, file_system)
        index = result[0]
        int_dir = result[1]

        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()
        # Pattern of a file/directory inside this directory
        # @dir/file or =dir/dir
        pattern_1 =  "@" + int_dir[1:].strip()
        pattern_2 = int_dir.strip()

        # Deleting the files under the directory and their contents
        while(index != len(contents)):
            if (pattern_1 in contents[index]):
                int_file = contents[index][1:].strip()
                contents = self.do_rm(file_system, int_file) 
                # Removing the file and it's size from the dictionary
                # since it is being removed from FS
                # SIZES.pop(int_file)
                # del SIZES[int_file]
                index = index + 1
            else:
                index = index + 1

        index = result[0]
        # Deleting the directories under the internal directory
        while(index != len(contents)):
            if (pattern_2 in contents[index] 
                and int_dir != contents[index]
            ):
                contents[index] = "#" + contents[index]
                index = index + 1
            else:
                index = index + 1
        
        index = result[0]
        # Deleting the internal directory itself
        while(index != len(contents)):
            if (int_dir == contents[index]):
                contents[index] = "#" + contents[index]
                index = index + 1
            else:
                index = index + 1
        
        # Making changes to FS
        with open(file_system, "w") as f:
            contents = "".join(contents)
            f.write(contents)   


    # Executes the 'defrag' command
    def do_defrag(self, file_system):
        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()
        
        index = 0
        # Deleting the lines that start with "#"
        while(index != len(contents)):
            if (contents[index][0] == "#"):
                contents.pop(index)
            else:
                index = index + 1
        
        # Removing new-line character from the last line
        contents[len(contents) - 1] = contents[len(contents) - 1].rstrip()
        # Making changes to FS
        with open(file_system, "w") as f:
            contents = "".join(contents)
            f.write(contents) 


    # Returns the number of directories one level below
    def get_link_count(self, internal_directory, file_system):

        link_count = 0
        # Getting index of the internal directory
        result = self.check_internal_directory(internal_directory, file_system)
        index = result[0]
        int_dir = result[1]
        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()
        
        # Pattern of a directory inside this directory
        # =dir/dir
        pattern = int_dir.strip()
        # Finding the directories under the internal directory
        index = index + 1
        while(index != len(contents)):
            if (pattern in contents[index]):
                path = contents[index][1:].strip()
                list = path.split("/")
                input = internal_directory.split("/")
                # Checking if no.of.dir under given dir 
                # in the current path (line) is 1, so that 
                # we know it is sub dir of given dir
                if (len(list) == len(input) + 2):
                    link_count = link_count + 1
            
            index = index + 1

        return link_count


    # Executes the 'list' command
    def do_list(self, file_system):
        # Fetching permissions, owner, group, file size, date time of the FS
        permissions = str(subprocess.check_output(["ls", "-l", file_system]))
        permissions = permissions[3:12]
        path = Path(file_system)
        owner = path.owner()
        group = path.group()
        file_size = str(os.stat(file_system).st_size)
        date_time = str(time.ctime(os.path.getctime(file_system)))
        date_time = date_time[4:len(date_time) - 8]

        # Creating a dictionary to store the names of file/dir
        # and their corresponding "list" result
        ls = {}
        # Gathering contents of FS in an array
        with open(file_system, "r") as f:
            contents = f.readlines()
        
        format = " " + owner + " " + group + " " + file_size + " " + date_time + " "
        
        # Scanning through notes file from index 1
        # since index 0 is "NOTES V1.0"
        index = 1
        while(index != len(contents)):
            # Checking if it's a file or dir
            if (contents[index][0] == "@" 
            or contents[index][0] == "=" 
            ):
                if (contents[index][0] == "@"):
                    file_name = contents[index][1:].strip()
                    attribute = "-" + permissions
                    N = "  1"
                    file_format = attribute + " " + N + format + file_name 
                    ls[file_name] = file_format
                else:
                    dir_name = contents[index][1:].strip()
                    attribute = "d" + permissions
                    lc = self.get_link_count(dir_name[0:len(dir_name)-1], file_system)
                    N = str(lc)
                    dir_format = attribute + " " + N + format + dir_name
                    ls[dir_name] = dir_format
            index = index + 1

        # Sorting file and dir names in alphabetical order (like ls)
        names = ls.keys()
        names = sorted(names)
        i = 0
        # Printing all ls values
        while (i != len(ls)):
            print(ls[names[i]])
            i = i + 1
            
            
    # Executes the entered command
    def execute(self, command):

        if (command[_OPERATION] == "list"):
            self.do_list(command[_FILESYSTEM])
        elif (command[_OPERATION] == "copyin"):
            self.do_copyin(command[_FILESYSTEM], command[3], command[4])
        elif (command[_OPERATION] == "copyout"):
            self.do_copyout(command[_FILESYSTEM], command[3], command[4])
        elif (command[_OPERATION] == "mkdir"):
            self.do_mkdir(command[_FILESYSTEM], command[3])
        elif (command[_OPERATION] == "rm"):
            self.do_rm(command[_FILESYSTEM], command[3])
        elif (command[_OPERATION] == "rmdir"):
            self.do_rmdir(command[_FILESYSTEM], command[3])
        elif (command[_OPERATION] == "defrag"):
            self.do_defrag(command[_FILESYSTEM])
        elif (command[_OPERATION] == "index"):
            self.print_stderr("Not implemented.")
            exit(1)