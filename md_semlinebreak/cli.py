"""Command-line interface for md-semlinebreak."""

import argparse
import sys
from pathlib import Path
from .formatter import format_markdown, normalize_unicode


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Reformat Markdown files with semantic line breaks"
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Input Markdown file (default: stdin)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "-i", "--in-place",
        action="store_true",
        help="Edit file in place"
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Normalize Unicode characters to plain ASCII equivalents"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.in_place and not args.input:
        parser.error("--in-place requires an input file")
    
    if args.in_place and args.output:
        parser.error("--in-place and --output are mutually exclusive")
    
    # Read input
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File '{args.input}' not found", file=sys.stderr)
            sys.exit(1)
        text = input_path.read_text(encoding='utf-8')
    else:
        text = sys.stdin.read()
    
    # Normalize Unicode if requested
    if args.normalize:
        text = normalize_unicode(text)
    
    # Format text
    formatted_text = format_markdown(text)
    
    # Write output
    if args.in_place:
        Path(args.input).write_text(formatted_text, encoding='utf-8')
    elif args.output:
        Path(args.output).write_text(formatted_text, encoding='utf-8')
    else:
        print(formatted_text, end='')


if __name__ == "__main__":
    main()