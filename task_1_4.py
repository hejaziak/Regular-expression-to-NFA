import argparse
import re




def task_1_4(args):
    regex = re.compile("[123\+\-\*\/\.=]{2,4}")
    output_file = open("task_1_4_result.txt","w+")
    with open(args.file+"/task1_4.txt", "r") as file:
        for line in file:
            matches = regex.finditer(line)
            if(matches):
                for match in matches:
                    output_file.write(match.group()+ "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?", metavar="file")
    args = parser.parse_args()
    print(args.file)
    task_1_4(args)