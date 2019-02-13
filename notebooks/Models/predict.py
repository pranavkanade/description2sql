from utils.consts import *

from utils.utilities import (
    get_json_data, get_subjs, get_agg_input_vector,
    get_where_cond_val, get_cond_op_input_vector)

from agg_predict import PredictAgg
from op_predict import PredictCond

def get_where_col(doc, data=None):
    if data is not None:
        if len(data['sql']['conds']) > 0:
            return data['sql']['conds'][0][0]
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
    
    def process_question(self):
        doc = self.PIPE(self.question)
        subjs = get_subjs(doc)
        self.sel_col = subjs[0]
        X_agg = get_agg_input_vector(self.sel_col, doc)

        self.cond_val = get_where_cond_val(doc)
        X_cond_op = get_cond_op_input_vector(doc)
        
        (agg_idx, op_idx) = self.predict_agg_n_op(X_agg, X_cond_op)
        self.agg = agg_ops[agg_idx]
        self.cond_op = cond_ops[op_idx]

        self.where_col = get_where_col(doc, self.data)
        print("select", self.agg, self.sel_col, "where", self.where_col, self.cond_op, self.cond_val)
        return
    
    def predict_agg_n_op(self, agg_x, op_x):
        agg_idx = PredictAgg().predict_agg(agg_x)
        op_idx = PredictCond().predict_cond_op(op_x)
        return (agg_idx, op_idx)