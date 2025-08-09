# md-semlinebreak

A Markdown semantic line break reformatter that improves readability by breaking lines at semantically meaningful points.

## Features

- Breaks lines at sentence boundaries
- Breaks at clause boundaries (commas, semicolons, colons)
- Breaks at conjunctions (and, but, or, etc.)
- Preserves Markdown formatting (headers, code blocks, lists)
- Normalizes Unicode characters to plain ASCII equivalents
- Command-line interface for easy integration

## Installation

```bash
pip install md-semlinebreak
```

## Usage

### Command Line

```bash
# Format a file and output to stdout
md-semlinebreak input.md

# Format a file and save to another file
md-semlinebreak input.md -o output.md

# Format a file in place
md-semlinebreak -i input.md

# Normalize Unicode characters (smart quotes, em dashes, etc.)
md-semlinebreak --normalize input.md

# Read from stdin
echo "This is a long sentence, with multiple clauses, and it should be reformatted." | md-semlinebreak
```

### Python API

```python
from md_semlinebreak import format_markdown, normalize_unicode

text = "This is a long sentence, with multiple clauses, and it should be reformatted."
formatted = format_markdown(text)
print(formatted)

# Normalize Unicode characters
text_with_unicode = ""Smart quotes" and em dashes — like this"
normalized = normalize_unicode(text_with_unicode)
print(normalized)  # "Smart quotes" and em dashes -- like this
```

## Example

### Input
```markdown
This is a long paragraph with multiple sentences. It has commas, semicolons; and other punctuation that should trigger line breaks. The formatter will break lines at semantically meaningful points to improve readability.
```

### Output
```markdown
This is a long paragraph with multiple sentences.
It has commas,
semicolons;
and other punctuation that should trigger line breaks.
The formatter will break lines at semantically meaningful points to improve readability.
```

## Requirements

- Python 3.10+

## Development

Run tests:
```bash
python -m pytest tests/
```

## License

MIT