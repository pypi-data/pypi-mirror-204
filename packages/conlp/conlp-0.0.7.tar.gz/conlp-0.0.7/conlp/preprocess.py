
import unicodedata 
import re

class preprocess: 
    def tweets(text:str, 
               remove_hashtag:bool=True, 
               hashtag_exception:list=None) -> str:
        """
        Preprocesses tweets in a tidy manner, returning normalized text following NFKD unicode 

        Args:
            text (str): Raw tweet to be preprocessed. 
            remove_hashtag (bool, optional): Removes all existing hashtags in the raw tweet. Defaults to True.
            hashtag_exception (list, optional): Exempt removal of certain key hashtags. Defaults to None.

        Returns:
            str: Normalized text following NFKD unicode. 
        """
        
        processed_text = re.sub("http\S+", "", text)
        processed_text = re.sub("RT", "", processed_text)
        processed_text = re.sub("@\S+", "", processed_text)
        processed_text = re.sub("[\r\n]+", " ", processed_text)

        if remove_hashtag is False: 
            unicode_normalized_text = unicodedata.normalize('NFKD', processed_text)
        else: 
            if hashtag_exception is None: 
                processed_text = re.sub("#\S+", "", processed_text)
                unicode_normalized_text = unicodedata.normalize('NFKD', processed_text)
            else: 
                #check if tweet includes hashtags in hashtag_exception
                hashtag_exception = ['#'+hashtag for hashtag in hashtag_exception]
                hashtag_grammar = ""

                for txt in processed_text.split():
                    if '#' in txt.lower():
                        if txt.lower() in hashtag_exception: 
                            hashtag_grammar += " "+txt
                        else: 
                            pass
                    else:
                        hashtag_grammar += " "+txt

                unicode_normalized_text = unicodedata.normalize('NFKD', hashtag_grammar)

        unicode_normalized_text = re.sub(" {2,}", " ", unicode_normalized_text)

        return unicode_normalized_text
    
    def news(text:str):
        """Generate Docstring""" 
        processed_text = re.sub("http\S+", "", text)
        processed_text = re.sub("[\n]+", " ", processed_text)
        processed_text = re.sub("[\t]+", " ", processed_text)
        processed_text = re.sub("[\r\n]+", " ", processed_text)
        processed_text = re.sub(" {2,}", " ", processed_text)
        unicode_normalized_text = unicodedata.normalize('NFKD', processed_text)
        return unicode_normalized_text
