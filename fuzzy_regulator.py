from simpful import *


class Fuzzy_Regulator:
    def __init__(self,target_value : float = 40,) -> None:
        self.reset(target_value)
        self.set_rules()
        

        
    
    def __str__(self) -> str:
        return "Fuzzy"
    
    def get_signal(self, last_value : float, last_time : int, time_before_that : int) -> float:
        self.error.append(self.target_value - last_value)

        self.Hfs.set_variable("uchyb", last_value)
        self.Hfs.set_variable("zm_uchyb", self.error[-1])
        Fc_Fz = self.Hfs.Mamdani_inference(['zadany']).get('zadany')
        self.Hfs.set_variable("zadany", Fc_Fz)

        
        if Fc_Fz > 1:
            Fc_Fz = 1
        if Fc_Fz < 0:
            Fc_Fz = 0
            
        return (0.1 + Fc_Fz) * 1500
    
    def get_errors(self) -> list:
        return self.error
    
    def set_rules(self):
        self.Hfs = FuzzySystem()

        HE_1 = TriangleFuzzySet(-0.75, -0.75, -0.25, term="LL")
        HE_2 = TriangleFuzzySet(-0.5, -0.25, -0.0, term="L")
        HE_3 = TriangleFuzzySet(-0.25, 0.0, 0.25, term="M")
        HE_4 = TriangleFuzzySet(0.0, 0.25, 0.5, term="H")
        HE_5 = TriangleFuzzySet(0.25, 0.75, 0.75, term="HH")

        HZ_1 = TriangleFuzzySet(-0.6, -0.6, -0.05, term="CL")
        HZ_2 = TriangleFuzzySet(-0.06, 0.0, 0.06, term="CM")
        HZ_3 = TriangleFuzzySet(0.05, 0.6, 0.6, term="CH")

        self.Hfs.add_linguistic_variable("uchyb", LinguisticVariable([HE_1, HE_2, HE_3, HE_4, HE_5]))
        self.Hfs.add_linguistic_variable("zm_uchyb", LinguisticVariable([HZ_1, HZ_2, HZ_3]))

        mult = 1.0

        # wartość sterująca
        HU1 = TriangleFuzzySet(-1.0 * mult, -1.0 * mult, -0.80 * mult,   term="PLLL")
        HU2 = TriangleFuzzySet(-1.0 * mult, -0.80 * mult, -0.60 * mult,   term="PLL")
        HU3 = TriangleFuzzySet(-0.80 * mult, -0.60 * mult, -0.40 * mult,   term="PL")
        HU4 = TriangleFuzzySet(-0.60 * mult, -0.40 * mult, -0.20 * mult,  term="PMLL")
        HU5 = TriangleFuzzySet(-0.40 * mult, -0.20 * mult, -0.00 * mult,  term="PML")
        HU6 = TriangleFuzzySet(-0.05 * mult, 0.0 * mult, 0.05 * mult,  term="PM") #SRODEK
        HU7 = TriangleFuzzySet(0.00 * mult, 0.2 * mult, 0.40 * mult,  term="PMH")
        HU8 = TriangleFuzzySet(0.20 * mult, 0.40 * mult, 0.60 * mult,  term="PMHH")
        HU9 = TriangleFuzzySet(0.40 * mult, 0.60 * mult, 0.8 * mult, term="PH")
        HU10 = TriangleFuzzySet(0.60 * mult, 0.80 * mult, 1.00 * mult, term="PHH")
        HU11 = TriangleFuzzySet(0.8 * mult, 1.00 * mult, 1.00 * mult, term="PHHH")

        self.Hfs.add_linguistic_variable("zadany", LinguisticVariable([HU1, HU2, HU3, HU4, HU5, HU6, HU7, HU8, HU9, HU10, HU11],
                                                                universe_of_discourse=[-1.0, 1.0]))
        self.Hfs.add_rules([
            "IF (uchyb IS LL) THEN zadany IS PHHH",
            "IF (uchyb IS L) AND (zm_uchyb IS CL) THEN zadany IS PHH",
            "IF (uchyb IS L) AND (zm_uchyb IS CM) THEN zadany IS PH",
            "IF (uchyb IS L) AND (zm_uchyb IS CH) THEN zadany IS PMHH",
            "IF (uchyb IS M) AND (zm_uchyb IS CL) THEN zadany IS PMH",
            "IF (uchyb IS M) AND (zm_uchyb IS CM) THEN zadany IS PM",
            "IF (uchyb IS M) AND (zm_uchyb IS CH) THEN zadany IS PML",
            "IF (uchyb IS H) AND (zm_uchyb IS CL) THEN zadany IS PMLL",
            "IF (uchyb IS H) AND (zm_uchyb IS CM) THEN zadany IS PL",
            "IF (uchyb IS H) AND (zm_uchyb IS CH) THEN zadany IS PLL",
            "IF (uchyb IS HH) THEN zadany IS PLLL",
            ])
    
    
    def reset(self, target_value : float = 40, kp : float = 1.0, ki : float  = 0.01, kd : float  = 0.0) -> None:
        self.target_value = target_value
        self.error = [self.target_value]
        