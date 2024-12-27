# bible-analysis/main.py
"""main."""

from cli.parsers import setup_parsers
from commands.handle_command import handle_command


def main():
    """Handle CLI commands."""
    parser = setup_parsers()
    args = parser.parse_args()
    handle_command(args)


if __name__ == "__main__":
    main()
