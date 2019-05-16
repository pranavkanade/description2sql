from utils.consts import *

from utils.utilities import (
    get_json_data, get_subjs, get_agg_input_vector,
    get_where_cond_val, get_cond_op_input_vector, get_num, get_nominal_subjects)

from .agg_predict import PredictAgg
from .op_predict import PredictCond

def get_where_col_act(doc, data=None):
    if data is not None:
        if len(data['sql']['conds']) > 0:
            return data['sql']['conds'][0][0]
    return None

def get_where_col(doc):
    nums = get_num(doc)
    ancestors = list(nums[0].ancestors)
    for p in ancestors:
        if p.pos_ in ["NOUN"]:
            return p
    root = None
    for p in ancestors:
#         print(p.text, p.pos_)
        if p.pos_ in ["VERB"]:
            root = p
            break
    nomi = get_nominal_subjects(root)
    if len(nomi) > 0:
        return nomi[0]
    return None  
    

class Predict():
    def __init__(self, question, pipe, data=None):
        self.question = question
        self.PIPE = pipe
        self.data = data
        self.sel_col = ""
        self.agg = ""
        self.where_col = ""
        self.cond_op = ""
        self.cond_val = ""
    
    def process_question(self, table_name, madeup=False):
        doc = self.PIPE(self.question)
        subjs = get_subjs(doc)
        self.sel_col = subjs[-1].text
        X_agg = get_agg_input_vector(subjs[0], doc)


        self.cond_val = (get_where_cond_val(doc)).text
        X_cond_op = get_cond_op_input_vector(doc)
        
        (agg_idx, op_idx) = self.predict_agg_n_op(X_agg, X_cond_op)
        self.agg = agg_ops[agg_idx]
        self.cond_op = cond_ops[op_idx]
        if not madeup:
            self.where_col = get_where_col_act(doc, self.data)
        else:
            self.where_col = (get_where_col(doc)).text
        query = "select "+ self.agg + "("+self.sel_col+") "+ "from "+ table_name + " where " + self.where_col + " " + self.cond_op + " " + self.cond_val + ";"
        return query
    
    def predict_agg_n_op(self, agg_x, op_x):
        agg_idx = PredictAgg().predict_agg(agg_x)
        op_idx = PredictCond().predict_cond_op(op_x)
        return (agg_idx, op_idx)
    
    def quality_check(self, data):
        if (str.lower(self.sel_col) in str.lower(data['sql']['sel']) and
            str.lower(self.agg) in str.lower(data['sql']['agg'])):
        
            if (len(data['sql']['conds']) > 0):
                if (str.lower(self.where_col) in str.lower(data['sql']['conds'][0][0]) and
                    str.lower(self.cond_op) in str.lower(data['sql']['conds'][0][1]) and
                    str.lower(self.cond_val) in str.lower(data['sql']['conds'][0][2])):
                    return True
                else:
                    return False
            return True
        else:
            return False
            
        