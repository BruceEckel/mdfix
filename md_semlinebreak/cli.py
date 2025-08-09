"""Command-line interface for md-semlinebreak."""

import argparse
import sys
from pathlib import Path
from .formatter import format_markdown, normalize_unicode
from .config import Config


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
        "--max-line-length",
        type=int,
        default=80,
        help="Maximum line length (default: 80)"
    )
    parser.add_argument(
        "--no-clause-breaks",
        action="store_true",
        help="Disable breaking at clauses (commas, semicolons, colons)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    args = parser.parse_args()
    
    # Show help if no arguments provided and not reading from stdin
    if len(sys.argv) == 1 and sys.stdin.isatty():
        parser.print_help()
        sys.exit(0)
    
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
    
    # Create configuration
    config = Config(
        max_line_length=args.max_line_length,
        soft_wrap_length=max(args.max_line_length - 10, 20),  # Leave some buffer
        normalize_unicode=args.normalize,
        break_at_clauses=not args.no_clause_breaks
    )
    
    # Normalize Unicode if requested
    if config.normalize_unicode:
        text = normalize_unicode(text)
    
    # Format text
    formatted_text = format_markdown(text, config)
    
    # Write output
    if args.in_place:
        Path(args.input).write_text(formatted_text, encoding='utf-8')
    elif args.output:
        Path(args.output).write_text(formatted_text, encoding='utf-8')
    else:
        print(formatted_text, end='')


if __name__ == "__main__":
    main()