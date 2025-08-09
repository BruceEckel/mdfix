"""Tests for the semantic break formatter."""

import pytest
from md_semlinebreak.formatter import format_paragraph, format_markdown, normalize_unicode


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
    
    def test_conjunction_break(self):
        """Test breaking on conjunctions."""
        text = "This is a test and it should break on conjunctions."
        expected = "This is a test and\nit should break on conjunctions."
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
        text = ""Hello world" and 'test'"
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
        expected = "Thishas zero-width spaces"
        result = normalize_unicode(text)
        assert result == expected
    
    def test_multiple_replacements(self):
        """Test handling multiple Unicode characters."""
        text = ""This is a test" — with multiple… characters'"
        expected = '"This is a test" -- with multiple... characters\''
        result = normalize_unicode(text)
        assert result == expected
    
    def test_no_changes_needed(self):
        """Test text that doesn't need normalization."""
        text = 'Regular "quotes" and normal text.'
        expected = text
        result = normalize_unicode(text)
        assert result == expected