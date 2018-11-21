#!/bin/python3
import os
import sys
import subprocess

def path_2_inode(path):
    splited_path = path.split("/")
    output = 0
    #remove root slash
    if splited_path[0] == '':
        splited_path = splited_path[1:]

    for folder in splited_path:
        if output == 0:
            command = "fls -o 2048 sally_disk | awk '$3==\"" + folder + "\" {print $2}' | egrep -o \"[0-9]+\""
        else:
            command = "fls -o 2048 sally_disk " + str(output) + " | awk '$3==\"" + folder + "\" {print $2}' | egrep -o \"[0-9]+\""
        output = subprocess.getoutput(command)
    return output

def list_folder(path):
    inode = path_2_inode(path)
    command = "fls -o 2048 sally_disk " + str(inode)
    output = subprocess.getoutput(command)
    return output


def simple_extract(inode, newfilepath):
    command = "icat -o 2048 sally_disk " + str(inode) + " > " + newfilepath
    subprocess.getoutput(command)

def extract(pathfile, newfilepath):
    inode = path_2_inode(pathfile)
    simple_extract(inode, newfilepath)

def extract_folder(path, newfilepath):
    inode = path_2_inode(path)

def main(argv):
    if len(sys.argv) <= 1:
        print("ERROR: Missing arguments")
        exit(1)

    #List folder
    if sys.argv[1] == "l":
        print("** YOU ARE WATCHING THE CONTENT OF: " + sys.argv[2])
        print()
        print(list_folder(sys.argv[2]))

    #Simple extract: given inode return content
    elif sys.argv[1] == "se":
        print(simple_extract(sys.argv[2], sys.argv[3]))

    #extract file by path
    elif sys.argv[1] == "e":
        print(extract(sys.argv[2], sys.argv[3]))

    #extract folder by path
    elif sys.argv[1] == "ef":
        print(extract_folder(sys.argv[2], sys.argv[3]))

if __name__ == "__main__":
   main(sys.argv[1:])


