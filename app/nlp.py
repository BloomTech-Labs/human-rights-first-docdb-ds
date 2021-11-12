import spacy

import re

nlp = spacy.load("en_core_web_sm")

def get_entities_and_years(text):
    """Get (1) named entities and (2) years from text using SpaCy NER"""
    text = re.sub('[§@]', '', text)
    text = re.sub(r'\s+', ' ', text)
    doc = nlp(text)
    entities = doc.ents # We might want to exclude date labels from entities, since we are getting years separately
    years = [re.search("\d{4}", e.text).group(0) for e in doc.ents if e.label_ == 'DATE' and re.search("\d{4}", e.text)]
    return entities, years

if __name__ == '__main__':
    some_text = """me (@ CONFIDENTIAL LONDON COPIES BY MUFAX ce PS/Secretar, of § és PUS. ¥ of, 
    Rate DUST IEA Mr Pritché Pn N10. Mr Cradock "ple Mr Middleton HMA, Dublin Mr Mallet, RID FCO INCREASE IN UDR 
    CONRATES when I saw Mr Donlon in Dublin on Friday he left me in no doubt that in his view the increase in the number 
    of UDR Conrates announced by the Secretary of State would be badly received in the Republic. He asked me
     what I really thought of the regiment. I told nim that I had visited UDR units and been out' on patrol 
     with them and had formed a great admiration for them. He said that he did not doubt that they put on a good 
     show for visitors. The fact was that the regiment had a bad record of misbehaviour and there had been too many 
     cases for us to explain them away with our "bad apple stories". He himself had recently suffered at their hands. 
     and when the incident occurred, a been stopped by a UDR VCP in the southern part of the Province and when the members 
     of the patrol saw thdt nis car had a...
     Test years function:
     This event happened in 4/2/1991 and and another test in 5/4/2003 and another test april 2020"""


    print(get_entities_and_years(some_text))
