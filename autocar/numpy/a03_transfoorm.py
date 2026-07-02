import numpy as np


def main():
    arr = np.arange(100)
    print(arr)
    reshp = arr.reshape((2,5,5,2))
    print(reshp,reshp.shape)


if __name__ == "__main__":
    main()