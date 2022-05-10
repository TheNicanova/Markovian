import numpy as np
import matplotlib.pyplot as plt
from Structure.UnderlyingGenerator import *
from Option.Put import *
from PricingModel.Langstaff import *
from PricingModel.Basic import *
import copy

um = GeometricBrownianMotion()

results = []

model_array = [LangStaff, Basic]

for model in model_array:
    model.train()



np.random.seed(19680801)

n_bins = 100
x = np.random.randn(1000)
y = np.random.randn(1000)

fig, ax = plt.subplots()

data = np.stack((x,y), axis=1)

ax.hist(data, n_bins, histtype='step', stacked=False, fill=False)

ax.set_title('stack step (unfilled)')

fig.tight_layout()
plt.show()