import pandas as pd
import numpy as np
import sqlite3
from Optimiztion.models_nn.linear_models import NLSNN1
from Optimiztion.models_nn.utils import *

model = NLSNN1(7)

filepath = generate_neural_filename(model,[64, 32],'modelML/_nls_models')
save_neural_weights(model,filepath)