## POS
VERB = ["VERB"]
### NOUNS -
NOUNS_POS = ["NOUN", "PROPN", "ADJ", "PRON"]
PREP_POS = ["ADP"]
DET_POS = ["DET"]

## Dep
SUBJECT_DEP = ["nsubj", "nsubjpass"]
COMPOUND_DEP = ["compound"]
PREPOSITIONAL_MOD = ["prep"]
OBJ_PREPOSITION = ["pobj"]
RELATIVE_CLAUSE_MOD = ["relcl"]
APPOS = ["appos"]
AND = ["conj"]
AUX = ["aux", "auxpass"]
CASUAL_SUBJECT = ["csubj", "csubjpass"]
ADJECTIVES = ["amod", "acomp"]

## Tag
WH = ["WP", "WP$", "WDT"]



## SQL keys
agg_ops = ['', 'MAX', 'MIN', 'COUNT', 'SUM', 'AVG']
cond_ops = ['=', '>', '<', 'OP']
syms = ['SELECT', 'WHERE', 'AND', 'COL', 'TABLE', 'CAPTION', 'PAGE', 'SECTION', 'OP', 'COND', 'QUESTION', 'AGG', 'AGGOPS', 'CONDOPS']