from core.analyzer.oi_analyzer import OIAnalyzer


class OptionChainAnalyzer:


    def __init__(self, option_chain_df):
        self.df = option_chain_df

    def analyze(self):

        oi = OIAnalyzer(self.df).analyze()

        #pcr = PCRAnalyzer(self.df).analyze()

        #max_pain = MaxPainAnalyzer(self.df).analyze()

        #iv = IVAnalyzer(self.df).analyze()