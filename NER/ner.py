from nltk.tag import StanfordNERTagger

def get_ner_tagging(text):
	"""text is splitted text"""
	st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
	return st.tag(text)	
