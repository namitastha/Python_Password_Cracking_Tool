import unittest
from unittest.mock import patch, mock_open, MagicMock
import zipfile
from new_ppc import extract_zip  # Replace 'your_script_name' with actual script filename (without .py)


class TestZipPasswordCracker(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="wrongpass\ncorrectpass\n")
    @patch("zipfile.ZipFile")
    def test_extract_zip_correct_password(self, mock_zipfile, mock_file):
        """
        Test case when the correct password is in the wordlist.
        """
        # Mocking ZipFile behavior
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # Simulate successful extraction with "correctpass"
        def extractall_side_effect(pwd):
            if pwd == b"correctpass":
                return  # Simulating successful extraction
            else:
                raise RuntimeError("Wrong password")

        mock_zip.extractall.side_effect = extractall_side_effect

        # Run function and verify it returns the correct password
        result = extract_zip("dummy.zip", "dummy_wordlist.txt")
        self.assertEqual(result, "correctpass")

    @patch("builtins.open", new_callable=mock_open, read_data="wrongpass\ninvalidpass\n")
    @patch("zipfile.ZipFile")
    def test_extract_zip_wrong_passwords(self, mock_zipfile, mock_file):
        """
        Test case when all passwords in the wordlist are incorrect.
        """
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        mock_zip.extractall.side_effect = RuntimeError("Wrong password")

        result = extract_zip("dummy.zip", "dummy_wordlist.txt")
        self.assertIsNone(result)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_extract_zip_missing_wordlist(self, mock_file):
        """
        Test case when the wordlist file is missing.
        """
        result = extract_zip("dummy.zip", "nonexistent_wordlist.txt")
        self.assertIsNone(result)

    @patch("zipfile.ZipFile", side_effect=FileNotFoundError)
    def test_extract_zip_missing_zipfile(self, mock_zipfile):
        """
        Test case when the ZIP file is missing.
        """
        result = extract_zip("nonexistent.zip", "dummy_wordlist.txt")
        self.assertIsNone(result)

    @patch("zipfile.ZipFile", side_effect=Exception("Unexpected error"))
    def test_extract_zip_unexpected_error(self, mock_zipfile):
        """
        Test case for unexpected exceptions.
        """
        result = extract_zip("dummy.zip", "dummy_wordlist.txt")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
