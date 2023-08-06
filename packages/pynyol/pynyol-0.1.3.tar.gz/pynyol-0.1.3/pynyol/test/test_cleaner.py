from pynyol.cleaner import replace_symbols, expand_abbreviations, clean

a = "tengo un med-fenómeno que - a decir verdad - no me interesa. sr y sra. quiero que sepan esto; y a pesar de todo: hola srael"
print(expand_abbreviations(replace_symbols(a)))

b = "tengo un med-fenómeno que - a decir verdad - no me interesa. sr y sra. Worcław quiero que sepan esto; y a pesar de todo: me deben $4532,48 por el trabajo 25659,32"
print(clean(b))