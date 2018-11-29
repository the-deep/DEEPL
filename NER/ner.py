from nltk.tag import StanfordNERTagger
import re

from classifier.models import ClassifiedDocument
from NER.models import NERCache

MONTHS = [
        'january', 'february', 'march', 'april', 'may', 'june', 'july',
        'august', 'september', 'october', 'november', 'december'
]
MONTHS_INITIALS = list(map(lambda x: x[:3], MONTHS))
TIMES = ['midnight', 'afternoon', 'noon', 'evening', 'morning', 'night']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday']


def get_ner_tagging_doc(docid):
    """
    Get NER tagged data for docoument with given docid
    Returns: <tagged_data>, <cached or not: True/False>
    """
    try:
        cache = NERCache.objects.get(classified_doc__id=docid)
    except NERCache.DoesNotExist:
        pass
    else:
        return cache.ner_data, True
    # no cache exists
    try:
        doc = ClassifiedDocument.objects.get(id=docid)
    except ClassifiedDocument.DoesNotExist:
        return {}, False
    else:
        tagged_data = get_ner_tagging(doc.text)
        # create cache object
        NERCache.objects.create(classified_doc=doc, ner_data=tagged_data)
        return tagged_data, False


def get_ner_tagging(text):
    # Split the text using regex (to record their split positions)
    matches = re.finditer(r'\S+', text)
    splits = [(m.group(0), (m.start(), m.end() - m.start()))
              for m in matches]

    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
    tags = st.tag([s[0] for s in splits])

    result = []
    for i, tag in enumerate(tags):
        if tag[1] != 'O':
            split = splits[i][1]
            result.append({
                'start': split[0],
                'length': split[1],
                'entity': tag[1],
            })
        else:
            result.append(None)

    combined_result = []
    prev_item = None
    for item in result:
        if not prev_item:
            prev_item = item
        elif item and item['entity'] == prev_item['entity']:
            prev_item['length'] = (item['start'] - prev_item['start']) + \
                item['length']
        else:
            combined_result.append(prev_item)
            prev_item = item

    if prev_item:
        combined_result.append(prev_item)

    return combined_result


def ___get_ner_tagging(text):
    """text is unsplitted text"""
    # date_txts = []
    # date_tagged = get_date_tagged(text)
    # splitted = date_tagged.split()
    # new_splitted = []
    # for x in splitted:
    #     if re.match('\*\*.*\*\*', x):
    #         date_txts.append(x.split('**')[1])
    #         new_splitted.append('DATETIME')
    #     else:
    #         new_splitted.append(x)
    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
    tagged = st.tag(text.strip().split())
    # tagged = st.tag(new_splitted)

    return tagged
    # count = 0
    # final = []
    # for x, tag in tagged:
    #     if x == 'DATETIME':
    #         final.append((date_txts[count].replace('_', ' '), 'DATETIME'))
    #         count += 1
    #     else:
    #         final.append((x, tag))
    # return final


def get_date_tagged(text):
    splitted = text.strip().split()
    new = []
    for x in splitted:
        if x.lower() in DAYS:
            new.append('**{}**'.format(x))
        elif x.lower() in MONTHS:
            new.append('**{}**'.format(x))
            # new.append('**M**')
        elif x.lower() in MONTHS_INITIALS:
            new.append('**{}**'.format(x))
            # new.append('**M**')
        elif re.match('\d{4}', x):
            new.append('**{}**'.format(x))
        elif re.match('\d{1,2}', x):
            new.append('**{}**'.format(x))
        elif re.match('\d{1,2}[\-/]\d{1,2}[\-/]\d{4}', x):
            new.append('**{}**'.format(x))
            # new.append('**N4**')
        elif re.match('\d{4}[\-/]\d{1,2}[\-/]\d{1,2}', x):
            new.append('**{}**'.format(x))
        elif x.lower() in TIMES:
            new.append('**{}**'.format(x))
            # new.append('**T**')
        elif re.match('\d{4}[\-/]', x):
            new.append('**{}**'.format(x))
        elif re.match('\d{1,2}[\-/]', x):
            new.append('**{}**'.format(x))
        # NOTE: the following do not work because it has been splitted by space
        elif re.match('\d{1,2} *[aApP].{0,1}[mM]', x.lower()):
            new.append('**{}**'.format(x))
            # new.append('**T**')
        elif re.match('\d{1,2} *: *\d2 *[aApP].{0,1}[mM]', x.lower()):
            new.append('**{}**'.format(x))
        elif re.match('\d{1,2} *o\'* *clock', x.lower()):
            new.append('**{}**'.format(x))
        else:
            new.append(x)
    # now merge
    index = 0
    merged = []
    while index < len(new):
        if re.match('\*\*.*\*\*', new[index]):
            txts = []
            while (index < len(new) and (new[index] in ['/', '-'])
                    or re.match('\*\*.*\*\*', new[index])):
                txts.append(new[index].split('**')[1])
                index += 1
            txt = '_'.join(txts)
            merged.append('**{}**'.format(txt))
            if index < len(new):
                merged.append(new[index])
        else:
            merged.append(new[index])
        index += 1
    return ' '.join(merged)
