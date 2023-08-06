import matplotlib.pyplot as plt
import numpy as np

import GooseMPL as gplt

plt.style.use(["goose", "goose-latex", "goose-autolayout"])


fig, ax = plt.subplots()

x = np.linspace(0, 1, 1000)
y = x**2

ax.plot(x, y)

ax.set_xlim([0, 1])
ax.set_ylim([0, 1])

gplt.xticks(keep=[0, -1], axis=ax)
gplt.yticks(keep=[0, -1], axis=ax)

plt.savefig("ticks.svg")
plt.close()
