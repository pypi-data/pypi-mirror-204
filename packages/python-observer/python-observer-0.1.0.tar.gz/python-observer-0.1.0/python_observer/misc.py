import subprocess
import sys
from pathlib import Path


def get_python_version():
    return (
        subprocess.check_output(f"{sys.executable} --version", shell=True)
        .strip()
        .decode("utf-8")
    )


def run_file(file_path, args=None):
    cmd = [sys.executable, file_path]

    if args is not None:
        cmd += args.split()  # split the arguments string into a list

    return subprocess.run(cmd)


def resolve_path(path):
    return Path(path).resolve()


def file_exists(file_path):
    return Path(file_path).is_file()
