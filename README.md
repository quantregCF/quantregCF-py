# QuantregCF

This Python package is an implementation of quantile regression model proposed by Professor Simon Lee in 
"[Endogeneity in Quantile Regression Models: A Control Function Approach](https://doi.org/10.1016/j.jeconom.2007.01.014)", Journal of Econometrics, 141: 1131-1158, 2007.

## Installation
This project can be installed using pip: 
```bash
pip install -i https://test.pypi.org/simple/ quantregCF
```

## How to get start
- Install the package by following the instruction above (note that the current package is stored in [TestPyPI](https://test.pypi.org/project/quantregCF/))
- Download the test file `fishdata.py` to your computer
- Run ```python3 fishdata.py```

## Usage 
```python
from quantregCF import quantregCF

beta, se = quantregCF(option, degree, tau_first_stage, tau_second_stage, data)
```
`quantregCF` returns a list of estimated coefficients and a list of standard errors. 

## Parameters
`option` = 1 if the data file is in Stata `.dta` format and is to be downloaded from a URL link. 

`degree` is the degree of the polynomial/B-spline. (integer) 

`tau_first_stage` is the tau for the first-stage quantile regression. (between 0 and 1)

`tau_second_stage` is the tau for the second-stage quantile regression. (between 0 and 1)

`data` is a list of length 4 that contains information about the dataset. `data` = [`dep_var`, `endog_var`, 
`exog_var_lst`, `iv_var_lst`], where `dep_var` and `endog_var` are strings of the names of dependent variable and endogenous 
right-hand side variable, and `exog_var_lst` and `iv_var_lst` are the lists of exogenous included variables and instrumental variables. 

## Example
```python
# load data
data_source = "http://people.brandeis.edu/~kgraddy/datasets/fishdata.dta"
var_lst = ['qty', 'price', ["day1", "day2", "day3", "day4"], ["stormy", "mixed"]]
data_lst = [0, data_source, var_lst]

# regressions
beta, se = quantregCF(option=1, degree=3, tau_first_stage=0.5, tau_second_stage=0.5, data=data_lst)

# calculate the 95% confidence interval
ci_lb = beta[0] - 1.96 * se[0]
ci_ub = beta[0] + 1.96 * se[0]
```

## Dependencies
- NumPy
- Pandas
- SciPy
- CVXPY
- Urllib
