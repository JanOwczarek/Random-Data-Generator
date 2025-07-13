# Random-Data-Generator
A python class that allows user to create random data at object instantiation. Class inherits the pandas Dataframe class (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) so all pandas methods for the dataframe object will be available.


# Future Updates
1) Add distribution option (i.e. define variable to have a negatively skewed disttribution)
2) Allow creating grouped data

# Use Guide

The argument rd_dict is supplied with a dictionary containing the definitions of the random variables that are meant to be created. An example definition is shown below:

var_dict = {"Ethnicity": ["cat", ["White", "Black", "Asian"]],
            "Weight": ["con", [50,150,2]],
            "Salary": ["con", [24000,100000,1]],
            "Died": ["binary", ["Not Died", "Died"]],
            "Age_at_death": ["interval", [56,102]],
            "Num_hosp_visits": ["interval", [0,20]]}

The key is the variable name and the value is a list that specifies the details of that variable.

NOTE: for every variable the first value of the specification (i.e. the key's value in the dictionary) is alwasy the type of variable and the options are: 'cat', 'con', 'interval', 'binary'.

* Categorical
"Ethnicity": ["cat", ["White", "Black", "Asian"]]
1) the second item of the specification list is the list of categories

* Continuous
"Weight": ["con", [50,150,2]] OR "Salary": ["con", [24000,100000,1]]
1) the second item of the specification list is a list containing (from left to right): the lower range, upper range, decimal places

* Inverval
  "Age_at_death": ["interval", [56,102]] OR "Num_hosp_visits": ["interval", [0,20]]
1) the second item of the specification list is a list containing (from left to right): the lower range, upper range
2) NOTE only a spacing of 1 between values is allowed.

* Binary
"Died": ["binary", ["Not Died", "Died"]]
1) the second item of the specification list is a list containing the binary categories

