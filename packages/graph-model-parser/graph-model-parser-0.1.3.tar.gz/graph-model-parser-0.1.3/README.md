# GraphModelParser

GraphModelParser is a Python library for representing and simulating dynamical graph models from a string description. The library supports various probability distributions such as normal, poisson, expon, binom, and uniform from the `scipy.stats` module.

## Installation

You can install GraphModelParser from PyPI by running:

```bash
pip install graph-model-parser
```

## Usage

```python
from graph_model_parser import GraphModelParser
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

model_description = '''
            a_{t} = a_{t-1} + 1
            b_{t} = b_{t-1} + 2*b_{t-2} + a_0
            c_{t} = c_{t-1} + normal(1, 2)
            '''
# Always enclose the dynamic time index in curly braces e.g. {t-1}  
initial_values = {'a_0': 0, 'a_1': 1, 'b_0': 0, 'b_1': 1, 'c_0': 0}
model = GraphModelParser(model_description, initial_values)
print(model(t=20))
```

In this example, we define a simple dynamical graph model with three variables (`a_{t}`, `b_{t}`, and `c_{t}`) and their relationships over time. The `c_{t}` variable is also affected by a random normal distribution with a mean of 1 and a standard deviation of 2.

## Features

- Define dynamical graph models using a simple string-based syntax.
- Support for various probability distributions from `scipy.stats`, including normal, poisson, expon, binom, and uniform.
- Easily compute the values of variables at specific time points.
- Define initial values for variables and model their evolution over time.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)