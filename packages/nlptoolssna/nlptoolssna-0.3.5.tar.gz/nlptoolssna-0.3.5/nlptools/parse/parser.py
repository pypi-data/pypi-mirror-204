import re 

def arStrip(input_str , diacs , smallDiacs , shaddah ,  digit , alif , specialChars ):

    try:
        if input_str: # if the input string is not empty do the following
            #print("in if")
            if diacs == True :
                input_str = re.sub(r'[\u064B-\u0650]+', '',input_str) # Remove all Arabic diacretics [ ًٌٍَُِْ]
                input_str = re.sub(r'[\u0652]+', '',input_str) # Remove SUKUN
            if shaddah == True:
                input_str = re.sub(r'[\u0651]+', '',input_str) # Remove shddah
            if smallDiacs == True:
                input_str = re.sub(r'[\u06D6-\u06ED]+', '',input_str) # Remove all small Quranic annotation signs
            if digit == True:
                input_str = re.sub('[0-9]+', ' ',input_str) # Remove English digits
                input_str = re.sub('[٠-٩]+', ' ',input_str)# Remove Arabic digits
            
            if alif == True:                             # Unify alif with hamzah: 
                input_str = re.sub('ٱ', 'ا',input_str);
                input_str = re.sub('أ', 'ا',input_str);
                input_str = re.sub('إ', 'ا',input_str);
                input_str = re.sub('آ', 'ا',input_str);
            if specialChars == True:
                input_str = re.sub('[?؟!@#$%-]+' , '' , input_str) # Remove some of special chars 

            input_str = re.sub('[\\s]+'," ",input_str) # Remove all spaces
            input_str = input_str.replace("_" , '') #Remove underscore
            input_str = input_str.replace("ـ" , '') # Remove Arabic tatwelah
            input_str = input_str.strip() # Trim input string
    except:
        return input_str
    return input_str
    
    
def removePunctuation( inputString ):
    """
    Removes punctuation marks from the input string.
    
    Args:
    inputString (str): The input string containing punctuation marks.
    
    Returns:
    str: The output string with all punctuation marks removed.
    
    Raises:
    None
    """
    outputString = inputString
    try:
        if inputString:
            # English Punctuation
            outputString = re.sub(r'[\u0021-\u002F]+', '',inputString) # ! " # $ % & ' ( ) * + ,  - . /
            outputString = re.sub(r'[U+060C]+', '',outputString) # ! " # $ % & ' ( ) * + ,  - . /
            outputString = re.sub(r'[\u003A-\u0040]+', '',outputString) # : ; < = > ? @ 
            outputString = re.sub(r'[\u005B-\u0060]+', '',outputString) # [ \ ] ^ _ `
            outputString = re.sub(r'[\u007B-\u007E]+', '',outputString) # { | } ~
            # Arabic Punctuation
            outputString = re.sub(r'[\u060C]+', '',outputString) # ،
            outputString = re.sub(r'[\u061B]+', '',outputString) # ؛
            outputString = re.sub(r'[\u061E]+', '',outputString) # ؞
            outputString = re.sub(r'[\u061F]+', '',outputString) # ؟
            outputString = re.sub(r'[\u0640]+', '',outputString) # ـ
            outputString = re.sub(r'[\u0653]+', '',outputString) # ٓ
            outputString = re.sub(r'[\u065C]+', '',outputString) #  ٬
            outputString = re.sub(r'[\u066C]+', '',outputString) #  ٜ 
            outputString = re.sub(r'[\u066A]+', '',outputString) # ٪
            outputString = re.sub(r'["}"]+', '',outputString) 
            outputString = re.sub(r'["{"]+', '',outputString) 
            # outputString = re.sub(r'[\u066B]+', '',outputString) # ٫ 
            # outputString = re.sub(r'[\u066D ]+','',outputString) # ٭
            # outputString = re.sub(r'[\u06D4 ]+','',outputString) # ۔
    except:
        return inputString
    # print(outputString)
    return outputString

def removeEnglish( inputString ):
    """
    Removes all English characters from the input string.

    Args:
    - inputString (str): The string to remove English characters from.

    Returns:
    - outputString (str): The input string with all English characters removed.
    If an error occurs during processing, the original input string is returned.
    """
    try:
        if inputString:
            inputString = re.sub('[a-zA-Z]+', ' ',inputString)
    except:
        return inputString
    return inputString
# print(removeEnglish("miojkdujhvaj1546545spkdpoqfoiehwv nWEQFGWERHERTJETAWIKUYFC"))
# print(removePunctuation("te!@#،$%%؟st") )
# Example
# print(arStrip( " مَحًمٌٍُِ" ,True ,True ,True ,True ,False , True ))

