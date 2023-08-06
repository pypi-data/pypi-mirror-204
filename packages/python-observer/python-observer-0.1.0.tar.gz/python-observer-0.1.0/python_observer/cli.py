import argparse

from .constants import DOT_CHAR
from .date import format_time, get_current_time, get_monotonic_time
from .display import newline, observer_message, print_both_sides, print_line
from .display import rich_print as print
from .misc import file_exists, get_python_version
from .watch import watch_file


def main():
    # sourcery skip: extract-method
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="path to the file to watch")

    args = parser.parse_args()

    try:
        if file_exists(args.file):
            file_path = args.file
        else:
            print(
                observer_message(
                    f"[red]Error: File {args.file} does not exist", style="red"
                ),
                highlight=False,
            )
            exit()

        newline()

        print_both_sides(
            left=observer_message("[magenta]A file system watcher for Python files[/]"),
            right=f"[green]{get_current_time(time_format='%Y-%m-%d %I:%M:%S %p')} :watch:",
        )

        print_both_sides(
            left=observer_message(
                f"[green]watching file [blue]{file_path}[/blue] [dim]{DOT_CHAR}[/dim] [red]hit Ctrl + C to exit[/]"
            ),
            right=f"[blue]{get_python_version()}[/blue] :snake:",
        )

        newline()
        print_line(rule_style="cyan", char="━")
        newline()

        session_start_time = get_monotonic_time(as_seconds=True, should_round=False)

        watch_file(file_path)
    except KeyboardInterrupt:
        session_end_time = get_monotonic_time(as_seconds=True, should_round=False)
        newline()
        print(
            observer_message(
                f"[cyan]watch session took [yellow]{format_time(session_end_time - session_start_time)}"
            )
        )
        newline()
        print(observer_message(":wave: [red]Goodbye![/]"))
        newline()
        exit()


if __name__ == "__main__":
    main()
