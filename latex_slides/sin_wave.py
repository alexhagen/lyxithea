import matplotlib as mpl
mpl.use('pgf')
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 6.5)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, 'r-', x, y2, 'b--')
plt.xlabel('x-coordinate ($x$) [$cm$]')
plt.ylabel('y-coordinate ($y$) [$cm$]')
plt.gcf().set_size_inches(3.5, 2.0)
plt.tight_layout()
plt.savefig('img/figure.pgf', bbox_inches='tight',
            transparent=True)
