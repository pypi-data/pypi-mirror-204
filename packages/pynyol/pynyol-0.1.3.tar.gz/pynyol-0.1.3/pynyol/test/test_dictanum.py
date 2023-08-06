#change this for unittest

from pynyol.dictanum import IntParser

MAX_ALLOWED = 1e24

ip = IntParser(45)
print(ip.num)
print(ip.txt)

ip.set_number(0)
print(ip.num)
print(ip.txt)

ip.set_number(323)
print(ip.num)
print(ip.txt)

ip.set_number(401)
print(ip.num)
print(ip.txt)

ip.set_number(-567)
print(ip.num)
print(ip.txt)

ip.set_number(-567_456)
print(ip.num)
print(ip.txt)

ip.set_number(-21_236_458_236_458_123_236_458)
print(ip.num)
print(ip.txt)

ip.set_number(MAX_ALLOWED)
print(ip.num)
print(ip.txt)