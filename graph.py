import matplotlib.pyplot as plt
from scipy import stats

plt.style.use('dark_background')

# Dados
x = list(range(-10,10))
y = [v + abs(v) for v in x]


# Gráfico
plt.scatter(x, y)
plt.show()