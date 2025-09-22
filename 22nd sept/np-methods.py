import numpy as np

arr = np.array([1,2,3,4,5,6])

#slicing
print(f" First 3 elements: {arr[:3]}")
print(f"Reversed: {arr[::-1]}")
print(f"Sum: {np.sum(arr)}")
print(f"Average: {np.mean(arr)}")
print(f"Min: {arr.min()}")
print(f"Max: {np.max(arr)}")
print(f"Standard Deviation: {np.std(arr)}")