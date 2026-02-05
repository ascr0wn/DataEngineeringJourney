# import sys
# print("The name of this file is:", sys.argv[0])
# for i in range(len(sys.argv)):
#     print(f"Argument {i}: {sys.argv[i]}")
# print("The Arguments passed to this file are:", sys.argv[1:])

import pandas as pd
my_df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})
print(my_df)

