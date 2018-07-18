import numpy as np
from tqdm import tqdm
from sklearn.metrics import roc_auc_score, r2_score


def empirical_loglik():
  """
  Calculate the empirical log-likihood.
  """
  pass

def calculate_concordance_dead_only(preds, ys, cs):
  """
  Calculate C-statistic for only cases where outcome is uncensored.
  """
  return calculate_concordance_naive(np.array(preds[cs == 0]), 
                                     np.array(ys[cs == 0]), 
                                     np.array(cs[cs == 0]))
    

def calculate_concordance_naive(preds, ys, cs):
  """
  Calculate Harrell's C-statistic in the presence of censoring.

  Cases:
  - (c=0, c=0): both uncensored, can compare
  - (c=0, c=1): can compare if true censored time > true uncensored time
  - (c=1, c=0): can compare if true censored time > true uncensored time
  - (c=1, c=1): both censored, cannot compare
  """
  trues = ys
  concordance, N = 0, len(trues)
  counter = 0
  for i in tqdm(range(N)):
    for j in range(i + 1, N):
      if (not cs[i] and not cs[j]) or \
         (not cs[i] and cs[j] and ys[i] < ys[j]) or \
         (cs[i] and not cs[j] and ys[i] > ys[j]):
        if (preds[i] < preds[j] and trues[i] < trues[j]) or \
           (preds[i] > preds[j] and trues[i] > trues[j]):
            concordance += 1
        elif preds[i] == preds[j]:
          concordance += 0.5
        counter += 1
  return concordance / counter
