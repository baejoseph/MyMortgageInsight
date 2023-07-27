import numpy as np
import numpy_financial as npf

class MortgageProduct:
    def __init__(self, **kwargs):
        if 'loan' in kwargs: self.set_loan(kwargs['loan'])
        if 'term' in kwargs: self.set_term(kwargs['term'])
        if 'rate' in kwargs: self.set_rate(kwargs['rate'])
        if 'pmt' in kwargs: self.set_pmt(kwargs['pmt'])

    def set_loan(self, value=None):
        if value: self._loan = value
        else:
            self._loan = npf.pv(self._rate/1200, self._term*12, -self._pmt)
    
    def get_loan(self):
        self.set_loan()
        return self._loan
    
    def set_term(self, value=None):
        if value: self._term = value
        else:
            self._term = npf.nper(self._rate/1200, -self._pmt, self._loan)/12
    
    def get_term(self):
        self.set_term()
        return self._term
    
    def set_rate(self, value=None):
        if value: self._rate = value
        else:
            self._rate = npf.rate(self._term*12, -self._pmt, self._loan)*100
    
    def get_rate(self):
        self.set_rate()
        return self._rate

    def set_pmt(self, value=None):
        if value: self._pmt = value
        else:
            self._pmt = -npf.pmt(self._rate/1200, self._term*12, self._loan)
    
    def get_pmt(self):
        self.set_pmt()
        return self._pmt
