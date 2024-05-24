import CoolProp
from CoolProp.Plots import PropertyPlot
plot = PropertyPlot('R404a', 'ts')
plot.calc_isolines()
plot.show()