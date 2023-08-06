KeypartX, a graph-based approach to represent perception (text in general) by key parts of speech.

if need coreferee: 
!pip install keypartx[coreferee_spacy]
!python3 -m coreferee install en
!python -m spacy download en_core_web_lg

else:
!pip install spacy
!pip install keypartx 
!python -m spacy download en_core_web_lg


