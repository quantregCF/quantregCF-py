# QuantregCF

This Python package is an implementation of the control function approach for quantile regression models proposed by Sokbae Lee in "[Endogeneity in Quantile Regression Models: A Control Function Approach,](https://doi.org/10.1016/j.jeconom.2007.01.014)" _Journal of Econometrics_, 141: 1131-1158, 2007.

## Installation
This project can be installed using pip: 
```bash
pip install quantregCF
```

## Usage 
```python
from quantregCF import quantregCF

beta, se = quantregCF(option, degree, tau_first_stage, tau_second_stage, data)
```
`quantregCF` returns a list of estimated coefficients and a list of standard errors. 

## Parameters

The main function is

    quantregCF(option, degree, tau_first_stage, tau_second_stage, data)

`option`= 0 if the second-stage quantile regression uses polynomial series.

`option`= 1 if the second-stage quantile regression uses B-spline. 

`degree` is the degree of the polynomial/B-spline. (integer) 

`tau_first_stage` is the value of tau for the first-stage quantile regression. (between 0 and 1)

`tau_second_stage` is the value of tau for the second-stage quantile regression. (between 0 and 1)

The dataset is specified in `data`, which is a list of length 3.

    data = [`data_type`, `data_source`, `var_lst`]

Each element in `data` is defined as followed: 

`data_type` = 0 if the dataset is in Stata `.dta` format and is to be downloaded from a URL link specified in `data_source`.

`data_type` = 1 if the dataset is in Stata `.dta` format and is to be loaded locally from the file path specified in `data_source`.

`data_source` is the URL link/file path of the dataset.

The variable names are specified in `var_lst`, which is a list of length 4. The first two elements of `var_lst` are strings and the last two elements are lists of strings.

    `var_lst` = [`dep_var`, `endog_var`, `exog_var_lst`, `iv_var_lst`]

Each element in `var_lst` is defined as followed: 

`dep_var` and `endog_var` are the names of dependent variable and endogenous right-hand side variable. 

`exog_var_lst` and `iv_var_lst` are the lists of names of exogenous included variables and instrumental variables. 

## Example
```python
# load data
data_type = 0 # download the dataset from a URL link
data_source = "http://people.brandeis.edu/~kgraddy/datasets/fishdata.dta"
var_lst = ['qty', 'price', ["day1", "day2", "day3", "day4"], ["stormy", "mixed"]]
data_lst = [data_type, data_source, var_lst]

# regressions using B-splines in the second-stage
beta, se = quantregCF(option=1, degree=3, tau_first_stage=0.5, tau_second_stage=0.5, data=data_lst)

# calculate the 95% confidence interval
ci_lb = beta[0] - 1.96 * se[0]
ci_ub = beta[0] + 1.96 * se[0]
```

The file `fishdata.py` contains an example of how to use `QuantregCF` on the well-known Graddy’s Fulton fish market data. To run the code, simply download `fishdata.py` from the `tests` folder and run ```python fishdata.py```.

## Dependencies
- NumPy
- Pandas
- SciPy
- CVXPY
- Urllib
