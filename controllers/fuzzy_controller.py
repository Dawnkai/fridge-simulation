"""Fuzzy controller component."""

from simpful import FuzzySystem, TriangleFuzzySet, LinguisticVariable

from constants import MAX_WORK

class Fuzzy_Controller:
    '''
    Fuzzy controller object.
    :param target_value: target regulated process value.
    :param max_response: maximum allowed response.
    '''
    def __init__(self, target_value : float = 10, init_value : float = 25,  max_signal : int = MAX_WORK) -> None:
        self.reset(target_value,init_value,  max_signal)
        self.set_rules()

    def __str__(self) -> str:
        return "Fuzzy"

    def get_signal(self, last_value : float, last_time : int, time_before_that : int) -> float:
        '''
        Get response from the controller.
        :param last_value: last value of controlled object.
        :param last_time: unused, last time of the measurement
        :param time_before_that: unused, time before the last_time
        '''
        self.errors.append( self.target_value - last_value)

        error= self.errors[-1] / self.max_signal
        prev_error = self.errors[-2]/ self.max_signal

        if(len(self.errors)>2): self.change = error - prev_error
        
        self.fuzzy_system.set_variable("error", error)
        self.fuzzy_system.set_variable("error_diff", error - prev_error )
        signal = self.fuzzy_system.Mamdani_inference(['signal']).get('signal')
        self.fuzzy_system.set_variable("signal", signal)
        
        
        return  max(-1, min(signal, 1)) * self.max_signal

    def get_errors(self) -> list:
        """Get all measurement errors detected by controller."""
        return self.errors

    def set_rules(self) -> None:
        """Set rules for the fuzzy controller."""
        self.fuzzy_system = FuzzySystem()

        self.fuzzy_system.add_linguistic_variable("error", LinguisticVariable([
            TriangleFuzzySet(-0.75, -0.75, -0.25, term="LL"),
            TriangleFuzzySet(-0.5, -0.25, -0.0, term="L"),
            TriangleFuzzySet(-0.25, 0.0, 0.25, term="M"),
            TriangleFuzzySet(0.0, 0.25, 0.5, term="H"),
            TriangleFuzzySet(0.25, 0.75, 0.75, term="HH")
        ]))
        self.fuzzy_system.add_linguistic_variable("error_diff", LinguisticVariable([
            TriangleFuzzySet(-0.6, -0.6, -0.05, term="CL"),
            TriangleFuzzySet(-0.06, 0.0, 0.06, term="CM"),
            TriangleFuzzySet(0.05, 0.6, 0.6, term="CH")
        ]))

        mult = 1.0

        # Control variable
        
        self.fuzzy_system.add_linguistic_variable("signal", LinguisticVariable(
            [
                TriangleFuzzySet(-1.0 * mult, -1.0 * mult, -0.80 * mult,   term="PHHH"),
                TriangleFuzzySet(-1.0 * mult, -0.80 * mult, -0.60 * mult,   term="PHH"),
                TriangleFuzzySet(-0.80 * mult, -0.60 * mult, -0.40 * mult,   term="PH"),
                TriangleFuzzySet(-0.60 * mult, -0.40 * mult, -0.20 * mult,  term="PMHH"),
                TriangleFuzzySet(-0.40 * mult, -0.20 * mult, -0.00 * mult,  term="PMH"),
                TriangleFuzzySet(-0.05 * mult, 0.0 * mult, 0.05 * mult,  term="PM"), # MIDDLE
                TriangleFuzzySet(0.00 * mult, 0.2 * mult, 0.40 * mult,  term="PML"),
                TriangleFuzzySet(0.20 * mult, 0.40 * mult, 0.60 * mult,  term="PMLL"),
                TriangleFuzzySet(0.40 * mult, 0.60 * mult, 0.8 * mult, term="PL"),
                TriangleFuzzySet(0.60 * mult, 0.80 * mult, 1.00 * mult, term="PLL"),
                TriangleFuzzySet(0.8 * mult, 1.00 * mult, 1.00 * mult, term='PLLL')
            ],
            universe_of_discourse=[-1.0, 1.0]
        ))

        
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

        

        

    def reset(self, target_value : float = 10, init_value : float = 25 ,max_signal : int = MAX_WORK) -> None:
        """Change parameters of the controller and reset measurements."""
        self.target_value = target_value
        self.max_signal = max_signal
        self.errors = [(self.target_value - init_value)]
        self.change=0
        
