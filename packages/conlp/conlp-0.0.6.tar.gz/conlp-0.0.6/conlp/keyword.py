from tqdm.auto import tqdm
from conlp import preprocess
from transformers.utils import logging

class keyword: 
    def __init__(self, 
                 load_models:str or list): 
        """
        available models to load = ['keyBERT']
        """
        self.logger = logging.get_logger("transformers")
        available_models = ['keyBERT']
        
        if isinstance(load_models, str): 
            self.load_models = [load_models]
        elif isinstance(load_models, list): 
            self.load_models = load_models  
        else: 
            raise ValueError("input 'load_models' must be either str or list")
        
        self.logger.warning("""Selected Model(s) for Keyword Extraction: {}""".format(self.load_models))
        #Check whether models are installed in the local env 
        #Check whether the user assigned available models for load_models 
        uninstalled = []
        unavailable = []
        
        for model in tqdm(self.load_models, desc='Checking Model(s) in Local dir'): 
            if model in available_models: 
                if model == 'keyBERT':
                    try: 
                        from keybert import KeyBERT
                    except ModuleNotFoundError: 
                        uninstalled.append(model) 
                else: 
                    uninstalled.append(model)
            else: 
                unavailable.append(model)
        
        if len(unavailable) == 0: 
            pass
        else: 
            raise ValueError("model(s) {} is assigned in 'load_models', which is unavaliable. AVAILABLE MODELS: {}".format(unavailable, available_models))
        
        if len(uninstalled) == 0: 
            pass
        else: 
            raise FileNotFoundError("To load corresponding model(s), pre-install {} via nlp.download(models= {})".format(uninstalled, uninstalled))
        
        for model in tqdm(self.load_models, desc='Loading Model(s)'):
            if model == 'keyBERT': 
                self.KeyBERT = KeyBERT()
                print("├──'keyBERT' successfully loaded")
        
    def keyBERT(self, 
                text:str, 
                text_type:str, 
                preprocess_exception=None, 
                ngram:int=1): 
        """a BERT based model that leverages BERT embeddings to create keywords and keyphrases that are most similar to a document"""
        #TBD preprocess_exception currently only supports hashtag_exception for tweets text_type.  
        keyword_dict = {} 
        if text_type.lower() == 'news': 
            processed_text = preprocess.news(text)
        elif text_type.lower() == 'tweets' and preprocess_exception is None: 
            processed_text = preprocess.tweets(text)
        elif text_type.lower() == 'tweets' and preprocess_exception is not None:
            processed_text = preprocess.tweets(text, hashtag_exception=preprocess_exception)
            processed_text = re.sub("#", "", processed_text)
        
        for (keyword, prob) in self.KeyBERT.extract_keywords(processed_text, keyphrase_ngram_range=(1,ngram), stop_words=None): 
            keyword_dict.update({keyword: prob})
        return keyword_dict
