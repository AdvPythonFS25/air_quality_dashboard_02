## Unit-Tests for 2 important functions

# update max-value
this function is responsible to return the max value of the pollutants in a given city and time-period
We test two distinct test-cases:
- Firstly the function call with a valid input (where everything should run fine)
- Secondly the function call with invalid input, where no data is available for the given city and period. Here we expect a "no-data-available" result

# update plot-function
this function is responsible to update the plot, when the user input is changed. It is essential to our dashboard
We also test two cases:
- Firstly the function call with valid input (again we expect everything to run fine)
- Secondly a "bad" function call, where no city is defined as a filter, we excpect a "select a city" prompt