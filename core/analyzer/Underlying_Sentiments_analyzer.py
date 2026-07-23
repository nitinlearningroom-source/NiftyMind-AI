
from core.analyzer.greek_analyzer import GreeksAnalyzer
from core.analyzer.iv_analyzer import IVAnalyzer
from core.analyzer.max_pain_analyzer import MaxPainAnalyzer
from core.analyzer.oi_analyzer import OIAnalyzer
from core.models.models import  OptionAnalysisConfig, Underlying_Sentiment
from core.analyzer.pcr_analyzer import PCRAnalyzer
from option_chain.models.option_contract import OptionContract



class Underlying_SentimentsAnalyzer:

    def __init__(
        self,
        oi_analyzer: OIAnalyzer | None = None,
        pcr_analyzer: PCRAnalyzer | None = None,
        iv_analyzer: IVAnalyzer | None = None,
        maxpain_analyzer: MaxPainAnalyzer | None = None,
        greeks_analyzer: GreeksAnalyzer | None = None,
    ):
        
        #todo: make this 500 configurabel
         
        self.oi_analyzer = oi_analyzer or OIAnalyzer(config=OptionAnalysisConfig(atm_window=10))  
        self.pcr_analyzer = pcr_analyzer or PCRAnalyzer(config=OptionAnalysisConfig(atm_window=10))  
        self.iv_analyzer = iv_analyzer or IVAnalyzer(config=OptionAnalysisConfig(atm_window=10))  
        self.maxpain_analyzer = maxpain_analyzer or MaxPainAnalyzer(config=OptionAnalysisConfig(atm_window=10))  
        self.greeks_analyzer = greeks_analyzer or GreeksAnalyzer(config=OptionAnalysisConfig(atm_window=10))  

    def analyze(self, snapshot):

        oi = self.oi_analyzer.analyze(snapshot)

        pcr = self.pcr_analyzer.analyze(snapshot)

        iv = self.iv_analyzer.analyze(snapshot)

        max_pain = self.maxpain_analyzer.analyze(snapshot)
        
        greeks = self.greeks_analyzer.analyze(snapshot)

        

        return Underlying_Sentiment(
               
               oi_analysis=oi,
               pcr_analysis=pcr,
               iv_analysis=iv,
               max_pain_analysis=max_pain,
               greeks_analysis=greeks 
        )

   