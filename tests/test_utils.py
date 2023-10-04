import unittest
import os
from slune.utils import find_directory_path, dict_to_strings, find_csv_files, get_all_paths

class TestFindDirectoryPath(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = 'test_directory'
        os.makedirs(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.2', '--folder3=0.3'))
        os.makedirs(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.22', '--folder3=0.33', '--folder4=0.4'))
        os.makedirs(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.2', 'another_folder'))
        os.makedirs(os.path.join(self.test_dir, '--folder1=0.1', '--folder5=0.5', '--folder6=0.6'))

    def tearDown(self):
        # Clean up the temporary directory structure
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.2', '--folder3=0.3'))
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.22', '--folder3=0.33', '--folder4=0.4'))
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.22', '--folder3=0.33'))
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.2', 'another_folder'))
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.2'))
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.22'))
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1', '--folder5=0.5', '--folder6=0.6'))
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1', '--folder5=0.5'))
        os.rmdir(os.path.join(self.test_dir, '--folder1=0.1'))
        os.rmdir(self.test_dir)

    def test_matching_path(self):
        search_strings = ['--folder1=', '--folder2=', '--folder3=']
        result = find_directory_path(search_strings, root_directory=self.test_dir)
        self.assertEqual(result, os.path.join(self.test_dir, '--folder1=', '--folder2=', '--folder3='))
    
    def test_matching_path_diff_order(self):
        search_strings = ['--folder2=', '--folder3=', '--folder1=']
        result = find_directory_path(search_strings, root_directory=self.test_dir)
        self.assertEqual(result, os.path.join(self.test_dir, '--folder1=', '--folder2=', '--folder3='))

    def test_partial_match(self):
        search_strings = ['--folder1=', '--folder2=', '--missing_folder=']
        result = find_directory_path(search_strings, root_directory=self.test_dir)
        self.assertEqual(result, os.path.join(self.test_dir, '--folder1=', '--folder2='))

    def test_partial_match_diff_order(self):
        search_strings = ['--folder2=', '--missing_folder=', '--folder1=']
        result = find_directory_path(search_strings, root_directory=self.test_dir)
        self.assertEqual(result, os.path.join(self.test_dir, '--folder1=', '--folder2='))

    def test_no_match(self):
        search_strings = ['--nonexistent_folder1=', '--nonexistent_folder2=']
        result = find_directory_path(search_strings, root_directory=self.test_dir)
        self.assertEqual(result, self.test_dir)

    def test_deepest(self):
        search_strings = ['--folder1=', '--folder2=', '--folder3=', '--folder4=']
        result = find_directory_path(search_strings, root_directory=self.test_dir)
        self.assertEqual(result, os.path.join(self.test_dir, '--folder1=', '--folder2=', '--folder3=', '--folder4='))
    
    def test_root_dir_with_forward_slash(self):
        search_strings = ['--folder2=', '--folder3=']
        result = find_directory_path(search_strings, root_directory=self.test_dir + '/--folder1=0.1')
        self.assertEqual(result, os.path.join(self.test_dir + '/--folder1=0.1', '--folder2=', '--folder3='))

    def test_just_root_dir_forward_slash(self):
        search_strings = ['--folder_not_there=']
        result = find_directory_path(search_strings, root_directory=self.test_dir + '/--folder1=0.1' + '/--folder2=0.2' + '/another_folder')
        self.assertEqual(result, os.path.join(self.test_dir, '--folder1=0.1', '--folder2=0.2', 'another_folder'))


class TestDictToStrings(unittest.TestCase):

    def test_dict_to_strings(self):
        d = {'arg1': 1, 'arg2': 2}
        result = dict_to_strings(d)
        self.assertEqual(result, ['--arg1=1', '--arg2=2'])
    

class TestFindCSVFiles(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory with some CSV files for testing
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)

        # Creating some CSV files
        self.csv_files = [
            'file1.csv',
            'file2.csv',
            'subdir1/file3.csv',
            'subdir2/file4.csv',
            'subdir2/subdir3/file5.csv'
        ]

        for file in self.csv_files:
            file_path = os.path.join(self.test_dir, file)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write("Sample CSV content")

    def tearDown(self):
        # Clean up the temporary directory and files after testing
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_find_csv_files(self):
        # Test the find_csv_files function

        # Call the function to get the result
        result = find_csv_files(self.test_dir)

        # Define the expected result based on the files we created
        expected_result = [
            os.path.join(self.test_dir, file) for file in self.csv_files
        ]

        # Sort both lists for comparison, as the order might not be guaranteed
        result.sort()
        expected_result.sort()

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)


class TestGetAllPaths(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory with some CSV files for testing
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)

        # Creating some CSV files with specific subdirectory paths
        self.csv_files = [
            'dir1/file1.csv',
            'dir2/file2.csv',
            'dir1/subdir1/file3.csv',
            'dir2/subdir2/file4.csv',
            'dir2/subdir2/subdir3/file5.csv'
        ]

        for file in self.csv_files:
            file_path = os.path.join(self.test_dir, file)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write("Sample CSV content")

    def tearDown(self):
        # Clean up the temporary directory and files after testing
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_get_all_paths(self):
        # Test the get_all_paths function

        # Call the function to get the result
        result = get_all_paths(['dir1', 'subdir1'], self.test_dir)

        # Define the expected result based on the files we created
        expected_result = [
            os.path.join(self.test_dir, 'dir1/subdir1/file3.csv')
        ]

        # Sort both lists for comparison, as the order might not be guaranteed
        result.sort()
        expected_result.sort()

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()