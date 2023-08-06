
import os 
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers.utils import logging
import numpy as np
from scipy.special import softmax
from tqdm.auto import tqdm 
import time 
from conlp import preprocess

class sentiment:     
    def __init__(self, 
                 load_models:str or list): 
        """
        Args:
            load_models (str or list): Available models to be loaded. \n
                Includes: 
                (i) 'twitter_roBERTa_v1';
                (ii)'twitter_roBERTa_v2';  
                (iii) 'twitter_XLM_roBERTa'; and
                (iv) 'finBERT'
        """
        self.logger = logging.get_logger("transformers")
        available_models = [#'alphaVADER'
                            'twitter_roBERTa_v1', 'twitter_roBERTa_v2', 'twitter_XLM_roBERTa', 'finBERT']
        
        if isinstance(load_models, str): 
            if load_models.lower() == 'all': 
                self.load_models = available_models
            else: 
                self.load_models = [load_models]
        elif isinstance(load_models, list): 
            if 'all' in load_models or 'All' in load_models: 
                self.load_models = available_models 
            else: 
                self.load_models = list(set(load_models))
        else: 
            raise ValueError("input 'load_models' must be either str or list")
        
        self.logger.warning("""Selected Model(s) for Sentiment Analysis: {}""".format(self.load_models))
        #Check whether selected models are installed in the local env 
        #Check whether the user assigned available models for load_models 
        uninstalled = []
        unavailable = []
        
        for model in tqdm(self.load_models, desc='Checking Model(s) in Local dir'): 
            if model in available_models: 
                # if model == 'alphaVADER': 
                #     pass
                # else:
                #     if os.path.isdir(model): 
                #         pass
                #     else: 
                #         uninstalled.append(model)
                if os.path.isdir(model): 
                    pass
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
            raise FileNotFoundError("To load corresponding model(s), pre-install {} via conlp.download(models= {})".format(uninstalled, uninstalled))
        
        for model in tqdm(self.load_models, desc='Loading Model(s)'):
            # if model == 'alphaVADER': 
            #     self.AlphaVADER = alphaVADER.SentimentIntensityAnalyzer().polarity_scores
            #     print("├──'alphaVADER' successfully loaded")
            #     time.sleep(1)
            if model == 'twitter_roBERTa_v1': 
                self.Twitter_roBERTa_v1_tokenizer = AutoTokenizer.from_pretrained('twitter_roBERTa_v1', local_files_only=True)
                self.Twitter_roBERTa_v1 = AutoModelForSequenceClassification.from_pretrained('twitter_roBERTa_v1', local_files_only=True)
                print("├──'twitter_roBERTa_v1' successfully loaded")
                time.sleep(1)
            elif model == 'twitter_roBERTa_v2': 
                self.Twitter_roBERTa_v2_tokenizer = AutoTokenizer.from_pretrained('twitter_roBERTa_v2', local_files_only=True)
                self.Twitter_roBERTa_v2 = AutoModelForSequenceClassification.from_pretrained('twitter_roBERTa_v2', local_files_only=True)
                print("├──'twitter_roBERTa_v2' successfully loaded")
                time.sleep(1)
            elif model == 'twitter_XLM_roBERTa':
                self.Twitter_XLM_roBERTa_tokenizer = AutoTokenizer.from_pretrained('twitter_XLM_roBERTa', local_files_only=True)
                self.Twitter_XLM_roBERTa = AutoModelForSequenceClassification.from_pretrained('twitter_XLM_roBERTa', local_files_only=True)
                print("├──'twitter_XLM_roBERTa' successfully loaded")
                time.sleep(1)
            elif model == 'finBERT': 
                self.FinBERT_tokenizer = AutoTokenizer.from_pretrained('finBERT', local_files_only=True)
                self.FinBERT = AutoModelForSequenceClassification.from_pretrained('finBERT', local_files_only=True)
                print("├──'finBERT' successfully loaded")
                time.sleep(1)

    def rescaling(self, old_value, old_minvalue, old_maxvalue):
        new_maxvalue, new_minvalue = 1, -1
        new_value = 2*((old_value - old_minvalue)/(old_maxvalue - old_minvalue)) - 1 
        return round(new_value, 5) 

    #aVADER
    # def alphaVADER(self, text, text_type, summarize=True):
    #     if text_type.lower() == 'news': 
    #         text = preprocess.news(text)
    #     elif text_type.lower() == 'tweets': 
    #         text = preprocess.tweets(text)
    #     alphaVADER_dict = self.AlphaVADER(text)
    #     if summarize is True: 
    #         return alphaVADER_dict['compound']
    #     else: 
    #         return alphaVADER_dict

    #twitter_roBERTa_v1
    def twitter_roBERTa_v1(self, 
                           text:str, 
                           text_type:str, 
                           summarize:bool=True) -> float or dict:
        """a roBERTa model trained on 58M tweets and finetuned for sentiment analysis with the TweetEval benchmark"""
        try: 
            if text_type.lower() == 'news': 
                original_doc = preprocess.news(text)
            elif text_type.lower() == 'tweets': 
                original_doc = preprocess.tweets(text)
            labels = ['negative', 'neutral', 'positive']
            original_tokens = self.Twitter_roBERTa_v1_tokenizer(original_doc, return_tensors='pt')
            len_original_tokens = len(original_tokens['input_ids'][0])
            if len_original_tokens <= 514: 
                scoring = self.Twitter_roBERTa_v1(**original_tokens)
                scoring = scoring[0][0].detach().numpy()
                scoring = softmax(scoring)
                ranking = np.argsort(scoring)
                sent_dict, compound = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}, 0 
                for i in range(scoring.shape[0]):
                    l = labels[ranking[i]]
                    s = scoring[ranking[i]]
                    if l == 'positive': 
                        compound += s*10
                        sent_dict.update({'pos': round(float(s), 5)})
                    elif l == 'negative': 
                        compound -= s*10
                        sent_dict.update({'neg': round(float(s), 5)})
                    else: 
                        compound += s*1
                        sent_dict.update({'neu': round(float(s), 5)})
                sent_dict.update({'compound': self.rescaling(float(compound), -10, 10)})
                
                if summarize is True: 
                    return sent_dict['compound']
                else: 
                    return sent_dict
            elif len_original_tokens > 514: 
                #self.logger.warning("├── Any warnings related to TokenSequenceLength can be ignored as input 'text' has been splited, such that the sequence length of each split is always less than the specified maximum sequence length")
                total_neg, total_neu, total_pos, total_compound = 0, 0, 0, 0 
                original_doc = np.array([original_doc.split()])
                num_split = int(round((len_original_tokens/514)+1, 0))
                paragraphs = np.array_split(original_doc, num_split, axis=1)
                for i in range(num_split): 
                    paragraph = paragraphs[i]
                    paragraph = " ".join(str(word).replace("'", "") for word in list(paragraph))
                    paragraph = paragraph.replace("\n", "")
                    paragraph = paragraph.replace("[", "").replace("]", "")
                    tokens = self.Twitter_roBERTa_v1_tokenizer(paragraph, return_tensors='pt')
                    scoring = self.Twitter_roBERTa_v1(**tokens)
                    scoring = scoring[0][0].detach().numpy()
                    scoring = softmax(scoring)
                    ranking = np.argsort(scoring)
                    for i in range(scoring.shape[0]):
                        l = labels[ranking[i]]
                        s = scoring[ranking[i]]
                        if l == 'positive': 
                            total_pos += s 
                            total_compound += s*10
                        elif l == 'negative': 
                            total_neg += s
                            total_compound -= s*10
                        else: 
                            total_neu += s
                            total_compound += s*1
                sent_dict = {'neg': round(total_neg/num_split, 5), 
                             'neu': round(total_neu/num_split, 5), 
                             'pos': round(total_pos/num_split, 5), 
                             'compound': self.rescaling(total_compound, -10*num_split, 10*num_split)}
                
                if summarize is True: 
                    return sent_dict['compound']
                else: 
                    return sent_dict 
        except AttributeError: 
            raise SystemError("twitter_roBERTa_v1 must be loaded in prior. Load the model via nlp.sentiment(load_models='twitter_roBERTa_v1')")

    #twitter_roBERTa_v2
    def twitter_roBERTa_v2(self, 
                           text:str, 
                           text_type:str, 
                           summarize:bool=True) -> float or dict:
        try: 
            """a roBERTa model trained on 124M tweets and finetuned for sentiment analysis with the TweetEval benchmark"""
            if text_type.lower() == 'news': 
                original_doc = preprocess.news(text)
            elif text_type.lower() == 'tweets': 
                original_doc = preprocess.tweets(text)
            labels = ['negative', 'neutral', 'positive']
            original_tokens = self.Twitter_roBERTa_v2_tokenizer(original_doc, return_tensors='pt')
            len_original_tokens = len(original_tokens['input_ids'][0])
            if len_original_tokens <= 514:
                scoring = self.Twitter_roBERTa_v2(**original_tokens)
                scoring = scoring[0][0].detach().numpy()
                scoring = softmax(scoring)
                ranking = np.argsort(scoring)
                sent_dict, compound = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}, 0 
                for i in range(scoring.shape[0]):
                    l = labels[ranking[i]]
                    s = scoring[ranking[i]]
                    if l == 'positive': 
                        compound += s*10
                        sent_dict.update({'pos': round(float(s), 5)})
                    elif l == 'negative': 
                        compound -= s*10
                        sent_dict.update({'neg': round(float(s), 5)})
                    else: 
                        compound += s*1
                        sent_dict.update({'neu': round(float(s), 5)})
                sent_dict.update({'compound': self.rescaling(float(compound), -10, 10)})
                
                if summarize is True:
                    return sent_dict['compound']
                else: 
                    return sent_dict 
            elif len_original_tokens > 514: 
                #self.logger.warning("├── Any warnings related to TokenSequenceLength can be ignored as input 'text' has been splited, such that the sequence length of each split is always less than the specified maximum sequence length")
                total_neg, total_neu, total_pos, total_compound = 0, 0, 0, 0 
                original_doc = np.array([original_doc.split()])
                num_split = int(round((len_original_tokens/514)+1, 0))
                paragraphs = np.array_split(original_doc, num_split, axis=1)
                for i in range(num_split): 
                    paragraph = paragraphs[i]
                    paragraph = " ".join(str(word).replace("'", "") for word in list(paragraph))
                    paragraph = paragraph.replace("\n", "")
                    paragraph = paragraph.replace("[", "").replace("]", "")
                    tokens = self.Twitter_roBERTa_v2_tokenizer(paragraph, return_tensors='pt')
                    scoring = self.Twitter_roBERTa_v2(**tokens)
                    scoring = scoring[0][0].detach().numpy()
                    scoring = softmax(scoring)
                    ranking = np.argsort(scoring)
                    for i in range(scoring.shape[0]):
                        l = labels[ranking[i]]
                        s = scoring[ranking[i]]
                        if l == 'positive': 
                            total_pos += s 
                            total_compound += s*10
                        elif l == 'negative': 
                            total_neg += s
                            total_compound -= s*10
                        else: 
                            total_neu += s
                            total_compound += s*1
                sent_dict = {'neg': round(total_neg/num_split, 5), 
                             'neu': round(total_neu/num_split, 5), 
                             'pos': round(total_pos/num_split, 5), 
                             'compound': self.rescaling(total_compound, -10*num_split, 10*num_split)}
                if summarize is True: 
                    return sent_dict['compound']
                else: 
                    return sent_dict 
        except AttributeError: 
            raise SystemError("twitter_roBERTa_v2 must be loaded in prior. Load the model via nlp.sentiment(load_models='twitter_roBERTa_v2')")

    #twitter_XLM_roBERTa
    def twitter_XLM_roBERTa(self, 
                            text:str, 
                            text_type:str, 
                            summarize:bool=True) -> float or dict:
        try: 
            """a XLM-roBERTa model trained on 198M tweets and finetuned for sentiment analysis with"""
            if text_type.lower() == 'news': 
                original_doc = preprocess.news(text)
            elif text_type.lower() == 'tweets': 
                original_doc = preprocess.tweets(text)
            labels = ['negative', 'neutral', 'positive']
            original_tokens = self.Twitter_XLM_roBERTa_tokenizer(original_doc, return_tensors='pt')
            len_original_tokens = len(original_tokens['input_ids'][0])
            if len_original_tokens <= 514: 
                scoring = self.Twitter_XLM_roBERTa(**original_tokens)
                scoring = scoring[0][0].detach().numpy()
                scoring = softmax(scoring)
                ranking = np.argsort(scoring)
                sent_dict, compound = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}, 0 
                for i in range(scoring.shape[0]):
                    l = labels[ranking[i]]
                    s = scoring[ranking[i]]
                    if l == 'positive': 
                        compound += s*10
                        sent_dict.update({'pos': round(float(s), 5)})
                    elif l == 'negative': 
                        compound -= s*10
                        sent_dict.update({'neg': round(float(s), 5)})
                    else: 
                        compound += s*1
                        sent_dict.update({'neu': round(float(s), 5)})
                sent_dict.update({'compound': self.rescaling(float(compound), -10, 10)})
                
                if summarize is True: 
                    return sent_dict['compound']
                else: 
                    return sent_dict 
            elif len_original_tokens > 514: 
                #self.logger.warning("├── Any warnings related to TokenSequenceLength can be ignored as input 'text' has been splited, such that the sequence length of each split is always less than the specified maximum sequence length")
                total_neg, total_neu, total_pos, total_compound = 0, 0, 0, 0 
                original_doc = np.array([original_doc.split()])
                num_split = int(round((len_original_tokens/514)+1, 0))
                paragraphs = np.array_split(original_doc, num_split, axis=1)
                for i in range(num_split): 
                    paragraph = paragraphs[i]
                    paragraph = " ".join(str(word).replace("'", "") for word in list(paragraph))
                    paragraph = paragraph.replace("\n", "")
                    paragraph = paragraph.replace("[", "").replace("]", "")
                    tokens = self.Twitter_XLM_roBERTa_tokenizer(paragraph, return_tensors='pt')
                    scoring = self.Twitter_XLM_roBERTa(**tokens)
                    scoring = scoring[0][0].detach().numpy()
                    scoring = softmax(scoring)
                    ranking = np.argsort(scoring)
                    for i in range(scoring.shape[0]):
                        l = labels[ranking[i]]
                        s = scoring[ranking[i]]
                        if l == 'positive': 
                            total_pos += s 
                            total_compound += s*10
                        elif l == 'negative': 
                            total_neg += s
                            total_compound -= s*10
                        else: 
                            total_neu += s
                            total_compound += s*1
                sent_dict = {'neg': round(total_neg/num_split, 5), 
                             'neu': round(total_neu/num_split, 5), 
                             'pos': round(total_pos/num_split, 5), 
                             'compound': self.rescaling(total_compound, -10*num_split, 10*num_split)}
                
                if summarize is True: 
                    return sent_dict['compound']
                else: 
                    return sent_dict 
        except AttributeError: 
            raise SystemError("XLM_roBERTa must be loaded in prior. Load the model via nlp.sentiment(load_models='XLM_roBERTa')")

    #finBERT
    def finBERT(self, 
                text:str, 
                text_type:str, 
                summarize:bool=True) -> float or dict: 
        try: 
            """a BERT model trained on 400k financial texts, including TRC2-financial dataset, Financial PhraseBank, and FiQA Sentiment dataset"""
            if text_type.lower() == 'news': 
                original_doc = preprocess.news(text)
            elif text_type.lower() == 'tweets': 
                original_doc = preprocess.tweets(text)
            labels = ['neutral', 'positive', 'negative']
            original_tokens = self.FinBERT_tokenizer(original_doc, return_tensors='pt')
            len_original_tokens = len(original_tokens['input_ids'][0])
            if len_original_tokens <= 512: 
                scoring = self.FinBERT(**original_tokens)
                scoring = scoring[0][0].detach().numpy()
                scoring = softmax(scoring)
                ranking = np.argsort(scoring)
                sent_dict, compound = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}, 0 
                for i in range(scoring.shape[0]):
                    l = labels[ranking[i]]
                    s = scoring[ranking[i]]
                    if l == 'positive': 
                        compound += s*10
                        sent_dict.update({'pos': round(float(s), 5)})
                    elif l == 'negative': 
                        compound -= s*10
                        sent_dict.update({'neg': round(float(s), 5)})
                    else: 
                        compound += s*1
                        sent_dict.update({'neu': round(float(s), 5)})
                sent_dict.update({'compound': self.rescaling(float(compound), -10, 10)})
                
                if summarize is True: 
                    return sent_dict['compound']
                else: 
                    return sent_dict 
            elif len_original_tokens > 512: 
                self.logger.warning("├── Any warnings related to TokenSequenceLength can be ignored as input 'text' has been splited, such that the sequence length of each split is always less than the specified maximum sequence length")
                total_neg, total_neu, total_pos, total_compound = 0, 0, 0, 0 
                original_doc = np.array([original_doc.split()])
                num_split = int(round((len_original_tokens/512)+1, 0))
                paragraphs = np.array_split(original_doc, num_split, axis=1)
                for i in range(num_split): 
                    paragraph = paragraphs[i]
                    paragraph = " ".join(str(word).replace("'", "") for word in list(paragraph))
                    paragraph = paragraph.replace("\n", "")
                    paragraph = paragraph.replace("[", "").replace("]", "")
                    tokens = self.FinBERT_tokenizer(paragraph, return_tensors='pt')
                    scoring = self.FinBERT(**tokens)
                    scoring = scoring[0][0].detach().numpy()
                    scoring = softmax(scoring)
                    ranking = np.argsort(scoring)
                    for i in range(scoring.shape[0]):
                        l = labels[ranking[i]]
                        s = scoring[ranking[i]]
                        if l == 'positive': 
                            total_pos += s 
                            total_compound += s*10
                        elif l == 'negative': 
                            total_neg += s
                            total_compound -= s*10
                        else: 
                            total_neu += s
                            total_compound += s*1
                sent_dict = {'neg': round(total_neg/num_split, 5), 
                             'neu': round(total_neu/num_split, 5), 
                             'pos': round(total_pos/num_split, 5), 
                             'compound': self.rescaling(total_compound, -10*num_split, 10*num_split)}
                
                if summarize is True: 
                    return sent_dict['compound']
                else: 
                    return sent_dict 
        except AttributeError: 
            raise SystemError("finBERT must be loaded in prior. Load the model via nlp.sentiment(load_models='finBERT')")

    #All models  
    def aggregate(self, 
                  text:str, 
                  text_type:str, 
                  summarize:bool=True) -> float or dict: 
        try: 
            if summarize is True: 
                # alphaVADER_c = self.alphaVADER(text, text_type=text_type)
                roBERTa_v1_c = self.twitter_roBERTa_v1(text, text_type=text_type)
                roBERTa_v2_c = self.twitter_roBERTa_v2(text, text_type=text_type)
                XLM_roBERTa_c = self.twitter_XLM_roBERTa(text, text_type=text_type)
                finBERT_c = self.finBERT(text, text_type=text_type)
                return {#'alphaVADER': alphaVADER_c,
                        'roBERTa_v1': roBERTa_v1_c,
                        'roBERTa_v2': roBERTa_v2_c,
                        'XLM_roBERTa': XLM_roBERTa_c,
                        'finBERT': finBERT_c, 
                        'total': round(np.mean([#alphaVADER_c, 
                                                roBERTa_v1_c, roBERTa_v2_c, XLM_roBERTa_c, finBERT_c]), 5)} 
            else:
                # alphaVADER_dict = self.alphaVADER(text, text_type=text_type, summarize=summarize)
                roBERTa_v1_dict = self.twitter_roBERTa_v1(text, text_type=text_type, summarize=summarize)
                roBERTa_v2_dict = self.twitter_roBERTa_v2(text, text_type=text_type, summarize=summarize)
                XLM_roBERTa_dict = self.twitter_XLM_roBERTa(text, text_type=text_type, summarize=summarize)
                finBERT_dict = self.finBERT(text, text_type=text_type, summarize=summarize)

                pos = [#alphaVADER_dict['pos'], 
                       roBERTa_v1_dict['pos'], roBERTa_v2_dict['pos'], XLM_roBERTa_dict['pos'], finBERT_dict['pos']]
                neg = [#alphaVADER_dict['neg'], 
                       roBERTa_v1_dict['neg'], roBERTa_v2_dict['neg'], XLM_roBERTa_dict['neg'], finBERT_dict['neg']]
                neu = [#alphaVADER_dict['neu'], 
                       roBERTa_v1_dict['neu'], roBERTa_v2_dict['neu'], XLM_roBERTa_dict['neu'], finBERT_dict['neu']]
                compound = [#alphaVADER_dict['compound'], 
                            roBERTa_v1_dict['compound'], roBERTa_v2_dict['compound'], XLM_roBERTa_dict['compound'], finBERT_dict['compound']]

                return {#'alphaVADER': alphaVADER_dict,
                        'roBERTa_v1': roBERTa_v1_dict,
                        'roBERTa_v2': roBERTa_v2_dict,
                        'XLM_roBERTa': XLM_roBERTa_dict,
                        'finBERT': finBERT_dict, 
                        'total': {'neg': round(np.mean(neg),5), 
                                  'neu': round(np.mean(neu),5), 
                                  'pos': round(np.mean(pos),5), 
                                  'compound': round(np.mean(compound),5)}} 
        except AttributeError: 
            raise SystemError("All models must be loaded in prior. Load the models via nlp.sentiment(load_models='all')")
