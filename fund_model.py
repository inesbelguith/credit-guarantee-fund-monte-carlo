"""
Can a credit guarantee fund survive a bad year? 
(All numbers are synthetic)
"""
import numpy as np

# fund
N_LOANS = 1_000                    
LOAN_SIZE = 40_000                 
COVERAGE = 0.50                    
PAYOUT = LOAN_SIZE * COVERAGE      
GUARANTEES = N_LOANS * PAYOUT      

# economy (years)
PD_NORMAL = 0.04                   
PD_RECESSION = 0.12                
P_RECESSION = 0.15                
PD_AVERAGE = (1 - P_RECESSION) * PD_NORMAL + P_RECESSION * PD_RECESSION  


def simulate_without_recessions(n_sims=10_000, seed=1):
    
    rng = np.random.default_rng(seed)
    defaults = rng.binomial(N_LOANS, PD_AVERAGE, size=n_sims)
    return defaults * PAYOUT


def simulate_with_recessions(n_sims=10_000, pd_normal=PD_NORMAL,
                             pd_recession=PD_RECESSION, p_recession=P_RECESSION,
                             seed=2):
    rng = np.random.default_rng(seed)
    is_recession = rng.random(n_sims) < p_recession
    pd_year = np.where(is_recession, pd_recession, pd_normal)
    defaults = rng.binomial(N_LOANS, pd_year)
    return defaults * PAYOUT, is_recession


def prob_of_ruin(claims, capital):
    
    return (claims > capital).mean()


if __name__ == "__main__":
    m = 1e6
    print("STEP 1 - one loan")
    print(f"  Loan ${LOAN_SIZE:,}; fund pays {COVERAGE:.0%} = ${PAYOUT:,.0f} if it defaults.")
    print(f"  With a 5.2% default chance, the average cost per loan is "
          f"${PAYOUT * PD_AVERAGE:,.0f} a year.")

    print("\nSTEP 2 - the whole portfolio (no simulation)")
    print(f"  {N_LOANS:,} loans -> total promised ${GUARANTEES/m:.0f}M")
    print(f"  Expected defaults per year = {N_LOANS} x {PD_AVERAGE:.1%} = {N_LOANS*PD_AVERAGE:.0f}")
    print(f"  Expected claims per year   = {N_LOANS*PD_AVERAGE:.0f} x ${PAYOUT:,.0f} = "
          f"${N_LOANS*PD_AVERAGE*PAYOUT/m:.2f}M   <- the 'normal cost of doing business'")

    print("\nSTEP 3 - simulate 10,000 years, no recessions")
    flat = simulate_without_recessions()
    print(f"  average claims ${flat.mean()/m:.2f}M | best year ${flat.min()/m:.2f}M | "
          f"worst year ${flat.max()/m:.2f}M")
    print("  (average matches step 2 -> the simulation works)")

    print("\nSTEP 4 - simulate 10,000 years, with recessions")
    rec, is_rec = simulate_with_recessions()
    print(f"  average claims ${rec.mean()/m:.2f}M | best year ${rec.min()/m:.2f}M | "
          f"worst year ${rec.max()/m:.2f}M")
    print(f"  recession years: {is_rec.mean():.1%} of years, average claims "
          f"${rec[is_rec].mean()/m:.2f}M")
    print(f"  normal years   : average claims ${rec[~is_rec].mean()/m:.2f}M")
    print("  Same average cost as step 3, but a much worse WORST year.")

    print("\nSTEP 5 - how much capital does the fund need?")
    print("  capital   leverage   ruin % (no recessions)   ruin % (with recessions)")
    for capital in [5e6, 3e6, 2.5e6, 2e6, 1.5e6]:
        print(f"  ${capital/m:>4.1f}M   {GUARANTEES/capital:>5.1f}x     "
              f"{100*prob_of_ruin(flat, capital):>10.2f}               "
              f"{100*prob_of_ruin(rec, capital):>10.2f}")
