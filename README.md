# Stochastic Processes in Finance

An academic study comparing geometric random walk, geometric Brownian motion,
and log-space Ornstein-Uhlenbeck simulations with **AAPL** and the **VIX
volatility index**.

**[Read the full research report (PDF)](results/report.pdf)**

<!-- REPORT-PAGES:START -->

![Research report — page 1](results/pages/page-01.png)

![Research report — page 2](results/pages/page-02.png)

![Research report — page 3](results/pages/page-03.png)

![Research report — page 4](results/pages/page-04.png)

![Research report — page 5](results/pages/page-05.png)

![Research report — page 6](results/pages/page-06.png)

![Research report — page 7](results/pages/page-07.png)

![Research report — page 8](results/pages/page-08.png)

![Research report — page 9](results/pages/page-09.png)

![Research report — page 10](results/pages/page-10.png)

![Research report — page 11](results/pages/page-11.png)

![Research report — page 12](results/pages/page-12.png)

![Research report — page 13](results/pages/page-13.png)

<!-- REPORT-PAGES:END -->

## Run the analysis

```bash
pip install -r requirements.txt
python src/analysis.py
```

The script uses the local datasets in `Data/Assets`, analyzes both assets,
and regenerates the report. PDF generation requires Tectonic or pdfLaTeX;
the local portable compiler is excluded from Git.

Model definitions are in `src/simulations.py`; statistical measures are in
`src/metrics.py`.
