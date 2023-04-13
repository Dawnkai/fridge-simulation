from simpful import *


class Fuzzy_Regulator:
    def __init__(self,target_value : float = 35, *args) -> None:
        self.reset(target_value)
        self.set_rules()
        

        
    
    def __str__(self) -> str:
        return "Fuzzy"
    
    def get_signal(self, last_value : float, last_time : int, time_before_that : int, prev_signal,max_force = 1500 ) -> float:
        self.error.append(( last_value - self.target_value)/max_force)

        self.fuzzy_system.set_variable("error", self.error[-1])
        self.fuzzy_system.set_variable("error_diff", self.error[-1] - self.error[-2])
        signal = self.fuzzy_system.Mamdani_inference(['signal']).get('signal')
        self.fuzzy_system.set_variable("signal", signal)

         
        if signal > 1:
            signal = 1
        if signal < 0:
            signal = 0

        
        return signal * max_force
    
    def get_errors(self) -> list:
        return self.error
    
    def set_rules(self):
        self.fuzzy_system = FuzzySystem()

        E_1 = TriangleFuzzySet(-0.75, -0.75, -0.25, term="LL")
        E_2 = TriangleFuzzySet(-0.5, -0.25, -0.0, term="L")
        E_3 = TriangleFuzzySet(-0.25, 0.0, 0.25, term="M")
        E_4 = TriangleFuzzySet(0.0, 0.25, 0.5, term="H")
        E_5 = TriangleFuzzySet(0.25, 0.75, 0.75, term="HH")

        ED_1 = TriangleFuzzySet(-0.6, -0.6, -0.05, term="CL")
        ED_2 = TriangleFuzzySet(-0.06, 0.0, 0.06, term="CM")
        ED_3 = TriangleFuzzySet(0.05, 0.6, 0.6, term="CH")

        self.fuzzy_system.add_linguistic_variable("error", LinguisticVariable([E_1, E_2, E_3, E_4, E_5]))
        self.fuzzy_system.add_linguistic_variable("error_diff", LinguisticVariable([ED_1, ED_2, ED_3]))

        mult = 1.0

        # wartość sterująca
        S_1 = TriangleFuzzySet(-1.0 * mult, -1.0 * mult, -0.80 * mult,   term="PLLL")
        S_2 = TriangleFuzzySet(-1.0 * mult, -0.80 * mult, -0.60 * mult,   term="PLL")
        S_3 = TriangleFuzzySet(-0.80 * mult, -0.60 * mult, -0.40 * mult,   term="PL")
        S_4 = TriangleFuzzySet(-0.60 * mult, -0.40 * mult, -0.20 * mult,  term="PMLL")
        S_5 = TriangleFuzzySet(-0.40 * mult, -0.20 * mult, -0.00 * mult,  term="PML")
        S_6 = TriangleFuzzySet(-0.05 * mult, 0.0 * mult, 0.05 * mult,  term="PM") #SRODEK
        S_7 = TriangleFuzzySet(0.00 * mult, 0.2 * mult, 0.40 * mult,  term="PMH")
        S_8 = TriangleFuzzySet(0.20 * mult, 0.40 * mult, 0.60 * mult,  term="PMHH")
        S_9 = TriangleFuzzySet(0.40 * mult, 0.60 * mult, 0.8 * mult, term="PH")
        S_10 = TriangleFuzzySet(0.60 * mult, 0.80 * mult, 1.00 * mult, term="PHH")
        S_11 = TriangleFuzzySet(0.8 * mult, 1.00 * mult, 1.00 * mult, term="PHHH")

        self.fuzzy_system.add_linguistic_variable("signal", LinguisticVariable([S_1, S_2, S_3, S_4, S_5, S_6, S_7, S_8, S_9, S_10, S_11],
                                                                universe_of_discourse=[-1.0, 1.0]))
        self.fuzzy_system.add_rules([
            "IF (error IS LL) THEN signal IS PHHH",
            "IF (error  IS L) AND (error_diff IS CL) THEN signal IS PHH",
            "IF (error IS L) AND (error_diff IS CM) THEN signal IS PH",
            "IF (error IS L) AND (error_diff IS CH) THEN signal IS PMHH",
            "IF (error IS M) AND (error_diff IS CL) THEN signal IS PMH",
            "IF (error IS M) AND (error_diff IS CM) THEN signal IS PM",
            "IF (error IS M) AND (error_diff IS CH) THEN signal IS PML",
            "IF (error IS H) AND (error_diff IS CL) THEN signal IS PMLL",
            "IF (error IS H) AND (error_diff IS CM) THEN signal IS PL",
            "IF (error IS H) AND (error_diff IS CH) THEN signal IS PLL",
            "IF (error IS HH) THEN signal IS PLLL",
            ])
    
    
    def reset(self, target_value : float = 35) -> None:
        self.target_value = target_value
        self.error = [self.target_value]
