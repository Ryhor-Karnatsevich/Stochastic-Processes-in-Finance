"""Generate the LaTeX report and compile its PDF."""
from pathlib import Path
import math
import argparse
import os
import shutil
import subprocess


RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


def latex_escape(value):
    replacements = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
        "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
        "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
        "–": "--",
    }
    return "".join(replacements.get(char, char) for char in str(value))


def statistics_table(table, ticker):
    """Use short model labels so the numerical table remains readable."""
    metrics = [
        ("mean", "Annualized mean log return", True),
        ("volatility", "Annualized volatility", True),
        ("autocorr", "Return autocorrelation (lag 1)", False),
        ("adf_pvalue", "ADF p-value: returns", False),
        ("adf_price", "ADF p-value: price series", False),
        ("skewness", "Return skewness", False),
        ("kurtosis", "Return kurtosis (Pearson)", False),
        ("max_drawdown", "Maximum drawdown", True),
    ]
    rows = ["Metric & " + latex_escape(ticker) + r" & RW & GBM & Log-OU \\", r"\midrule"]
    for key, label, percent in metrics:
        values = []
        for value in table[key]:
            value = float(value)
            if not math.isfinite(value):
                values.append("--")
            elif percent:
                values.append(f"{value * 100:.2f}" + r"\%")
            elif key.startswith("adf") and value < 0.0001:
                values.append(r"$<10^{-4}$")
            else:
                values.append(f"{value:.4g}")
        rows.append(label + " & " + " & ".join(values) + r" \\")
    return (r"\begin{table}[htbp]\centering" + "\n"
            + rf"\caption{{{latex_escape(ticker)}: observed and simulated statistics.}}" + "\n"
            + r"\resizebox{\linewidth}{!}{\begin{tabular}{lrrrr}\toprule" + "\n"
            + "\n".join(rows) + "\n"
            + r"\bottomrule\end{tabular}}\end{table}")


def write_report(results):
    """One academic report; edit this template for lasting wording changes."""
    RESULTS_DIR.mkdir(exist_ok=True)
    sections = []
    parameter_rows = []
    summary_rows = []
    for result in results:
        ticker = result["ticker"]
        table = result["table"]
        observed = table.loc[ticker]
        models = table.drop(index=ticker)
        parameter_rows.append(
            f"{latex_escape(ticker)} & {result['starting_price']:.2f} & "
            f"{result['mean_return']:.4f} & {result['volatility']:.4f} & "
            f"{result['long_term_mean']:.4f} & {result['theta']:.1f}" + r" \\")
        summary_rows.append(
            f"{latex_escape(ticker)} & {observed['autocorr']:.3f} & "
            f"{observed['kurtosis']:.2f} & {observed['adf_price']:.4g}" + r" \\")
        stationarity = ("rejects the unit-root null at the 5\\% level"
                        if observed['adf_price'] < 0.05 else
                        "does not reject the unit-root null at the 5\\% level")
        sections.append(r"\clearpage" + "\n" + rf"\section{{Results: {latex_escape(ticker)}}}" + "\n"
            + statistics_table(table, ticker) + "\n"
            + rf"The sample contains {result['observations']} observed daily log returns. "
            + f"Its annualized mean log return is {observed['mean'] * 100:.2f}"
            + r"\% and annualized volatility is "
            + f"{observed['volatility'] * 100:.2f}" + r"\%." + "\n\n"
            + r"\subsection{Distribution and risk}" + "\n"
            + f"Observed Pearson kurtosis is {observed['kurtosis']:.2f}, versus "
            + f"{models['kurtosis'].min():.2f}--{models['kurtosis'].max():.2f} "
            + "across the simulated models. Observed skewness is "
            + f"{observed['skewness']:.3f}. Gaussian shocks do not reproduce "
            + "the observed higher return moments in this run. "
            + f"Observed maximum drawdown is {observed['max_drawdown'] * 100:.2f}"
            + r"\%; model drawdowns are path averages and should not be treated as forecasts." + "\n\n"
            + r"\subsection{Persistence and model fit}" + "\n"
            + f"Lag-one return autocorrelation is {observed['autocorr']:.3f}. "
            + "This is a descriptive measure, not a formal test of market efficiency. "
            + f"The ADF test on observed log prices {stationarity}. "
            + "That result alone does not identify an OU process. "
            + f"GBM simulated volatility is {table.loc['Geometric Brownian Motion', 'volatility'] * 100:.2f}"
            + r"\%, while its annualized mean log return is "
            + f"{table.loc['Geometric Brownian Motion', 'mean'] * 100:.2f}"
            + r"\%. The drift convention discussed above explains why the mean need not match the data."
            + "\n\n" + r"\small RW: geometric random walk; GBM: geometric Brownian motion; Log-OU: exponentiated OU process.\normalsize"
        )
        for page_title, names in [
            ("Price dynamics", [("price_paths", "Observed series and one illustrative path per model."),
                                ("mean_paths", "Observed series and ensemble mean of 200 simulated paths.")]),
            ("Return diagnostics", [("distributions", "Observed and simulated log-return distributions; counts use different sample sizes."),
                                    ("autocorrelation", "Log-return autocorrelations; simulated diagnostics pool independent paths.")]),
        ]:
            figures = []
            for name, caption in names:
                figures.append(r"\begin{figure}[!htbp]\centering" + "\n"
                    + rf"\includegraphics[width=\linewidth,height=0.35\textheight,keepaspectratio]{{{result['figures_dir']}/{name}.png}}" + "\n"
                    + rf"\caption{{{latex_escape(ticker)}: {caption}}}" + "\n" + r"\end{figure}")
            sections.append(r"\clearpage" + "\n"
                            + rf"\subsection*{{{latex_escape(ticker)}: {page_title}}}" + "\n"
                            + "\n".join(figures))
    source = r"""% Generated by src/report.py. Edit that template for lasting changes.
% Basics: \section{...} creates headings; \[ ... \] displays mathematics.
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath,booktabs,graphicx}
\usepackage{xcolor,fancyhdr,microtype,lmodern}
\usepackage[hidelinks]{hyperref}
\definecolor{ink}{HTML}{17354A}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\textsc{Stochastic Processes in Finance}}
\fancyhead[R]{\small AAPL and VIX}
\fancyfoot[C]{\small\thepage}
\setlength{\headheight}{14pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\renewcommand{\arraystretch}{1.25}
\title{\color{ink}Stochastic Processes in Finance\\\large An Empirical Comparison of AAPL and VIX}
\author{}\date{}
\begin{document}\maketitle
\begin{abstract}
This study compares a geometric random walk, geometric Brownian motion,
and an exponentiated Ornstein--Uhlenbeck process with observed AAPL stock
prices and the VIX volatility index. Each asset is studied using 504 daily
log returns and 200 simulated paths per model. The comparison considers
return moments, serial dependence, stationarity diagnostics, and drawdown.
The exercise evaluates in-sample descriptive fit; it does not establish
predictive performance or market efficiency.
\end{abstract}

\section{Research objective and hypotheses}
The objective is to assess which empirical features of two contrasting
financial series can be reproduced by simple stochastic processes.
VIX is a volatility index, not a directly investable stock price; applying
price-process models to it is an illustrative statistical exercise.

The original research questions are expressed as four hypotheses:
\begin{enumerate}
\item \textbf{H1: Weak return dependence.} Returns have little serial
correlation. Autocorrelation is examined as a limited diagnostic of the
broader weak-form efficiency question.
\item \textbf{H2: Random-walk approximation.} A geometric random walk
reproduces observed return and risk characteristics reasonably well.
\item \textbf{H3: GBM distributional fit.} Gaussian log-return increments
provide an adequate description of the observed distribution.
\item \textbf{H4: Mean reversion.} Log-price stationarity is consistent
with using a mean-reverting process. An ADF test is a diagnostic, not proof
of OU dynamics.
\end{enumerate}

\clearpage
\section{Data and methodology}
The analysis uses the local snapshots \texttt{Data/Assets/stock.csv} and
\texttt{Data/Assets/index.csv}, originally sourced through yfinance.
Each series contributes its last 505 closing observations, giving 504
log returns, $r_t=\log(S_t/S_{t-1})$. The CSV files contain no date column,
so exact calendar coverage cannot be reconstructed from these inputs.
The report is rebuilt from both snapshots without downloading fresh data.

Each asset uses 200 paths of 504 increments, $\Delta t=1/252$, and random
seed 51 reset separately for reproducibility. Inputs are estimated from
the same sample used for comparison, making this an in-sample study.
Annualized mean and volatility use $m=252\bar r$ and
$\sigma=\sqrt{252}\,\operatorname{std}(r)$, with population standard deviation.

\subsection{Implemented processes}
Let $Z_t$ be independent standard normal draws and $X_t=\log S_t$:
\begin{align*}
\text{RW:}\quad S_{t+1}&=S_t\exp(\sqrt{\Delta t}Z_t),\\
\text{GBM:}\quad S_{t+1}&=S_t\exp\bigl[(m-\sigma^2/2)\Delta t+\sigma\sqrt{\Delta t}Z_t\bigr],\\
\text{Log-OU:}\quad X_{t+1}&=X_t+\theta(\ell-X_t)\Delta t+\sigma\sqrt{\Delta t}Z_t,
\quad S_t=e^{X_t}.
\end{align*}
Here $\ell$ is the sample mean log price and $\theta$ is specified rather
than fitted. The random walk fixes annual log volatility at one.
The GBM code uses the observed mean log return as $m$ and then subtracts
$\sigma^2/2$, so expected annual log return is $m-\sigma^2/2$, rather than $m$.
This implementation detail is retained and must inform interpretation.

\begin{table}[htbp]\centering
\caption{Model inputs. Starting levels retain their original units.}
\begin{tabular}{lrrrrr}\toprule
Asset & $S_0$ & $m$ & $\sigma$ & $\ell$ & $\theta$ \\\midrule
__PARAMETERS__
\bottomrule\end{tabular}\end{table}

\subsection{Measurement conventions}
Simulated return moments use pooled paths. Return ADF tests and
correlations use flattened paths, creating artificial joins between
independent simulations. Simulated price ADF p-values and drawdowns are
averages of per-path statistics; average p-values are not combined tests.
Observed and OU price ADF tests use log prices, whereas RW and GBM use
levels. Pearson kurtosis equals three under normality. Drawdowns are
negative losses relative to preceding peaks.

__SECTIONS__

\clearpage
\section{Discussion and conclusions}
\begin{table}[htbp]\centering
\caption{Observed diagnostics across the two assets.}
\begin{tabular}{lrrr}\toprule
Asset & Return ACF(1) & Pearson kurtosis & Log-price ADF p-value \\\midrule
__SUMMARY__
\bottomrule\end{tabular}\end{table}

\textbf{H1: Limited evidence on dependence.} The observed autocorrelations
and ACF plots describe serial dependence, but there is no formal joint
whiteness or market-efficiency test in this implementation. The broader
efficiency hypothesis remains unresolved.

\textbf{H2: Limited random-walk fit.} The implemented random walk uses
unit annual log volatility rather than an asset-calibrated scale. Its
risk and distributional fit must therefore be assessed relative to this
specific specification, not as a rejection of every random-walk model.

\textbf{H3: Distributional mismatch.} Both observed series have higher
kurtosis than the approximately Gaussian simulated returns in this run.
GBM reproduces its volatility input closely but does not reproduce these
tail characteristics. Its mean comparison is additionally affected by
the drift convention described in the methodology.

\textbf{H4: Stationarity is not model identification.} The asset-level
ADF results give evidence concerning a unit root under the test's default
specification. Neither rejection nor non-rejection alone establishes
that an OU process is suitable; $\theta$ is not estimated here.

\subsection{Scope and further work}
No single implemented model captures all observed features. The main
lesson is to compare scale, tails, and persistence jointly, rather than
judge models from one illustrative path or a matching volatility.
These results are descriptive, not investment or forecasting evidence.

A stronger follow-up would preserve dated observations, align simulated
and observed price grids, use consistent price transformations for ADF,
compute dependence diagnostics per path, estimate mean-reversion speed,
and evaluate corrected drift calibration on an unseen sample. These are
proposed extensions, not changes made for this report.
\end{document}
"""
    for token, value in {
        "PARAMETERS": "\n".join(parameter_rows),
        "SUMMARY": "\n".join(summary_rows),
        "SECTIONS": "\n".join(sections),
    }.items():
        source = source.replace(f"__{token}__", value)
    destination = RESULTS_DIR / "report.tex"
    destination.write_text(source, encoding="utf-8")
    return destination


def compile_report(source=None, open_pdf=False):
    source = Path(source or RESULTS_DIR / "report.tex").resolve()
    if not source.is_file():
        raise FileNotFoundError("Run src/analysis.py first to generate results/report.tex")
    portable = RESULTS_DIR.parent / ".tools" / "tectonic" / "tectonic.exe"
    tectonic = str(portable) if portable.is_file() else shutil.which("tectonic")
    pdflatex = shutil.which("pdflatex")
    if tectonic:
        commands = [[tectonic, "--untrusted", source.name]]
    elif pdflatex:
        commands = [[pdflatex, "-no-shell-escape", "-interaction=nonstopmode",
                     "-halt-on-error", source.name]] * 2
    else:
        raise RuntimeError("No LaTeX compiler found. Install Tectonic or pdfLaTeX; "
                           "or put tectonic.exe in .tools/tectonic/. The .tex source is available.")
    for command in commands:
        subprocess.run(command, cwd=source.parent, check=True)
    pdf = source.with_suffix(".pdf")
    if not pdf.is_file():
        raise RuntimeError("Compilation completed without producing report.pdf")
    print(f"PDF report saved to: {pdf}")
    if open_pdf:
        if os.name == "nt":
            os.startfile(pdf)
        else:
            import webbrowser
            webbrowser.open(pdf.as_uri())
    return pdf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--open", action="store_true", help="Open the finished PDF")
    args = parser.parse_args()
    compile_report(open_pdf=args.open)
