# README - Trabajo Práctico 1

Guía del proyecto para Análisis de Series de Tiempo II.

## Project Overview

This is a university assignment repository for "Análisis de Series de Tiempo II" (Time Series Analysis II) from Universidad de Buenos Aires, Especialización en Inteligencia Artificial.

**Assignment:** Trabajo Práctico 1 (TP1-AST2.pdf)
**Due Date:** 16/11/2025
**Instructors:** Camilo Argoty, Matias Vera

## Assignment Structure

The assignment consists of 2 exercises, each requiring a separate Jupyter notebook (*.ipynb):

### Exercise 1: Geometric Brownian Motion (Stock Price Simulation)
- Initial stock price: $60
- Expected return (μ): 20% annual
- Volatility (σ): 40% annual
- Differential equation: dPt = μPtdt + σPtdt
- Tasks:
  a) Determine probability distribution for stock price at t=2 years
  b) Calculate mean, standard deviation, and 95% confidence interval
  c) Monte Carlo simulation to verify analytical calculations

### Exercise 2: ARMA(5,3) Process with Kalman Filter
- Generate synthetic time series of length T=10000
- Observations available only every 10 time steps (sparse observations)
- Tasks:
  a) Generate synthetic ARMA(5,3) sequence
  b) Subsample observations (every 10th point)
  c) Implement Kalman filter for state estimation and forecasting
  d) Evaluate filter performance vs ground truth

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install required packages (create requirements.txt first)
pip install -r requirements.txt
```

### Running Jupyter Notebooks
```bash
# Start Jupyter Lab
jupyter lab

# Start Jupyter Notebook
jupyter notebook
```

## Key Technical Concepts

### Exercise 1 Architecture
- **Geometric Brownian Motion (GBM):** Standard model for stock price dynamics
- Solution form: P(t) = P(0) * exp((μ - σ²/2)t + σW(t))
- P(T) follows log-normal distribution
- Monte Carlo simulation compares empirical vs theoretical distributions

### Exercise 2 Architecture
- **ARMA(5,3) Model:** Autoregressive Moving Average with 5 AR terms and 3 MA terms
- **State-Space Representation:** ARMA model must be converted to state-space form for Kalman filtering
- **Kalman Filter Components:**
  - State transition matrix (F)
  - Observation matrix (H)
  - Process noise covariance (Q)
  - Measurement noise covariance (R)
- **Sparse Observations:** Observations at t=0, 10, 20, 30... while estimating all intermediate states

## Expected Packages

Likely dependencies (create requirements.txt):
- numpy: Numerical computing
- scipy: Statistical distributions and optimization
- matplotlib/seaborn: Visualization
- statsmodels: ARMA model generation and estimation
- jupyter/jupyterlab: Notebook environment
- pandas: Data manipulation (optional)

## File Organization

Expected structure:
```
TP1ST2/
├── TP1-AST2.pdf          # Assignment specification
├── ejercicio1.ipynb      # Geometric Brownian Motion exercise
├── ejercicio2.ipynb      # ARMA + Kalman Filter exercise
├── requirements.txt      # Python dependencies
├── .venv/               # Virtual environment (excluded from git)
└── README.md            # This file
```

## Important Notes

- Each exercise must be in a separate .ipynb file
- Both exercises require both theoretical derivations and simulation/implementation
- Exercise 1 requires comparing analytical solutions with Monte Carlo results
- Exercise 2 requires implementing Kalman filter from scratch or using existing libraries
- Visualizations are essential for demonstrating results
- The Kalman filter in Exercise 2 must handle the sparse observation pattern (decimation)
