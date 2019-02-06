from utils.consts import *
import json
import spacy
from pprint import pprint

def get_data(path):
    with open(path, 'r') as fp:
        json_data = json.load(fp)
    return json_data

def printmd(string, color=None):
    colorstr = "<span style='color:{}'>{}</span>".format(color, string)
    display(Markdown(colorstr))

def show_dep(doc):
    options = {'compact':True,
               'collapse_punct':False,
               'collapse_phrases':True,
               'color': 'white',
               'font': 'Source Sans Pro',
               'bg': '#09a3d5'}
    spacy.displacy.render(doc, jupyter=True, style='dep')

# get the root
def get_root(doc):
    # There is always a single root for a sentence.
    # This is just a safety guard
    roots = list()
    for word in doc:
        if word.head == word:
            roots.append(word)
    if len(roots) != 1:
        return None
    return roots[0]

# get nominal subjects
def get_nominal_subjects(root):
    subject_list = list()
    for child in root.children:
        if child.pos_ in NOUNS_POS and child.dep_ in SUBJECT_DEP:
            subject_list.append(child)
    return subject_list

# get the nsubjs
def get_nsubjs(noun):
    conjs = list()
    conjs.append(noun)
    for child in noun.children:
        if child.pos_ in NOUNS_POS and child.dep_ in AND:
            conjs.extend(get_nsubjs(child))
    return conjs

def get_compound(noun):
    compound_candidates = list()
    compound_candidates.append(noun)
    for child in noun.children:
        if (child.pos_ in NOUNS_POS or child.pos_ in DET_POS) and child.dep_ in COMPOUND_DEP:
            compound_candidates.extend(get_compound(child))
    return compound_candidates

# Find the `appos`
# Check if there is chain of `VERB --(nsubj)--> NOUN --(appos)--> NOUN`
def get_appos(noun):
    # Assume that there will be only one appos
    for child in noun.children:
        if child.pos_ in NOUNS_POS and child.dep_ in APPOS:
            return child
    return None

def get_prep(noun):
    # assume there will be only one of these attached to the main noun
    prep = []
    for child in noun.children:
        if child.pos_ in PREP_POS and child.dep_ in PREPOSITIONAL_MOD:
            prep.append(child)
    if len(prep) > 0:
        return prep[-1]
    else:
        return None

def get_attributes(nominal_subj):
    appos_noun = get_appos(nominal_subj)
    if appos_noun is None:
        return get_nsubjs(nominal_subj)
    else:
        return get_nsubjs(appos_noun)
    
def get_objects(prep):
    for child in prep.children:
        if child.pos_ in NOUNS_POS and child.dep_ in OBJ_PREPOSITION:
            return child
    return None

def get_table_attr(main_obj):
    # Check if there, relative clause modifier
    relative_verb = None
    # check if 'relcl'
    for child in main_obj.children:
        if child.pos_ in VERB and child.dep_ in RELATIVE_CLAUSE_MOD:
            relative_verb = child
            break
    intermediate_prep = None
    # If there isn't then, check the for prep.
    if relative_verb is None:
        intermediate_prep = get_prep(main_obj)
    else:
        intermediate_prep = get_prep(relative_verb)
    objs = get_objects(intermediate_prep)
    return [main_obj, objs]

def get_attrs_n_objects(text):
    doc = nlp_pipe(text)
    text_root = get_root(doc)
    attributes = get_attributes(get_nominal_subjects(text_root)[0])
    main_prep = get_prep(attributes[0])
    main_object = get_objects(main_prep)
    all_objects = get_table_attr(main_object)
    attributes = [get_compound(attr) for attr in attributes]
    all_objects = [get_compound(obj) for obj in all_objects]
    return attributes, all_objects

def join(list_attrs):
    return [" ".join([a.text for a in attrs]) for attrs in list_attrs]

def test(doc):
    text_root = get_root(doc)
    print("root : {}".format(text_root))
    # I'll just be testing the first subjs
    nominal_subjs = get_nominal_subjects(text_root)
    print("nsubj : {}".format(nominal_subjs[0]))
    if len(nominal_subjs) > 1:
        print("There are more subjs are attached to ROOT")
    attrs = get_attributes(nominal_subjs[0])
    print("Attributes :")
    pprint([get_compound(attr) for attr in attrs])
    main_prep = get_prep(attrs[0])
    print("Prep : {}".format(main_prep))
    main_object = get_objects(main_prep)
    print("Objects : {}".format(main_object))
    all_objs = get_table_attr(main_object)
    print("All objs : ")
    pprint([get_compound(obj) for obj in all_objs])
    show_dep(doc)
    
def get_verb_and_subj_pair(data_sample):
    # get the doc representation of the string
    doc = PIPE(data_sample['question'])
    # Find out the root of the given statement
    root = get_root(doc)
    # Some times the root can be a noun, in that case it'll always be associated to
    # an aux verb, and we gotta find it
    aux = get_aux(root)
    # If there is any aux found, we use it as our verb root
    if aux is not None and len(aux) > 0:
        vb = aux[0]
    else:
        # Else, we use our root as it is
        vb = root
    # nominals in this case is going to be a list of all the cols
    # in SELECT clause. If we find any nsubj attached to the root_verb we catch it here.
    nominals = get_nominal_subjects(vb)
    is_wh = False
    # If what we have found is not actually a noun but a question noun (wh-word)
    # TODO: In this case we may want to go on hunt for the actual nominal col.
    if len(nominals) != 0:
        is_wh = check_if_wh(nominals)
    if is_wh:
        # for now
        pass
    # Even after all this if there is no way the prog have found a nominal
    # find out if there is any prop attached to the verb.
    # If there is then we may look for prep_obj attached to it for the nominal.
    prep = None
    if len(nominals) == 0:
        prep = get_prep(root)
    pobj = None
    if prep is not None:
        pobj = get_objects(prep)
        nominals.append(pobj)
    return nominals