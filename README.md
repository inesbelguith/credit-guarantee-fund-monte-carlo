# credit-guarantee-fund-monte-carlo
Monte Carlo simulation in Python of a credit guarantee fund: how likely is it to run out of capital, and how much do recession years change the answer? Includes a Streamlit dashboard.

# Can a credit guarantee fund survive a bad year?

A Monte Carlo simulation of a credit guarantee fund: how likely is it to run out of capital in a year, and how much do recession years change the answer?
> All data is synthetic. The goal is only to demonstrate the method.


## The setup

- The fund guarantees 1,000 loans of $40,000 and pays 50% ($20,000) of each loan that defaults, so it has promised $20M in total.
- A normal year (85% of years): 4% of loans default. A recession year (15%): 12% default.
- The average default rate is 5.2%, so expected claims are $1.04M a year in both cases.


## Method

1. Decide for each of 10,000 simulated years whether it is a recession.
2. Set that year's default rate (12% or 4%).
3. Draw the number of defaults from a binomial distribution (1,000 loans).
4. Claims = defaults x $20,000.
5. Probability of ruin = share of years where claims exceed capital.


## Files

- `fund_model.py`: the simulation, one function per step
- `app.py`: Streamlit dashboard (capital, recession frequency and severity)


## Limitations

Identical loans, a one-year horizon, no fee income or recoveries, a two-state economy, and assumed (not estimated) parameters.
