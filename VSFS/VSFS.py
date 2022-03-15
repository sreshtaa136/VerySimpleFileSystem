#!/usr/bin/python3
import sys
import Commands

def main():

    object = Commands.VSFSCommands()

    arg_length = len(sys.argv)

    if (arg_length == 1):
        object.print_stderr("Invalid VSFS: PROVIDE VALID ARGUMENTS")
        exit(1)
    else:
        # Checking if entered command is valid and executing it
        if (object.check_command(sys.argv, arg_length) == True):
            object.execute(sys.argv)


if __name__ == "__main__":
    main()