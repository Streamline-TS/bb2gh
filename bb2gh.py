# Copyright Streamline Tech LLC - https://www.streamline.us
# Covered under the MIT License

import subprocess
import os
import shutil
import sys
import config

# Wait for 'c' or 's' keypress on either Windows or Unix-based systems
def get_single_keypress():
    
    try:
        import termios
    except ImportError:
        # We are on Windows.
        import msvcrt
        while True:
            key = msvcrt.getch().decode()
            if key.lower() in ['c', 's']:
                print(key, end="", flush=True)
                return key

    # We are on Unix-based system.
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            ch = sys.stdin.read(1)
            if ch.lower() in ['c', 's']:
                print(ch, end="", flush=True)
                return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# Run the shell command
def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\033[91mAn error occurred with the command: {command}\033[0m")
        while True:
            print("\033[91mDo you want to continue with the next repo or stop the execution? (press 'c' to continue or 's' to stop):\033[0m ", end="", flush=True)
            user_input = get_single_keypress().lower()
            print()  # Move to the next line after getting input.
            if user_input == 'c':
                return False
            elif user_input == 's':
                exit(1)
            else:
                print("\033[31mInvalid input, please press 'c' or 's'.\033[0m")
    return True


# Loop through all the repos and clone them
for bitbucket_repo in config.bitbucket_repos:
    bitbucket_repo_url = f'git@bitbucket.org:{config.bitbucket_org}/{bitbucket_repo}.git'
    github_repo_url = f'git@github.com:{config.github_org}/{bitbucket_repo}.git'
    print('\033[93m' + f"Cloning {bitbucket_repo_url} ---> {github_repo_url}" + '\033[0m')
    if not run_command(f"gh repo create {config.github_org}/{bitbucket_repo} --private"):
        continue
    if not run_command(f"git clone --mirror {bitbucket_repo_url} {bitbucket_repo}") and os.path.isdir(bitbucket_repo):
        shutil.rmtree(bitbucket_repo)
        continue
    os.chdir(bitbucket_repo)
    if not run_command("git remote rm origin"):
        os.chdir("..")
        shutil.rmtree(bitbucket_repo)
        continue
    if not run_command(f"git remote add origin {github_repo_url}"):
        os.chdir("..")
        shutil.rmtree(bitbucket_repo)
        continue
    if not run_command("git push --mirror"):
        os.chdir("..")
        shutil.rmtree(bitbucket_repo)
        continue
    os.chdir("..")
    shutil.rmtree(bitbucket_repo)