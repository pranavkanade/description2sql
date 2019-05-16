from utils.consts import *

from utils.utilities import (
    get_json_data, get_subjs, get_agg_input_vector,
    get_where_cond_val, get_cond_op_input_vector)

from utils.predict import Predict
from utils.agg_predict import PredictAgg
from utils.op_predict import PredictCond

import pickle
import json
from pprint import pprint
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.WARN)
import numpy as np

import spacy
PIPE = spacy.load('en_core_web_lg')
# PIPE = spacy.load('en_coref_lg')

data = get_json_data('./data_with_num/dev_dataset.json')

d1 = data[0]

print(d1['question'])

p1 = Predict(d1['question'], PIPE, d1)

p1.process_question()