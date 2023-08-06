import subprocess
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM

class download:
    def __init__(self, 
                 models:str or list):
        """
        Downloads Huggingface Natural Language Processing Models in the local environment.  

        Args:
            models (str or list): Target models to download. 
            Available models include ['twitter_roBERTa_v1', 'twitter_roBERTa_v2', 'twitter_XLM_roBERTa', 'finBERT', 'cnn_dailymail_BART', 'xsum_BART', 'cnn_dailymail_distilBART', 'xsum_distilBART','cnn_dailymail_PEGASUS', 'multi_news_PEGASUS', 'bloomberg_PEGASUS', 'keyBERT', 'mnli_distilBART']
        """
        available_models = [#Sentiment Classification 
                            'twitter_roBERTa_v1', 'twitter_roBERTa_v2', 'twitter_XLM_roBERTa', 'finBERT', 
                            #Text Summarization 
                            'cnn_dailymail_BART', 'xsum_BART', 'cnn_dailymail_distilBART', 'xsum_distilBART',
                            'cnn_dailymail_PEGASUS', 'multi_news_PEGASUS', 'bloomberg_PEGASUS', 
                            #KeyWord Extraction & Zero-Shot Classification 
                            'keyBERT', 'mnli_distilBART']
        
        if isinstance(models, str): 
            models = [models]
        elif isinstance(models, list): 
            pass
        else: 
            raise ValueError("Input models must be either str or list")
        
        for model in models:
            if model in available_models: 
                pass
            else: 
                raise ValueError("""'models' includes input '{}', which is not supported. SUPPORTED MODELS:
                    (i) Sentiment Classification - 'twitter_roBERTa_v1', 'twitter_roBERTa_v2', 'twitter_XLM_roBERTa', 'FinBERT'; 
                    (ii) Text Summarization - 'cnn_dailymail_BART', 'xsum_BART', 'cnn_dailymail_distilBART', 'xsum_distilBART', 'cnn_dailymail_PEGASUS', 'multi_news_PEGASUS', 'bloomberg_PEGASUS'; 
                    (iii) Zero-Shot Classification & Keyword Extraction - 'keyBERT', 'mnli_distilBART'""".format(model))
        
        path = Path().resolve()
        
        for model in models: 
            if model == 'alphaVADER': 
                print("""Installing alphaVADER by [SocialScienceAI] in your local environment...\n(for more details, see https://)""")
                #multiple dictionaries will be added in the future
                import alphaVADER 
                print(r'├── package alphaVADER successfully installed at FILE PATH: {}'.format(alphaVADER.__file__))
                print('\n')
            elif model == 'twitter_roBERTa_v1': 
                print("""Installing twitter_roBERTa_v1, a model trained and finetuned by [cardiffnlp] in your local environment...\n(for more details, see https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)""")
                GET_MODEL_PATH = 'cardiffnlp/twitter-roberta-base-sentiment'
                twitter_roBERTa_v1_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                twitter_roBERTa_v1 = AutoModelForSequenceClassification.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'twitter_roBERTa_v1'
                twitter_roBERTa_v1_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                twitter_roBERTa_v1.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── twitter_roBERTa_v1 successfully installed at FILE PATH: {}\twitter_roBERTa_v1'.format(path))
                print('\n')
            elif model == 'twitter_roBERTa_v2': 
                print("""Installing twitter_roBERTa_v2, a model trained and finetuned by [cardiffnlp] in your local environment...\n(for more details, see https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)""")
                GET_MODEL_PATH = 'cardiffnlp/twitter-roberta-base-sentiment-latest'
                twitter_roBERTa_v2_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                twitter_roBERTa_v2 = AutoModelForSequenceClassification.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'twitter_roBERTa_v2'
                twitter_roBERTa_v2_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                twitter_roBERTa_v2.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── twitter_roBERTa_v2 successfully installed at FILE PATH: {}\twitter_roBERTa_v2'.format(path))
                print('\n')
            elif model == 'twitter_XLM_roBERTa': 
                print("""Installing twitter_XLM_roBERTa, a model trained and finetuned by [cardiffnlp] in your local environment...\n(for more details, see https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment)""")
                GET_MODEL_PATH = 'cardiffnlp/twitter-xlm-roberta-base-sentiment'
                XLM_roBERTa_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                XLM_roBERTa = AutoModelForSequenceClassification.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'twitter_XLM_roBERTa'
                XLM_roBERTa_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                XLM_roBERTa.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── twitter_XLM_roBERTa successfully installed at FILE PATH: {}\twitter_XLM_roBERTa'.format(path))
                print('\n')
            elif model == 'finBERT': 
                print("""Installing finBERT, a model trained and finetuned by [ProsusAI] in your local environment...\n(for more details, see https://huggingface.co/ProsusAI/finbert)""")
                GET_MODEL_PATH = 'ProsusAI/finbert'
                FinBERT_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                FinBERT = AutoModelForSequenceClassification.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'finBERT'
                FinBERT_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                FinBERT.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── finBERT successfully installed at FILE PATH: {}\finBERT'.format(path))
                print('\n')
            
            elif model == 'cnn_dailymail_BART':
                print("""Installing cnn_dailymail_BART, a model trained and finetuned by [facebook] in your local environment...\n(for more details, see https://huggingface.co/facebook/bart-large-cnn)""") 
                GET_MODEL_PATH = 'facebook/bart-large-cnn'
                cnn_BART_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                cnn_BART = AutoModelForSeq2SeqLM.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'cnn_dailymail_BART' 
                cnn_BART_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                cnn_BART.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── cnn_dailymail_BART successfully installed at FILE PATH: {}\cnn_dailymail_BART'.format(path))
                print('\n')
            elif model == 'xsum_BART': 
                print("""Installing xsum_BART, a model trained and finetuned by [facebook] in your local environment...\n(for more details, see https://huggingface.co/facebook/bart-large-xsum)""") 
                GET_MODEL_PATH = 'facebook/bart-large-xsum'
                xsum_BART_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                xsum_BART = AutoModelForSeq2SeqLM.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'xsum_BART' 
                xsum_BART_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                xsum_BART.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── xsum_BART successfully installed at FILE PATH: {}\xsum_BART'.format(path))
                print('\n')
            elif model == 'cnn_dailymail_distilBART': 
                print("""Installing cnn_dailymail_distilBART, a model trained by [facebook] and distilled by [sshleifer] in your local environment...\n(for more details, see https://huggingface.co/sshleifer/distilbart-cnn-12-6)""") 
                GET_MODEL_PATH = 'sshleifer/distilbart-cnn-12-6'
                cnn_distilBART_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                cnn_distilBART = AutoModelForSeq2SeqLM.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'cnn_dailymail_distilBART' 
                cnn_distilBART_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                cnn_distilBART.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── cnn_dailymail_distilBART successfully installed at FILE PATH: {}\cnn_dailymail_distilBART'.format(path))
                print('\n')
            elif model == 'xsum_distilBART': 
                print("""Installing xsum_distilBART, a model pretrained by [facebook] and distilled by [sshleifer] in your local environment...\n(for more details, see https://huggingface.co/sshleifer/distilbart-xsum-12-6)""") 
                GET_MODEL_PATH = 'sshleifer/distilbart-xsum-12-6'
                xsum_distilBART_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                xsum_distilBART = AutoModelForSeq2SeqLM.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'xsum_distilBART' 
                xsum_distilBART_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                xsum_distilBART.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── xsum_distilBART successfully installed at FILE PATH: {}\xsum_distilBART'.format(path))
                print('\n')
            elif model == 'cnn_dailymail_PEGASUS': 
                print("""Installing cnn_dailymail_PEGASUS, a model trained and finetuned by [google] in your local environment...\n(for more details, see https://huggingface.co/google/pegasus-cnn_dailymail)""") 
                GET_MODEL_PATH = 'google/pegasus-cnn_dailymail'
                cnn_PEGASUS_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                cnn_PEGASUS = AutoModelForSeq2SeqLM.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'cnn_dailymail_PEGASUS' 
                cnn_PEGASUS_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                cnn_PEGASUS.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── cnn_dailymail_PEGASUS successfully installed at FILE PATH: {}\cnn_dailymail_PEGASUS'.format(path))
                print('\n')
            elif model == 'multi_news_PEGASUS': 
                print("""Installing multi_news_PEGASUS, a model trained and finetuned by [google] in your local environment...\n(for more details, see https://huggingface.co/google/pegasus-multi_news)""") 
                GET_MODEL_PATH = 'google/pegasus-cnn_dailymail'
                multi_PEGASUS_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                multi_PEGASUS = AutoModelForSeq2SeqLM.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'multi_news_PEGASUS' 
                multi_PEGASUS_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                multi_PEGASUS.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── multi_news_PEGASUS successfully installed at FILE PATH: {}\multi_news_PEGASUS'.format(path))
                print('\n')
            elif model == 'bloomberg_PEGASUS': 
                print("""Installing bloomberg_PEGASUS, a model pretrained by [google] and finetuned by [MedoidAI] in your local environment...\n(for more details, see https://huggingface.co/human-centered-summarization/financial-summarization-pegasus)""") 
                GET_MODEL_PATH = 'human-centered-summarization/financial-summarization-pegasus'
                bloomberg_PEGASUS_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                bloomberg_PEGASUS = AutoModelForSeq2SeqLM.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'bloomberg_PEGASUS' 
                bloomberg_PEGASUS_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                bloomberg_PEGASUS.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── bloomberg_PEGASUS successfully installed at FILE PATH: {}\bloomberg_PEGASUS'.format(path))
                print('\n')
            
            elif model == 'keyBERT': 
                print("""Installing keyBERT, a model pretrained by [MaartenGr] in your local environment...\n(for more details, see https://github.com/MaartenGr/KeyBERT)""")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "keyBERT"])
                from keybert import KeyBERT
                KeyBERT()
                print(r'├── package keyBERT successfully installed at FILE PATH: {}'.format(keybert.__file__))
                print('\n')
            elif model == 'mnli_distilBART':
                print("""Installing mnli_distilBART, a model pretrained by [facebook] and distilled by [valhalla] in your local environment...\n(for more details, see https://huggingface.co/valhalla/distilbart-mnli-12-9)""") 
                GET_MODEL_PATH = 'valhalla/distilbart-mnli-12-9'
                distilBART_tokenizer = AutoTokenizer.from_pretrained(GET_MODEL_PATH)
                distilBART = AutoModelForSequenceClassification.from_pretrained(GET_MODEL_PATH)
                SAVE_MODEL_PATH = 'mnli_distilBART' 
                distilBART_tokenizer.save_pretrained(SAVE_MODEL_PATH)
                distilBART.save_pretrained(SAVE_MODEL_PATH)
                print(r'├── mnli_distilBART successfully installed at FILE PATH: {}\mnli_distilBART'.format(path))
                print('\n')
