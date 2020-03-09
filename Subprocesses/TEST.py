import numpy as np
import matplotlib.pyplot as plt

X = 0

if __name__ == "__main__":
    with open('test.log', 'r') as f:
        try:
            x = int(f.read())
            x += 10
        except:
            x = 0
    with open('test.log', 'w') as f:
        f.write(str(x))	