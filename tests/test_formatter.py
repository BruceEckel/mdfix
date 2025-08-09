"""Tests for the semantic break formatter."""

import pytest
from md_semlinebreak.formatter import format_paragraph, format_markdown, normalize_unicode
from md_semlinebreak.config import Config


class TestSemanticBreakFormatter:
    """Test cases for semantic break formatter."""
    
    def test_simple_sentence(self):
        """Test formatting a simple sentence."""
        text = "This is a simple sentence."
        expected = "This is a simple sentence."
        result = format_paragraph(text)
        assert result == expected
    
    def test_sentence_with_comma(self):
        """Test formatting a sentence with comma."""
        text = "This is a sentence, and it has a comma."
        expected = "This is a sentence,\nand it has a comma."
        result = format_paragraph(text)
        assert result == expected
    
    def test_multiple_sentences(self):
        """Test formatting multiple sentences."""
        text = "This is the first sentence. This is the second sentence."
        expected = "This is the first sentence.\nThis is the second sentence."
        result = format_paragraph(text)
        assert result == expected
    
    def test_conjunction_no_break(self):
        """Test that simple conjunctions don't break mid-sentence."""
        text = "This book is for developers who know two or more languages but not JavaScript."
        expected = "This book is for developers who know two or more languages but not JavaScript."
        result = format_paragraph(text)
        assert result == expected
    
    def test_complex_sentence(self):
        """Test formatting a complex sentence."""
        text = "This is a complex sentence, with multiple clauses, and it should break appropriately."
        expected = "This is a complex sentence,\nwith multiple clauses,\nand it should break appropriately."
        result = format_paragraph(text)
        assert result == expected
    
    def test_markdown_headers(self):
        """Test that headers are preserved."""
        text = "# This is a header\n\nThis is a paragraph."
        expected = "# This is a header\n\nThis is a paragraph."
        result = format_markdown(text)
        assert result == expected
    
    def test_code_blocks(self):
        """Test that code blocks are preserved."""
        text = "```python\nprint('hello')\n```"
        expected = "```python\nprint('hello')\n```"
        result = format_markdown(text)
        assert result == expected
    
    def test_lists(self):
        """Test that lists are preserved."""
        text = "- Item 1\n- Item 2"
        expected = "- Item 1\n- Item 2"
        result = format_markdown(text)
        assert result == expected
    
    def test_empty_input(self):
        """Test handling empty input."""
        text = ""
        expected = ""
        result = format_markdown(text)
        assert result == expected
    
    def test_whitespace_only(self):
        """Test handling whitespace-only input."""
        text = "   \n  \n  "
        result = format_markdown(text)
        assert result.strip() == ""


class TestNormalizeUnicode:
    """Test cases for Unicode normalization."""
    
    def test_smart_quotes(self):
        """Test converting smart quotes to straight quotes."""
        text = "\u201CHello world\u201D and \u2018test\u2019"
        expected = '"Hello world" and \'test\''
        result = normalize_unicode(text)
        assert result == expected
    
    def test_dashes(self):
        """Test converting em and en dashes to double hyphens."""
        text = "This is an em dash — and this is an en dash –"
        expected = "This is an em dash -- and this is an en dash --"
        result = normalize_unicode(text)
        assert result == expected
    
    def test_ellipsis(self):
        """Test converting ellipsis to three periods."""
        text = "This is an ellipsis…"
        expected = "This is an ellipsis..."
        result = normalize_unicode(text)
        assert result == expected
    
    def test_special_spaces(self):
        """Test converting special spaces to regular spaces."""
        text = "This\u00A0has\u2009special\u200Aspaces"
        expected = "This has special spaces"
        result = normalize_unicode(text)
        assert result == expected
    
    def test_zero_width_spaces(self):
        """Test removing zero-width spaces."""
        text = "This\u200Bhas\u2060zero-width spaces"
        expected = "Thishaszero-width spaces"
        result = normalize_unicode(text)
        assert result == expected
    
    def test_multiple_replacements(self):
        """Test handling multiple Unicode characters."""
        text = "\u201CThis is a test\u201D \u2014 with multiple\u2026 characters\u2019"
        expected = '"This is a test" -- with multiple... characters\''
        result = normalize_unicode(text)
        assert result == expected
    
    def test_no_changes_needed(self):
        """Test text that doesn't need normalization."""
        text = 'Regular "quotes" and normal text.'
        expected = text
        result = normalize_unicode(text)
        assert result == expected


class TestConfig:
    """Test cases for configuration functionality."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        assert config.max_line_length == 80
        assert config.soft_wrap_length == 70
        assert config.break_at_clauses == True
        assert config.clause_break_punctuation == [',', ':', ';']
        
    def test_custom_config(self):
        """Test custom configuration values."""
        config = Config(
            max_line_length=100,
            break_at_clauses=False,
            clause_break_punctuation=[',']
        )
        assert config.max_line_length == 100
        assert config.break_at_clauses == False
        assert config.clause_break_punctuation == [',']
        
    def test_disable_clause_breaks(self):
        """Test disabling clause breaks."""
        config = Config(break_at_clauses=False)
        text = "This has commas, semicolons; and colons: but no breaks."
        expected = "This has commas, semicolons; and colons: but no breaks."
        result = format_paragraph(text, config)
        assert result == expected
        
    def test_custom_punctuation(self):
        """Test custom clause break punctuation."""
        config = Config(clause_break_punctuation=[','])  # Only break on commas
        text = "Commas, break; semicolons: don't break."
        expected = "Commas,\nbreak; semicolons: don't break."
        result = format_paragraph(text, config)
        assert result == expected
        
    def test_compound_phrases_preserved(self):
        """Test that compound phrases with or/and stay together."""
        text = "This book is for developers who have two or more programming languages, but not JavaScript or TypeScript."
        expected = "This book is for developers who have two or more programming languages,\nbut not JavaScript or TypeScript."
        result = format_paragraph(text)
        assert result == expected
        
    def test_complex_paragraph_formatting(self):
        """Test formatting of a complex paragraph similar to the original issue."""
        text = "This book is for developers who have a firm grasp of two or more programming languages, but not JavaScript or TypeScript. The goal is to quickly give the experienced programmer a tour of the language, including all the odd and obscure bits so you aren't flummoxed when you see them in practice."
        
        expected = ("This book is for developers who have a firm grasp of two or more programming languages,\n"
                   "but not JavaScript or TypeScript.\n"
                   "The goal is to quickly give the experienced programmer a tour of the language,\n"
                   "including all the odd and obscure bits so you aren't flummoxed when you see them in practice.")
        
        result = format_paragraph(text)
        assert result == expected
        
    def test_line_length_consideration(self):
        """Test that line length affects breaking decisions."""
        config = Config(soft_wrap_length=30)  # Very short lines
        text = "This is a very long sentence with commas, and other punctuation that should break more aggressively."
        result = format_paragraph(text, config)
        lines = result.split('\n')
        
        # Should break at clause boundaries when lines get long
        assert len(lines) > 1
        for line in lines:
            if line.strip():  # Ignore empty lines
                assert len(line) <= 80  # Still respect max length