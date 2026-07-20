# Comparative KPI Analysis of Stock Brokers

Comparative dashboard of 11 brokers in the Dominican securities market: average annual return, risk rating (1-9), fees, assets under management (AUM) and order execution rate, compared through scatter matrices (risk/return, fees/return, execution/risk, AUM/return).

**About the data:** simulated. Broker names and SIVCV codes belong to real registered brokers, but every figure is fictional. The value here is the comparative KPI framework applied to the real structure of the market.

**Why this project:** I follow the Dominican securities market closely (my goal is a Master's in Economics) and I built this to explore how you'd actually compare brokers if the data were public.

## Results

![Risk vs Return](images/risk_vs_return.png)

![Return vs AUM](images/return_vs_aum.png)

More charts in [`images/`](./images): fees vs return, execution vs risk, risk vs AUM.

## Run it

```bash
pip install pandas matplotlib seaborn
python broker_kpi_analysis.py
```

Charts are saved to `images/` automatically.

**Stack:** Python · Pandas · Matplotlib · Seaborn
