import os
import subprocess

def execute_user_command():
    user_input = input("Enter a command: ")
    # Vulnerable: Using eval on user input
    eval(user_input)

def run_system_command(
 user_input = input("Enter a system command: ")
    # Vulnerable: Using subprocess with shell=True
    subprocess.call(f"echo {user_input}", shell=True)

def execute_code():
    code = input("Enter Python code to execute: ")
    # Vulnerable: Using exec on user input
    exec(code)

if __name__ == "__main__":
    execute_user_command()
    run_system_command()
    execute_code()
