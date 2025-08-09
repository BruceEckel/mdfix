"""Markdown semantic line break reformatter."""

__version__ = "0.1.0"

from .formatter import format_markdown, format_paragraph, normalize_unicode

__all__ = ["format_markdown", "format_paragraph", "normalize_unicode"]