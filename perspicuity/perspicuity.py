import statistics

class Perspicuity:
    def __init__(self, values):
        self.words = values['words']
        self.phrases = values['phrases']
        self.syllables = values['syllables']
        self.letters = values['letters']

    def calculate(self):
        return 0
    
    def limitResult(self,value):
        if value>100.0:
            return 100.0
        if value<0.0:
            return 0.0
        return value

class SzigrisztPazos(Perspicuity):
    def calculate(self):
        has_words = self.words > 0
        has_phrases = self.phrases > 0

        if(not(has_words) or not(has_phrases)):
            return 0
        
        return self.limitResult((207 - (62.3*((self.syllables*1.0)/(self.words*1.0))) - ((self.words*1.0)/(self.phrases*1.0))))


class FernandezHuerta(Perspicuity):
        
    def calculate(self):
        has_words = self.words > 0
        has_phrases = self.phrases > 0
        if (not(has_words) or not(has_phrases)):
            return 0

        P, F = self.__calculateFernandezHuertaValues()
        
        return self.limitResult((206.84 - (60*P) - (1.02*F)))
    
    def __calculateFernandezHuertaValues(self):
        P = (self.syllables*1.0)/(self.words*1.0)
        F = (self.words*1.0)/(self.phrases*1.0)
        return P, F

class MuLegibility(Perspicuity):
    def calculate(self):
        try:
            mean = statistics.mean(self.letters)
            variance = statistics.variance(self.letters)
            
            return self.limitResult(((self.words) / ((self.words) - 1.0)) * (mean / variance) * 100)
        except:
            return 0