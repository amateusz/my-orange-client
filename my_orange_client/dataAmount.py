class Data_Amount:
    def __init__(self, amount=None):
        if type(amount) == str:
            if (' ' in amount):
                self.amount, self.units = amount.split()
                self.amount = float(self.amount)
            else:
                self.amount = float(amount)
                self.units = 'GB'
        elif type(amount) == float:
            self.amount = amount
            self.units = 'GB'
        # else:
        #     self.unit
        self.normalize()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if not self.amount:
            return '--' + ' ' + self.units
        else:
            # pity of me. for complience with computer world it should be dot not comma, but I like comma better!
            return str(self.amount).replace('.', ',') + ' ' + self.units

    def __eq__(self, incoming):
        if incoming is None:
            return True if self.amount is None else False
        return self.amount == incoming

    def __int__(self):
        return int(self.amount)

    def __float__(self):
        return self.amount

    def normalize(self):
        # normalize to GB
        normalize_factor = None
        units_caseless = self.units.lower()
        # not really considering kilo BITS here
        if units_caseless == 'kb':
            normalize_factor = 1000.0 ** 2
        elif units_caseless == 'kib':
            normalize_factor = 1024.0 ** 2
        elif units_caseless == 'mb':
            normalize_factor = 1000.0
        elif units_caseless == 'mib':
            normalize_factor = 1024.0
        elif units_caseless == 'gib':
            normalize_factor = 1.024
        elif units_caseless == 'gb':
            return

        self.amount /= normalize_factor
        self.units = 'GB'
