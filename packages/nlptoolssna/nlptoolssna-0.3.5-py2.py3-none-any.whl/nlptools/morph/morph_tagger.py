import pickle
from nlptools.morph import settings 
import re
from nlptools.morph.lemmatizeSentence import lemmatize_sentence
from nlptools.morph.tokenizers_words import simple_word_tokenize
from nlptools.parse.parser import arStrip
import os.path
from nlptools.DataDownload import downloader

def load_ALMA_dic():
   # Open the Pickle file in binary mode
    filename = '20230418test27012000.pickle'
    path =downloader.get_appdatadir()
    file_path = os.path.join(path, filename)
    

    with open(file_path, 'rb') as f:
       #Load the serialized data from the file
       ALMA_dic = pickle.load(f)
       #print(ALMA_dic)
       return ALMA_dic

def tag(word, lang, task):
    """
    given a token, this method retrives the possible morphological solutions (lemma, pos, and frequency) filterd by spesific
    language and task.
     
       in a dictionary to find its lemma, part of speech, and frequency,
    filtered by the specified language and task. The dictionary used is assumed to be a nested dictionary where keys
    are words and values are lists of lemma entries, where each lemma entry is a list of the form
    [form_id, form, pos_ar, lemma, lemma_freq, lang, task].

    Args:
        word (str): The Arabic word to be morphologcaly tagged.
        lang (str): The language to filter the results by [MSA, Pal, ].
        task (str): The task to filter the results by [lemmatizer, pos, full].

    Returns:
        list: A list of [word, lemma, pos_ar, lemma_freq, lang, task], where:
            - word: the original input word
            - lemma: the lemma of the word
            - pos_ar: the part of speech of the word in Arabic
            - lemma_freq: the frequency of the lemma in the dictionary @check:returen or not
            - lang: the input language value
            - task: the input task languge

            If no sloution is found for this word, an empty list is returned.
    """
    if word in settings.div_dic.keys():

        soluation =settings.div_dic[word][1]
        if task =='full' and soluation[-2] == lang:
            return  [word, soluation[3], soluation[2],  soluation[-2], soluation[-1]]
        elif soluation[-2] == lang and soluation[-1] ==task:
            return [word, soluation[3], soluation[2],  soluation[-2], soluation[-1]]
        return []
    else:
        return []

def lemmatize_sentence(text ,lang, task):
   """
    This method takes a text as input and returns a morphological solution for each token in this text, Based
    on the input language and task, such that:
    if task == lemmatizaer, then the morphological soltuion is only the lemma.
       task == pos, then the morphological soltuion is only the pos.
       task == full, the the morphological soltuion is both the lemma and the pos.
     
    the lang arguemet is used to help the morphological analysis to return more accurate solutions, for example if the sentence
    is MSA, or Palestinian dilect.
   

    Args:
    - text (str): The input text to morphologicaly analyzed.
    - task (str): The type of task being performed (e.g., 'lemmatizer', 'pos', or 'full').
    - lang (str): The language of the input sentence (e.g., 'MSA').

    Returns:
    - output_list (list): A list of morphological solution for each token in the input text.

    """
   output_list = []
   # tokenize sentence into words
   words = simple_word_tokenize(text)
   # for each word 
   for word in words:
         result_word =[]
         # Trim spaces 
         word = word.strip()
         # Remove smallDiac
         word = arStrip(word , False , True , False , False , False , False) 
         # Unify ٱ 
         word = re.sub('[ٱ]','ﺍ',word)
         # Initialize solution [word, lemma, pos]
         solution = [word,word+"_0","",0]
         
         # if word is digit, update pos to be digit 
         if word.isdigit():
            solution[2] = "digit"

         # if word is english, update pos to be ENGLISH
         elif re.match("^[a-zA-Z]*$", word):
            solution[2] = "ENGLISH"

         else:
            # search for a word (as is) in ALMA dictionary   
            result_word = tag(word,lang, task)
            
            if len(re.sub(r'^[ﻝ]','',re.sub(r'^[ﺍ]','',word))) > 5 and result_word == []:
               # try with remove remove AL
               result_word = tag(re.sub(r'^[ﻝ]','',re.sub(r'^[ﺍ]','',word)), lang, task)

            if result_word == []:
              # try with replace ﻩ with ﺓ
               result_word = tag(re.sub(r'[ﻩ]$','ﺓ',word), lang, task)

            if result_word == []:
               # try with unify Alef
               word_with_unify_alef = arStrip(word , False , False , False , False , True , False) # Unify Alef
               result_word = tag(word_with_unify_alef, lang, task)
            
            if result_word == []:
               # try with remove diac
               word_undiac = arStrip(word , True , False , True , True , False , False) # remove diacs, shaddah ,  digit
               result_word = tag(word_undiac, lang, task)

            if result_word == []:
               # try with remove diac and unify alef
               word_undiac = arStrip(word , True , True , True , False, True , False) # diacs , smallDiacs , shaddah ,  alif
               result_word = tag(word_undiac, lang, task)
         
         if result_word != []:
               # if solution found
               tmp_solution = [word,word+"_0","",0]               
               tmp_solution[1] = result_word[2] # lemma
               tmp_solution[2] = result_word[1] # pos_ar
               tmp_solution[3] = result_word[3] # lemma_freq
               output_list.append(tmp_solution)
         else:
            # if no solution is found
            output_list.append(solution)
   return output_list               
        
def tagger(text: str, task = 'full', lang = 'MSA') -> list:

    """
    This method takes an Arabic text as input, tokenize it into tokens and calles 
    the morphological tagger to return the morpological solution for each token in this text.
    There is not limit for the text size, but one should be resonable based on the available resources (computational power).
    @check

   @comment : text or sentence. 
    
    Args:
        text (str): The input Arabic sentence to be morphologically analyzed and tagged.
        task (str): The type of morphological analysis and tagging to be performed. Default is 'full'.
        lang (str): The language of the input sentence. Default is 'MSA' (Modern Standard Arabic).
        
    Returns:
        list: A list of lists, where each sublist contains information about a word in the input text, including 
              the original word, its lemma, its part of speech (POS) tag, and its lemma frequency.
    """
    
    # Check if the ALMA dictionary has been loaded
    if settings.flag == True:
        settings.flag = False
    settings.div_dic = load_ALMA_dic()
   
    
    # Perform lemmatization on the input sentence
    output_list = lemmatize_sentence(text,lang, task)
    
    # Return the list of lemmatized words
    return output_list

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    
    
    
    
    
