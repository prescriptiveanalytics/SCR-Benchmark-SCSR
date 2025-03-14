from SCRBenchmark import FEYNMAN_SRSD_HARD,HARD_NOISE_LEVELS,HARD_SAMPLE_SIZES
from SCRBenchmark import BenchmarkSuite
from SCRBenchmark import StringKeys as sk

import json
import numpy as np
import pandas as pd

target_folder = './data/experiments'

HARD_SAMPLE_SIZES = [1000,10_000]
print('generating instances')
#creates one folder per equation under the parent folder
# each equation folder contains the info file as json
# and the data files for each configuration as csv
BenchmarkSuite.create_hard_instances(target_folder = target_folder,
                                      Equations= FEYNMAN_SRSD_HARD,
                                      sample_sizes=HARD_SAMPLE_SIZES,
                                      noise_levels=HARD_NOISE_LEVELS,
                                      repetitions = 1
                                      )

c_positive = '[0 .. inf.]'
c_negative = '[-inf. .. 0]'
c_zero = '[0 .. 0]'

print('appending info for SCPR')
for equation_name in FEYNMAN_SRSD_HARD:
  print(equation_name)
  equation_folder = f'{target_folder}/{equation_name}'
  
  supportedConstraints = []
  with open(f'{equation_folder}/constraint_info.json', "r+") as f:
    data = json.load(f)
    descriptor = ""
    for constraint in data['Constraints']:
      if constraint['descriptor'] == sk.EQUATION_CONSTRAINTS_DESCRIPTOR_ZERO:
        descriptor = c_zero
      if constraint['descriptor'] == sk.EQUATION_CONSTRAINTS_DESCRIPTOR_NEGATIVE:
        descriptor = c_negative
      if constraint['descriptor'] == sk.EQUATION_CONSTRAINTS_DESCRIPTOR_POSITIVE:
        descriptor = c_positive
      
      spaces = []
      for space in constraint["sample_space"]:
        spaces.append(f"{space['name']} in [{space['low']} .. {space['high']}]")


      if constraint['order_derivative'] == 0:
        supportedConstraints.append(f"f in {descriptor} where {', '.join(spaces)}")
      elif constraint['order_derivative'] == 1:
        supportedConstraints.append(f"df/d{constraint['var_name']} in {descriptor} where {', '.join(spaces)}")
      elif constraint['order_derivative'] == 2:
        supportedConstraints.append(f"d²f/d{constraint['var_name']}² in {descriptor} where {', '.join(spaces)}")
    # Write the constraints to a text file, each on a new line
    with open(f'{equation_folder}/constraints.txt', "w", encoding='utf-8') as f:
      f.write("\r".join(supportedConstraints))
    