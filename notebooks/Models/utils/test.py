def get_verb_and_subj_pair(data_sample):
    # Get the doc obj
    doc = PIPE(data_sample['question'])
    # Find out the root of the given statement
    root = get_root(doc)
    is_verb = _is_verb(root)
    aux = None
    # Some times the root can be a noun, in that case it'll always be associated to
    # an aux verb, and we gotta find it
    aux = get_aux(root)
    # If there is any aux found, we use it as our verb root
    if aux is not None and len(aux) > 0:
        root_verb = aux[0]
    else:
        # Else, we use our root as it is
        root_verb = root
    # Check if there is any csubj attached this means we have two wh nouns attached to
    # two different verbs one is asking and other qualifying.
    csubj_verb = get_csubj(root_verb)
    if csubj_verb is not None:
        root_verb = csubj_verb
#     print("ROOT : {}".format(root.text))
#     print("AUX : ")
#     pprint(aux)
    # nominals in this case is going to be a list of all the cols
    # in SELECT clause. If we find any nsubj attached to the root_verb we catch it here.
    nominals = get_nominal_subjects(root_verb)
    is_wh = False
    # If what we have found is not actually a noun but a question noun (wh-word)
    # TODO: In this case we may want to go on hunt for the actual nominal col.
    if len(nominals) != 0:
        is_wh = check_if_wh(nominals)
    if is_wh:
        # for now
        pass
#     print("SUBJ : ")
#     pprint(nominals)
    # Even after all this if there is no way the prog have found a nominal
    # find out if there is any prop attached to the verb.
    # If there is then we may look for prep_obj attached to it for the nominal.
    prep = None
    if len(nominals) == 0:
        prep = get_prep(root_verb)
#     print("PREP : ")
#     pprint(prep)
    pobj = None
    if prep is not None:
        pobj = get_objects(prep)
        nominals.append(pobj)
#     print("POBJ : ")
#     pprint(pobj)
#     show_dep(doc)
    return nominals
