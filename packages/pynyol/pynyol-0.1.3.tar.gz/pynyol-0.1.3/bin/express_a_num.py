from argparse import ArgumentParser
from pynyol.dictanum import IntParser

parser = ArgumentParser(description="This script takes a number and prints the spelling of that number")

parser.add_argument("num", required=True)

ip = IntParser(parser.num)

print(f'{ip.number} is spelled \"{ip.txt}\" in spanish.')