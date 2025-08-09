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
    
    def test_stdin_stdout(self):
        """Test reading from stdin and writing to stdout."""
        with patch('sys.stdin', StringIO('This is a test, and it should work.')), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch.object(sys, 'argv', ['md-semlinebreak']):
            main()
        output = mock_stdout.getvalue()
        expected = "This is a test,\nand it should work."
        assert output == expected
        
    def test_no_clause_breaks_option(self):
        """Test --no-clause-breaks option."""
        with patch('sys.stdin', StringIO('This has commas, semicolons; and colons: everywhere.')), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch.object(sys, 'argv', ['md-semlinebreak', '--no-clause-breaks']):
            main()
        output = mock_stdout.getvalue()
        expected = "This has commas, semicolons; and colons: everywhere."
        assert output == expected
        
    def test_compound_phrases_preserved(self):
        """Test that compound phrases with conjunctions stay together."""
        with patch('sys.stdin', StringIO('This book is for developers who know two or more languages but not JavaScript.')), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch.object(sys, 'argv', ['md-semlinebreak']):
            main()
        output = mock_stdout.getvalue()
        expected = "This book is for developers who know two or more languages but not JavaScript."
        assert output == expected
        
    def test_normalize_option(self):
        """Test --normalize option."""
        with patch('sys.stdin', StringIO('\u201CSmart quotes\u201D and em\u2014dashes should be normalized.')), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch.object(sys, 'argv', ['md-semlinebreak', '--normalize']):
            main()
        output = mock_stdout.getvalue()
        expected = '"Smart quotes" and em--dashes should be normalized.'
        assert output == expected