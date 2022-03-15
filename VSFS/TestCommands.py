#!/usr/bin/python3
import unittest
import Commands

class TestCommands(unittest.TestCase):

    def test_check_operation(self):
        object = Commands.VSFSCommands()
        message = "TEST FAILED"
        # Testing a correct command
        self.assertTrue(object.check_operation("copyin"), message)
        # Testing a wrong command
        # and checking if it exits with exit(1)
        with self.assertRaises(SystemExit) as cm:
            object.check_operation("copy")
        self.assertEqual(cm.exception.code, 1)
    

    def test_check_file_system(self):
        object = Commands.VSFSCommands()
        message = "TEST FAILED"
        # Testing a correct FS
        self.assertTrue(object.check_file_system("VSFS.notes"), message)
        with self.assertRaises(SystemExit) as cm:
            # Testing an FS which does not exist
            # and checking if it exits with exit(1)
            object.check_file_system("VSFS.note")
            # Testing an FS which is invalid
            object.check_file_system("tests/invalid.notes")
        self.assertEqual(cm.exception.code, 1)


    def test_check_internal_file(self):
        object = Commands.VSFSCommands()
        message = "TEST FAILED"
        # Testing a correct IF
        # This method only checks if the path is valid and not the IF itself
        self.assertTrue(object.check_internal_file("dir1/note1", "tests/valid.notes"), message)
        with self.assertRaises(SystemExit) as cm:
            # Testing all the possible incorrect IFs
            # and checking if they exit with exit(1)
            object.check_internal_file("note/", "tests/valid.notes")
            object.check_internal_file(".", "tests/valid.notes")
            object.check_internal_file("..", "tests/valid.notes")
            object.check_internal_file("/", "tests/valid.notes")
            object.check_internal_file("dir0/note", "tests/valid.notes")
        self.assertEqual(cm.exception.code, 1)
        

    def test_check_external_file(self):
        object = Commands.VSFSCommands()
        message = "TEST FAILED"
        # Testing a correct EF
        self.assertTrue(object.check_external_file("tests/valid_ef"), message)
        # Testing a wrong EF
        with self.assertRaises(SystemExit) as cm:
            object.check_external_file("dummy/ef")
        self.assertEqual(cm.exception.code, 1)


    def test_check_internal_directory(self):
        object = Commands.VSFSCommands()
        # Checking if method returns index and name of given dir
        result = object.check_internal_directory("dir1/dir2", "tests/valid.notes")
        expected = [2, "=dir1/dir2/\n"]
        self.assertEqual(result, expected)
        # Result index for non-existant dir must be "-1"
        result = object.check_internal_directory("dir0", "tests/valid.notes")
        expected = [-1, "=dir0/"]


    def test_check_command(self):

        object = Commands.VSFSCommands()

        # Testing an invalid command
        with self.assertRaises(SystemExit) as cm:
            command = ["./VSFS.py"]
            object.check_command(command, len(command))
            command = ["./VSFS.py", "dummy"]
            object.check_command(command, len(command))
            command = [" "]
            object.check_command(command, len(command))
        self.assertEqual(cm.exception.code, 1)

        # Testing all correct commands
        command = ["./VSFS.py", "list", "tests/valid.notes"]
        self.assertTrue(object.check_command(command, len(command)))
        command = ["./VSFS.py", "defrag", "tests/valid.notes"]
        self.assertTrue(object.check_command(command, len(command)))
        command = ["./VSFS.py", "index", "tests/valid.notes"]
        self.assertTrue(object.check_command(command, len(command)))
        command = ["./VSFS.py", "mkdir", "tests/valid.notes", "dir10"]
        self.assertTrue(object.check_command(command, len(command)))
        command = ["./VSFS.py", "rm", "tests/valid.notes", "note1"]
        self.assertTrue(object.check_command(command, len(command)))
        command = ["./VSFS.py", "rmdir", "tests/valid.notes", "dir1"]
        self.assertTrue(object.check_command(command, len(command)))
        command = ["./VSFS.py", "copyin", "tests/valid.notes", "tests/valid_ef", "dir1/note1"]
        self.assertTrue(object.check_command(command, len(command)))
        command = ["./VSFS.py", "copyout", "tests/valid.notes", "note1", "tests/valid_ef"]
        self.assertTrue(object.check_command(command, len(command)))

        # Testing a wrong dir
        with self.assertRaises(SystemExit) as cm:
            # Testing a wrong dir
            command = ["./VSFS.py", "mkdir", "tests/valid.notes", "dir1/dir2"]
            object.check_command(command, len(command))
            # Testing an invalid path
            command = ["./VSFS.py", "rm", "tests/valid.notes", "dummy/path"]
            object.check_command(command, len(command))
            command = ["./VSFS.py", "rmdir", "tests/valid.notes", "dir0"]
            object.check_command(command, len(command))
            command = [["./VSFS.py", "copyin", "tests/invalid.notes", "dummy/ef", "dir0"]]
            object.check_command(command, len(command))
            command = [["./VSFS.py", "copyin", "tests/invalid.notes", "dir0", "dummy/ef"]]
            object.check_command(command, len(command))

        self.assertEqual(cm.exception.code, 1)


    def test_does_if_exist(self):

        object = Commands.VSFSCommands()
        result = object.does_if_exist("tests/valid.notes", "note1")
        expected = [3, "@note1\n"]
        self.assertEqual(result, expected)
        # Result index for non-existant internal file must be "-1"
        result = object.does_if_exist("tests/valid.notes", "dummy")
        expected = [-1, "@dummy"]
        self.assertEqual(result, expected)


    def test_do_copyin(self):

        object = Commands.VSFSCommands()

        # Trying to copy a file
        object.do_copyin("tests/copyin_test.notes", "tests/valid_ef", "dir1/note2")
        # Trying to replace the copied file
        object.do_copyin("tests/copyin_test.notes", "tests/valid_ef", "dir1/note2")

        # Gathering contents of FS in an array
        with open("tests/copyin_test.notes", "r") as f:
            result = f.readlines()

        # Gathering contents of expected FS in an array
        with open("tests/copyin_test.notes", "r") as f:
            expected = f.readlines()

        self.assertEqual(result, expected)

    
    def test_do_copyout(self):

        object = Commands.VSFSCommands()

        # Trying to copy out a file
        object.do_copyout("tests/copyin_test.notes", "dir1/note2", "tests/copyout_result")

        # Gathering contents of FS in an array
        with open("tests/copyout_result", "r") as f:
            result = f.readlines()

        # Gathering contents of expected FS in an array
        with open("tests/copyout_expected", "r") as f:
            expected = f.readlines()

        self.assertEqual(result, expected)

        # Testing a wrong IF
        with self.assertRaises(SystemExit) as cm:
            object.do_copyout("tests/copyin_test.notes", "dummy", "tests/copyout_result")
        self.assertEqual(cm.exception.code, 1)


    def test_do_mkdir(self):

        # Cannot check to create existing dir because error is 
        # raised in the method "check_command", which calls 
        # do_mkdir if no errors were raised
        object = Commands.VSFSCommands()
        object.do_mkdir("tests/mkdir_test.notes", "dir2")

        # Gathering contents of FS in an array
        with open("tests/mkdir_test.notes", "r") as f:
            result = f.readlines()

        # Gathering contents of expected FS in an array
        with open("tests/mkdir_expected.notes", "r") as f:
            expected = f.readlines()

        self.assertEqual(result, expected)


    def test_do_rm(self):

        object = Commands.VSFSCommands()
        object.do_rm("tests/rm_test.notes", "note1")

        # Gathering contents of FS in an array
        with open("tests/rm_test.notes", "r") as f:
            result = f.readlines()

        # Gathering contents of expected FS in an array
        with open("tests/rm_expected.notes", "r") as f:
            expected = f.readlines()

        self.assertEqual(result, expected)
        # Testing a wrong IF
        with self.assertRaises(SystemExit) as cm:
            object.do_rm("tests/rm_test.notes", "note2")
        self.assertEqual(cm.exception.code, 1)


    def test_do_rmdir(self):

        # Cannot check to rm existing dir because error is 
        # raised in the method "check_command", which calls 
        # rmdir if no errors were raised
        object = Commands.VSFSCommands()
        object.do_rmdir("tests/rmdir_test.notes", "dir1")

        # Gathering contents of FS in an array
        with open("tests/rmdir_test.notes", "r") as f:
            result = f.readlines()

        # Gathering contents of expected FS in an array
        with open("tests/rmdir_expected.notes", "r") as f:
            expected = f.readlines()

        self.assertEqual(result, expected)


    def test_do_defrag(self):
        object = Commands.VSFSCommands()
        object.do_defrag("tests/defrag_test.notes")

        # Gathering contents of FS in an array
        with open("tests/defrag_test.notes", "r") as f:
            result = f.readlines()

        # Gathering contents of expected FS in an array
        with open("tests/defrag_expected.notes", "r") as f:
            expected = f.readlines()

        self.assertEqual(result, expected)


    def test_get_link_count(self):
        object = Commands.VSFSCommands()
        result = object.get_link_count("dir1", "tests/links_test.notes")
        self.assertEqual(result, 3)


if __name__ == "__main__":
    unittest.main()