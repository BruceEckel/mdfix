"""Semantic line break formatter for Markdown."""

import re

# Compile regex patterns at module level
SENTENCE_ENDINGS = re.compile(r'([.!?])\s+')
CLAUSE_BREAKS = re.compile(r'([,:;])\s+')
CONJUNCTION_BREAKS = re.compile(r'\s+(and|but|or|yet|so|for|nor)\s+')
CODE_FENCE_PATTERN = re.compile(r'^```')

# Character replacement mappings
UNICODE_REPLACEMENTS = {
    # Quotes
    '\u201C': '"',  # Left double quotation mark (curly)
    '\u201D': '"',  # Right double quotation mark (curly)
    '\u2018': "'",  # Left single quotation mark (curly)
    '\u2019': "'",  # Right single quotation mark (curly)
    '„': '"',  # Double low-9 quotation mark
    '‚': "'",  # Single low-9 quotation mark
    '«': '"',  # Left-pointing double angle quotation mark
    '»': '"',  # Right-pointing double angle quotation mark
    '‹': "'",  # Single left-pointing angle quotation mark
    '›': "'",  # Single right-pointing angle quotation mark
    
    # Dashes
    '—': '--',  # Em dash
    '–': '--',  # En dash
    
    # Spaces
    '\u00A0': ' ',  # Non-breaking space
    '\u2009': ' ',  # Thin space
    '\u200A': ' ',  # Hair space
    '\u2002': ' ',  # En space
    '\u2003': ' ',  # Em space
    '\u2004': ' ',  # Three-per-em space
    '\u2005': ' ',  # Four-per-em space
    '\u2006': ' ',  # Six-per-em space
    '\u2007': ' ',  # Figure space
    '\u2008': ' ',  # Punctuation space
    '\u200B': '',   # Zero-width space
    '\u2060': '',   # Word joiner
    
    # Other punctuation
    '…': '...',  # Horizontal ellipsis
    '′': "'",    # Prime (often used as apostrophe)
    '″': '"',    # Double prime
}


def normalize_unicode(text: str) -> str:
    """Convert Unicode characters to plain ASCII equivalents for Markdown."""
    for unicode_char, replacement in UNICODE_REPLACEMENTS.items():
        text = text.replace(unicode_char, replacement)
    return text


def _format_clauses(text: str) -> str:
    """Format clauses within a sentence."""
    parts = CLAUSE_BREAKS.split(text)
    formatted_parts = []
    current_part = ""

    for i, part in enumerate(parts):
        if i % 2 == 0:  # Text part
            current_part += part
        else:  # Punctuation part
            current_part += part
            if current_part.strip():
                formatted_parts.append(current_part.strip())
            current_part = ""

    # Handle remaining text
    if current_part.strip():
        formatted_parts.append(current_part.strip())

    return '\n'.join(formatted_parts)


def _format_sentence(sentence: str) -> str:
    """Format a single sentence with semantic breaks."""
    parts = CONJUNCTION_BREAKS.split(sentence)
    formatted_parts = []

    for i, part in enumerate(parts):
        if i % 2 == 0:  # Text part
            if part.strip():
                formatted_parts.append(_format_clauses(part.strip()))
        else:  # Conjunction part
            if formatted_parts:
                formatted_parts[-1] += f" {part.strip()}"

    return '\n'.join(filter(None, formatted_parts))


def format_paragraph(paragraph: str) -> str:
    """Format a single paragraph with semantic line breaks."""
    if not paragraph.strip():
        return paragraph

    lines = []
    current_line = ""

    # Split on sentence endings first
    sentences = SENTENCE_ENDINGS.split(paragraph)

    for i, part in enumerate(sentences):
        if i % 2 == 0:  # Text part
            if part.strip():
                current_line += part.strip()
        else:  # Punctuation part
            current_line += part
            if current_line.strip():
                lines.append(_format_sentence(current_line.strip()))
            current_line = ""

    # Handle remaining text
    if current_line.strip():
        lines.append(_format_sentence(current_line.strip()))

    return '\n'.join(lines)


def format_markdown(text: str) -> str:
    """Format entire Markdown text with semantic line breaks."""
    lines = text.split('\n')
    result_lines = []
    current_paragraph = []
    in_code_block = False

    for line in lines:
        # Handle code blocks
        if CODE_FENCE_PATTERN.match(line):
            if current_paragraph:
                result_lines.append(format_paragraph(' '.join(current_paragraph)))
                current_paragraph = []
            in_code_block = not in_code_block
            result_lines.append(line)
            continue

        if in_code_block:
            result_lines.append(line)
            continue

        # Handle other special lines (headers, lists, etc.)
        if (line.startswith('#') or
            line.startswith('- ') or
            line.startswith('* ') or
            re.match(r'^\d+\. ', line) or
            line.startswith('> ') or
            not line.strip()):

            # Format accumulated paragraph
            if current_paragraph:
                result_lines.append(format_paragraph(' '.join(current_paragraph)))
                current_paragraph = []

            result_lines.append(line)
        else:
            # Accumulate paragraph text
            current_paragraph.append(line.strip())

    # Handle final paragraph
    if current_paragraph:
        result_lines.append(format_paragraph(' '.join(current_paragraph)))

    return '\n'.join(result_lines)
