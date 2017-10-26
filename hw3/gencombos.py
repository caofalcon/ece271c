import numpy as np

comboArray = np.zeros((3003,), dtype=int)

idx = 0
for num in range(0, 800001):
    numAsNPArray = np.array(list(str(num)))
    if np.sum(numAsNPArray.astype(int)) <= 8:
        comboArray[idx] = num
        idx = idx + 1

np.save('combos.npy', comboArray)
