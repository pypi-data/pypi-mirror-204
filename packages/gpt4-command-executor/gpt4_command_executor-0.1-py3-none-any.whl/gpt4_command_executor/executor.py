import subprocess
import logging

logging.basicConfig(filename="command_executor.log", level=logging.INFO)


def log_command(command):
    log_message = f"Executed command: {command}"
    logging.info(log_message)


def is_command_safe(command):
    if command is None:
        return False

    forbidden_commands = ["rm", "sudo", "chmod"]

    for forbidden in forbidden_commands:
        if forbidden in command:
            return False
    return True


def execute_command(command):
    if not is_command_safe(command):
        print(f"Generated command '{command}' is not safe. Skipping execution.")
        return

    print(f"Generated command: {command}")

    confirm = input("Do you want to execute this command? (y/n): ")
    if confirm.lower() == 'y':
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        log_command(command)
        return output.stdout
