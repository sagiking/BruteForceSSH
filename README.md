Simple multi threaded SSHBrute Force Python Script

There are two files:

The first is the python script

The second is the same script in executable format

To run the python script you need to install the module paramiko, 
you can download the module with package management system like pip:

pip install paramiko

There are various parameters you can use in the code:

  -h , --help            Show help message and exit
  
  -i , --host            The target ip
  
  -u , --user            The login username
  
  -U , --users_file      Loading several usernames from a file
  
  -p , --password        The login password
  
  -P , --passwords_file  Loading several passwords from a file    
  
  -s , --port            Define the port ssh use, The default is 22
  
  -t , --thread_number   The number of threads for the passwords search, The default is 8 threads
                        
For the tool to work it needs host address (-i), user (-u) or users list (-U) and password (-p) or password list (-P).

Example: BruteForceSSH.py -i 127.0.0.1 -U users.txt -P passwords.txt -p 22 -t 16

In this example i am attacking my computer with users and passwords file, in port 22 and using 16 threads.

Note: The threads are only for the passwords check, and inserting a large number of threads can stuck the program, The recommendation is to use between 8 - 32 threads.

This code DOES NOT promote or encourage any illegal activities!
