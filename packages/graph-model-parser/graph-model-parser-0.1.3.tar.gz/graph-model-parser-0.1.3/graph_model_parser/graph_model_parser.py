import re
from collections import deque

import numpy as np
from scipy.stats import norm, poisson, expon, binom, uniform


class GraphModelParser:
    def __init__(self, model_description: str, initial_values: dict = None):
        """
        Class able to represent dynamical graph models from a string description, e.g.:
            >>> model_description = '''
            >>>                     a_t = a_{t-1} + 1
            >>>                     b_t = b_{t-1} + 2*b_{t-2} + a_t
            >>>                     c_t = c_{t-1} + normal(1, 2)
            >>>                     '''
            >>>
            >>> initial_values = {'a_0': 0, 'a_1': 1, 'b_0': 0, 'b_1': 1, 'b_2': 2}
            >>> model = GraphModelParser(model_description, initial_values)
            >>> print(model(t=10))

        The normal, poisson, expon, binom, and uniform from scipy.stats are supported.
        :param model_description: String with the model description
        :param initial_values: Dictionary with the initial values
        """
        self.variable_re = r"([a-zA-Z-_\d~{]+_{t})"
        self.model_description = model_description
        self.initial_values = initial_values
        self._formulas = {}
        self.computed_values = {}
        self._flatten_values = {}

        self.parse_model_description()

    def check_model_description(self):
        lines = self.model_description.strip().split('\n')

        for line in lines:
            # Check if there is an equal sign in the line
            if '=' not in line:
                raise ValueError(f"Invalid model description. Missing '=' in line: {line}")

            var_name, formula = line.split('=')

            # Check if variable name is valid
            var_name_pattern = r"^[a-zA-Z][a-zA-Z0-9_]*_{t}$"
            if not re.match(var_name_pattern, var_name.strip()):
                raise ValueError(f"Invalid variable name '{var_name}' in line: {line}. "
                                 "Be careful to enclose the time between { and }, e.g. b_{t}")

            # Check if formula is not empty
            if not formula.strip():
                raise ValueError(f"Invalid model description. Empty formula in line: {line}")

        return True

    def parse_model_description(self):
        self.check_model_description()
        lines = self.model_description.strip().split('\n')

        formulas = {}
        for line in lines:
            var_name, formula = line.split('=')
            var_name = var_name.strip()
            formulas[var_name] = formula.strip()

        ordered_formulas = []
        formulas_queue = deque(formulas.items())
        added = set()
        while formulas_queue:
            var_name, formula = formulas_queue.popleft()
            dependencies = set(re.findall(self.variable_re, formula))
            dependencies_met = all(dep in added for dep in dependencies)

            if dependencies_met:
                ordered_formulas.append((var_name, formula))
                added.add(var_name)
            else:
                formulas_queue.append((var_name, formula))

        self._formulas = ordered_formulas

    @property
    def formulas(self):
        if not self._formulas:
            self.parse_model_description()
        return self._formulas

    @property
    def variables(self):
        # Remove the time subscript
        return [var_name.split('_')[0] for var_name, formula in self.formulas]

    @property
    def max_time_computed(self):
        full_computed = -1
        if self.computed_values:
            max_time_computed = max(self.computed_values.keys())
            for t in range(max_time_computed, -1, -1):
                if t not in self.computed_values:
                    continue
                if all([f'{var_name}_{t}' in self.computed_values[t] for var_name in self.variables]):
                    full_computed = t
                    break
        max_initial_values = max([int(var_name.split('_')[1]) for var_name in self.initial_values.keys()])
        if full_computed >= max_initial_values:
            return full_computed

        for t in range(max_initial_values, -1, -1):
            if all([f'{var_name}_{t}' in self.initial_values for var_name in self.variables]):
                # Add computed values
                for t_computed in range(0, t + 1):
                    # Filter out the initial values
                    values_at_t = {var_name: value for var_name, value in self.initial_values.items()
                                   if f"_{t_computed}" in var_name}
                    self.computed_values[t_computed] = values_at_t
                return t

        return full_computed

    def flatten_values(self, t):
        if t > self.max_time_computed + 1:
            raise ValueError(f"Time {t} is not computed yet.")

        if t != self.max_time_computed + 1 and t in self._flatten_values:
            return self._flatten_values[t]

        if t <= 0:
            previous_values = {var_name: value for var_name, value in self.initial_values.items()
                               if f"_0" in var_name}
            if 0 in self.computed_values:
                previous_values = dict(
                    previous_values,
                    **self.computed_values[0]
                )
        else:
            previous_values = self.flatten_values(t - 1)

        current_values = {var_name: value for var_name, value in self.initial_values.items()
                          if f"_{t}" in var_name}
        if t in self.computed_values:
            current_values = dict(current_values,
                                  **{var_name: value for var_name, value in self.computed_values[t].items()})
        all_values = dict(
            previous_values,
            **current_values
        )

        if all([f'{var_name}_{t}' in all_values for var_name in self.variables]):
            self._flatten_values[t] = all_values

        return all_values

    def __call__(self, t=0, **kwargs):
        if t not in self.computed_values:
            return self.compute(t, **kwargs)

    def compute(self, t, whole_history=False):
        if t in self.computed_values:
            return self.computed_values[t]
        else:
            self.computed_values[t] = {}

        current_max_time_computed = self.max_time_computed
        if t > current_max_time_computed + 1:
            self.compute(t - 1)

        for var_name, formula in self.formulas:
            var_name = var_name.split('_')[0]
            flattened_values = self.flatten_values(t)
            if f"{var_name}_{t}" in flattened_values:
                self.computed_values[t][f'{var_name}_{t}'] = flattened_values[f'{var_name}_{t}']
            else:
                t_pattern = re.compile(r"{t-?\d+}")
                matches = t_pattern.finditer(formula)

                for match in matches:
                    offset = t + int(match.group()[2:-1])
                    if offset < 0:
                        offset = 0
                    formula = formula.replace(match.group(), f"{offset}")

                # Replace {t} with t
                formula = formula.replace('{t}', str(t))

                # Add custom functions for sampling
                custom_functions = {
                    'normal': norm.rvs,
                    'uniform': uniform.rvs,
                    'poisson': poisson.rvs,
                    'binomial': binom.rvs,
                    'exponential': expon.rvs,
                    '__builtins__': None
                }

                # Extract variable names from the formula
                var_pattern = re.compile(r"[a-zA-Z_\d^{]+_\d+")
                formula_vars = set(var_pattern.findall(formula))

                # Check if all variables are present in the flattened_values dictionary
                missing_vars = formula_vars - set(flattened_values.keys())
                if missing_vars:
                    raise ValueError(f"Missing variables: {missing_vars}")

                current_value = eval(formula, custom_functions, flattened_values)
                self.computed_values[t][f'{var_name}_{t}'] = current_value

        if whole_history:
            return self.flatten_values(t)

        return self.computed_values[t]
