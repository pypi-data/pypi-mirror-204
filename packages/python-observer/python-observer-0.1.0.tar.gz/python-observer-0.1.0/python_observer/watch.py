import os
import time

from .constants import DOT_CHAR, MIN_TIMEOUT_MILLISECONDS
from .date import format_time, get_current_time, get_monotonic_time
from .display import observer_message, print_both_sides, print_line
from .misc import resolve_path, run_file


def watch_file(file_path):
    def draw_process_lines(is_rerun=True):
        if is_rerun:
            last_save_text = f"{DOT_CHAR} [blue]since last save: [/blue]{format_time(end_save_time - start_save_time)}"
        else:
            last_save_text = ""

        if process.returncode != 0:
            print_both_sides(
                left=observer_message("[red]app crashed[/]", style="i red"),
                right=f"[blue]run:[/blue] {end_time - start_time} ms {last_save_text} {DOT_CHAR} [blue]{get_current_time()}[/]",
            )
            print_line(rule_style="dim red")
        else:
            print_both_sides(
                left=observer_message("[green]clean exit[/]", style="i green"),
                right=f"[blue]run:[/blue] {end_time - start_time} ms {last_save_text} {DOT_CHAR} [blue]{get_current_time()}[/]",
            )
            print_line(rule_style="dim green")

    print_both_sides(
        left=observer_message("[cyan]initial run[/]", style="i magenta"),
        right=f"[blue]{get_current_time()}[/]",
    )

    file_path = resolve_path(file_path)

    start_time = get_monotonic_time()

    # first run
    process = run_file(file_path)

    end_time = get_monotonic_time()

    draw_process_lines(is_rerun=False)

    # get the initial modification time of the file
    last_modified_time = os.stat(file_path).st_mtime

    start_save_time = get_monotonic_time(as_seconds=True, should_round=False)

    run_count = 1

    while True:
        # wait for a short time before checking for changes
        time.sleep(MIN_TIMEOUT_MILLISECONDS / 1000)

        # get the current modification time of the file
        current_modified_time = os.stat(file_path).st_mtime

        # check if the file has been modified since the last time we checked
        if current_modified_time != last_modified_time:
            print_both_sides(
                left=observer_message(f"[cyan]rerun {run_count}[/]", style="i magenta"),
                right=f"[blue]{get_current_time()}[/]",
            )

            end_save_time = get_monotonic_time(as_seconds=True, should_round=False)

            start_time = get_monotonic_time()

            # run the file
            process = run_file(file_path)

            end_time = get_monotonic_time()

            # update the last modified time to the current time
            last_modified_time = current_modified_time

            draw_process_lines()

            # reset the last save time
            start_save_time = get_monotonic_time(as_seconds=True, should_round=False)

            run_count += 1
