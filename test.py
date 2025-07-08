import numpy as np

result = {
    'equity': [10,12,33,23],
    'one_min_fee': 0.1
}

fee_equity = np.array(result['equity']) - result['one_min_fee']
print(fee_equity)