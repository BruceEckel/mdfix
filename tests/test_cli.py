"""Tests for the CLI interface."""

import sys
from io import StringIO
from unittest.mock import patch
import pytest
from md_semlinebreak.cli import main


class TestCLI:
    """Test cases for CLI interface."""
    
    def test_help_option(self):
        """Test --help option."""
        with patch.object(sys, 'argv', ['md-semlinebreak', '--help']):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 0
    
    def test_version_option(self):
        """Test --version option."""
        with patch.object(sys, 'argv', ['md-semlinebreak', '--version']):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 0
    
    @patch('sys.stdin', StringIO('This is a test, and it should work.'))
    @patch('sys.stdout', new_callable=StringIO)
    def test_stdin_stdout(self, mock_stdout, mock_stdin):
        """Test reading from stdin and writing to stdout."""
        with patch.object(sys, 'argv', ['md-semlinebreak']):
            main()
        output = mock_stdout.getvalue()
        expected = "This is a test,\nand it should work."
        assert output == expected