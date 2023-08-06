===========
pynyol
===========

pynyol is the Python implementation of the Nyol package. This package is aimed at helping with processing the spanish language.

Each module inside the package provides help in a different area of language processing. These modules are:

    #!/usr/bin/env python

    from towelstuff import location
    from towelstuff import utils

    if utils.has_towel():
        print "Your towel is located:", location.where_is_my_towel()

(Note the double-colon and 4-space indent formatting above.)

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.


Dictanum
=========

Useful for getting the spelling of numbers.
The spelling is handled by different *parser* whith different number ranges.
This is one example for it:

    #!/usr/bin/env python

    from pynyol.dictanum import IntParser
    
    mynum = #insert a number here

    ip = IntParser(mynum)

    print(f'the spelling for {mynum} in spanish is: {ip.text}')
