from lift.coloring import Colors, Colorate
import os
import subprocess
import sys
import time

def execute_command(command):
    try:
        if "|" in command:
            # save for restoring later on
            s_in, s_out = (0, 0)
            s_in = os.dup(0)
            s_out = os.dup(1)

            # first command takes commandut from stdin
            fdin = os.dup(s_in)

            # iterate over all the commands that are piped
            for cmd in command.split("|"):
                # fdin will be stdin if it's the first iteration
                # and the readable end of the pipe if not.
                os.dup2(fdin, 0)
                os.close(fdin)

                # restore stdout if this is the last command
                if cmd == command.split("|")[-1]:
                    fdout = os.dup(s_out)
                else:
                    fdin, fdout = os.pipe()

                # redirect stdout to pipe
                os.dup2(fdout, 1)
                os.close(fdout)

                try:
                    subprocess.run(cmd.strip().split())
                except Exception:
                    print(".dreamShell # command not found: {}".format(cmd.strip()))

            # restore stdout and stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            subprocess.run(command.split(" "))
    except Exception:
        print("psh: command not found: {}".format(command))


def psh_cd(path):
    """convert to absolute path and change directory"""
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print(".dreamShell CD # no such file or directory: {}".format(path))


def dreamshell_help():
    print(Colorate.Horizontal(Colors.red_to_yellow, f"""lift.py help # Best discord bot controlling shell ever created
    
        Command List:
    > help - Shows this message
    > exit - Stop the bot process
    """))


def main():
    while True:
        inp = input(Colorate.Horizontal(Colors.red_to_yellow, f"lift.py > "))
        if inp == "exit":
            sys.exit()
        elif inp[:3] == "cd ":
            psh_cd(inp[3:])
        elif inp == "help":
            dreamshell_help()
        else:
            execute_command(inp)

def Init():
     print(Colorate.Horizontal(Colors.black_to_blue, f"""

                    ██╗     ██╗███████╗████████╗██████╗ ██╗   ██╗
                    ██║     ██║██╔════╝╚══██╔══╝██╔══██╗╚██╗ ██╔╝
                    ██║     ██║█████╗     ██║   ██████╔╝ ╚████╔╝ 
                    ██║     ██║██╔══╝     ██║   ██╔═══╝   ╚██╔╝  
                    ███████╗██║██║        ██║██╗██║        ██║   
                    ╚══════╝╚═╝╚═╝        ╚═╝╚═╝╚═╝        ╚═╝   
                                             
                                             """))
     main()
     