UNITS = [
    "cero",
    "un",
    "dos",
    "tres",
    "cuatro",
    "cinco",
    "seis",
    "siete",
    "ocho",
    "nueve"
]

DECIMALS = [
    "",
    "diez",
    "veinte",
    "treinta",
    "cuarenta",
    "cincuenta",
    "sesenta",
    "setenta",
    "ochenta",
    "noventa"
]

HUNDREDS = [
    "",
    "ciento",
    "doscientos",
    "trescientos",
    "cuatrocientos",
    "quinientos",
    "seiscientos",
    "setecientos",
    "ochocientos"
    "novecientos"
]

THOUSAND_MULTIPLIER = [
    {"default": "%NUM%"},
    {"un": "mil", "default": "%NUM% mil"},
    {"un": "%NUM% millón", "default": "%NUM% millones"},
    {"un": "mil", "default": "%NUM% mil"},
    {"un": "%NUM% billón", "default": "%NUM% billones"},
    {"un": "mil", "default": "%NUM% mil"},
    {"un": "%NUM% trillón", "default": "%NUM% trillones"},
    {"un": "mil", "default": "%NUM% mil"}
]

class Parser:

    def __init__(self, number: float):
        self.number = number

    def set_number(self, value):
        self.number = value

    @property
    def num(self):
        return self.number
    
    @property
    def txt(self):
        return self.process()


class HundredParser(Parser):

    def process(self):

        if (self.number >= 1000):
            raise ValueError(f"HundredParser can only handle numbers with absolute value less than 1000, but it received {self.number}") 
        
        raw = self.number

        hundreds = raw // 100
        decimals = (raw - hundreds*100) // 10
        units = (raw - hundreds*100 - decimals*10)
        proc = []

        if decimals < 1:
            proc.append(UNITS[units])
        elif decimals < 2:
            if units == 0:
                proc.append(DECIMALS[decimals])
            elif units == 1:
                proc.append("once")
            elif units == 2:
                proc.append("doce")
            elif units == 3:
                proc.append("trece")
            elif units == 4:
                proc.append("catorce")
            elif units == 5:
                proc.append("quince")
            else:
                proc.append(f'dieci{UNITS[units]}')
        elif decimals < 3:
            if units == 0:
                proc.append(DECIMALS[decimals])
            else:
                proc.append(f'veinti{UNITS[units]}')
        else:
            if units == 0:
                proc.append(DECIMALS[decimals])
            else:
                proc.append(f'{DECIMALS[decimals]} y {UNITS[units]}')

        if decimals == 0 and units == 0:
            if hundreds == 1:
                return "cien"
            else:
                return HUNDREDS[hundreds]
        else:
            proc.append(HUNDREDS[hundreds])

        return ' '.join(proc[::-1]).strip()

class IntParser(Parser):

    def process(self):
        raw = int(self.number)
        
        proc = []

        negative = False
        if raw == 0:
            return 'cero'
        elif raw < 0:
            negative = True
            raw *= -1
        
        while raw > 0:
            proc.append(HundredParser(raw%1000).process())
            raw = raw // 1000

        proc = [self.add_thousand_mult(t, i) for i, t in enumerate(proc)]

        #EXCEPTIONS
        if proc[0][-2:] == 'un':
            proc[0] = f'{proc[0]}o' #changes un for uno if its the last number

        return ('menos ' if negative else '') + ' '.join(proc[::-1])
    
    def add_thousand_mult(self, text, position):
        if position >= len(THOUSAND_MULTIPLIER):
            raise ValueError("IntParser only supports transformations of numbers lower than a traditional quadrillion (1e24)")
        
        try:
            mult = THOUSAND_MULTIPLIER[position][text]
        except KeyError:
            mult = THOUSAND_MULTIPLIER[position]["default"]

        return mult.replace("%NUM%", text)
