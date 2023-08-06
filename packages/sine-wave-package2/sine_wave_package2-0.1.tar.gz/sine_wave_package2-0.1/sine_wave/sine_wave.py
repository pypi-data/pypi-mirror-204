import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    df = pd.DataFrame({'x': x, 'y': y})
    plt.plot(df['x'], df['y'])
    plt.show()


if __name__ == '__main__':
    main()
