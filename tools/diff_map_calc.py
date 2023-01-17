import numpy as np
import pandas as pd
from pyperclip import copy
from edc_converter import to_rows, to_edcsuite

if __name__ == '__main__':
  np.set_printoptions(precision=2)

  first = np.array(to_rows()).astype("int")
  input("select second map then press Enter")
  second = np.array(to_rows()).astype("int")
  
  print("First array:")
  print(first)
  print("--------")
  print("Second array:")
  print(second)
  print("--------")
  print("Differences:")
  
  diffs = np.subtract(second, first)
  print(diffs)
  
  print("--------")
  print("Excel friendly:")
  for row in diffs:
    for col in row:
      print(col, end="\t")
    print()
    
  df = pd.DataFrame(diffs)
  df.to_excel('excel.xlsx', index = True)