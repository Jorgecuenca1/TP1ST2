"""
Script para ejecutar el Ejercicio 2 y capturar resultados
"""
import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess
from filterpy.kalman import KalmanFilter
import json

# Semilla para reproducibilidad
np.random.seed(42)

print("="*70)
print("EJERCICIO 2: ARMA(5,3) CON FILTRO DE KALMAN")
print("="*70)

# Parametros del modelo ARMA(5,3)
p = 5  # Orden AR
q = 3  # Orden MA
T = 10000  # Longitud de la serie temporal

# Coeficientes AR y MA
ar_coeffs = np.array([1, -0.6, 0.3, -0.2, 0.15, -0.1])
ma_coeffs = np.array([1, 0.5, -0.3, 0.2])

print("\n" + "="*70)
print("PARAMETROS DEL MODELO")
print("="*70)
print(f"Orden AR (p): {p}")
print(f"Orden MA (q): {q}")
print(f"Longitud serie: {T}")
print(f"Coeficientes AR: {ar_coeffs[1:]}")
print(f"Coeficientes MA: {ma_coeffs[1:]}")

# PARTE A: Generar proceso ARMA(5,3)
print("\n" + "="*70)
print("PARTE A: GENERACION DEL PROCESO ARMA(5,3)")
print("="*70)

arma_process = ArmaProcess(ar_coeffs, ma_coeffs)
burnin = 1000
y_true = arma_process.generate_sample(nsample=T + burnin)
y_true = y_true[burnin:]
t = np.arange(T)

media_serie = np.mean(y_true)
std_serie = np.std(y_true)
var_serie = np.var(y_true)

print(f"\nEstadisticas de la serie generada:")
print(f"  Media:          {media_serie:.6f}")
print(f"  Desv. Std:      {std_serie:.6f}")
print(f"  Varianza:       {var_serie:.6f}")
print(f"  Min:            {np.min(y_true):.6f}")
print(f"  Max:            {np.max(y_true):.6f}")

# PARTE B: Observaciones sparse (cada 10 pasos)
print("\n" + "="*70)
print("PARTE B: OBSERVACIONES SPARSE")
print("="*70)

decimation_factor = 10
t_obs = t[::decimation_factor]
y_obs = y_true[::decimation_factor]
n_obs = len(y_obs)

print(f"\nFactor de decimacion:  {decimation_factor}")
print(f"Puntos originales:     {T}")
print(f"Puntos observados:     {n_obs}")
print(f"Porcentaje observado:  {n_obs/T*100:.1f}%")

# PARTE C: Implementar Filtro de Kalman
print("\n" + "="*70)
print("PARTE C: FILTRO DE KALMAN")
print("="*70)

dim_x = max(p, q + 1)
dim_z = 1

kf = KalmanFilter(dim_x=dim_x, dim_z=dim_z)

# Matriz de transicion F
kf.F = np.zeros((dim_x, dim_x))
kf.F[0, :p] = -ar_coeffs[1:]
kf.F[1:p, :p-1] = np.eye(p-1)

# Matriz de observacion H
kf.H = np.zeros((dim_z, dim_x))
kf.H[0, 0] = 1.0

# Ruido de proceso Q
sigma_process = np.var(y_true)
kf.Q = np.zeros((dim_x, dim_x))
kf.Q[0, 0] = sigma_process

for i in range(1, min(q+1, dim_x)):
    kf.Q[0, i] = sigma_process * ma_coeffs[i] if i < len(ma_coeffs) else 0
    kf.Q[i, 0] = kf.Q[0, i]
    kf.Q[i, i] = sigma_process * 0.1

# Ruido de observacion R
sigma_obs = 0.01
kf.R = np.array([[sigma_obs**2]])

# Estado inicial
kf.x = np.zeros((dim_x, 1))
kf.P = np.eye(dim_x) * sigma_process

print(f"\nConfiguracion del filtro:")
print(f"  Dimension del estado: {dim_x}")
print(f"  Varianza del proceso: {sigma_process:.6f}")
print(f"  Varianza observacion: {sigma_obs**2:.6f}")

# Ejecutar filtro
print(f"\nEjecutando filtro de Kalman...")

x_filtered = np.zeros((T, dim_x))
P_filtered = np.zeros((T, dim_x, dim_x))
y_estimated = np.zeros(T)

obs_idx = 0

for t_step in range(T):
    kf.predict()

    if t_step in t_obs:
        z = np.array([[y_obs[obs_idx]]])
        kf.update(z)
        obs_idx += 1

    x_filtered[t_step, :] = kf.x.flatten()
    P_filtered[t_step, :, :] = kf.P
    y_estimated[t_step] = kf.x[0, 0]

    if (t_step + 1) % 2000 == 0:
        print(f"  Procesados {t_step + 1}/{T} ({(t_step+1)/T*100:.0f}%)")

print(f"\n>> Filtro ejecutado completamente")

# PARTE D: Evaluacion del desempeno
print("\n" + "="*70)
print("PARTE D: EVALUACION DEL DESEMPENO")
print("="*70)

# Calcular errores
error = y_estimated - y_true
abs_error = np.abs(error)

mae = np.mean(abs_error)
mse = np.mean(error**2)
rmse = np.sqrt(mse)

mask_nonzero = y_true != 0
mape = np.mean(np.abs(error[mask_nonzero] / y_true[mask_nonzero])) * 100

correlation = np.corrcoef(y_true, y_estimated)[0, 1]

ss_res = np.sum(error**2)
ss_tot = np.sum((y_true - np.mean(y_true))**2)
r2_score = 1 - (ss_res / ss_tot)

print(f"\nMetricas globales:")
print(f"  MAE (Error Absoluto Medio):           {mae:.6f}")
print(f"  MSE (Error Cuadratico Medio):         {mse:.6f}")
print(f"  RMSE (Raiz Error Cuadratico Medio):   {rmse:.6f}")
print(f"  MAPE (Error Porcentual Abs. Medio):   {mape:.4f}%")
print(f"  Correlacion:                           {correlation:.6f}")
print(f"  R^2 (Coef. Determinacion):             {r2_score:.6f}")

# Comparacion puntos observados vs interpolados
observed_mask = np.zeros(T, dtype=bool)
observed_mask[t_obs] = True

error_obs = error[observed_mask]
mae_obs = np.mean(np.abs(error_obs))
rmse_obs = np.sqrt(np.mean(error_obs**2))

error_interp = error[~observed_mask]
mae_interp = np.mean(np.abs(error_interp))
rmse_interp = np.sqrt(np.mean(error_interp**2))

print(f"\nPuntos Observados (n={np.sum(observed_mask)}):")
print(f"  MAE:   {mae_obs:.6f}")
print(f"  RMSE:  {rmse_obs:.6f}")

print(f"\nPuntos Interpolados (n={np.sum(~observed_mask)}):")
print(f"  MAE:   {mae_interp:.6f}")
print(f"  RMSE:  {rmse_interp:.6f}")

ratio_mae = mae_interp / mae_obs
ratio_rmse = rmse_interp / rmse_obs

print(f"\nRelacion Error Interpolado / Error Observado:")
print(f"  MAE ratio:  {ratio_mae:.4f}")
print(f"  RMSE ratio: {ratio_rmse:.4f}")

# Evaluacion
print("\n" + "="*70)
print("EVALUACION DE LA INTERPOLACION")
print("="*70)
if ratio_mae < 1.5:
    print(">> EXCELENTE: Error similar en puntos observados e interpolados")
elif ratio_mae < 2.5:
    print(">> ACEPTABLE: Error moderadamente mayor en puntos interpolados")
else:
    print(">> DEFICIENTE: Error significativamente mayor en puntos interpolados")

# Guardar resultados
resultados = {
    "parametros": {
        "p": p,
        "q": q,
        "T": T,
        "decimation_factor": decimation_factor
    },
    "serie": {
        "media": float(media_serie),
        "std": float(std_serie),
        "varianza": float(var_serie)
    },
    "metricas_globales": {
        "mae": float(mae),
        "mse": float(mse),
        "rmse": float(rmse),
        "mape": float(mape),
        "correlacion": float(correlation),
        "r2": float(r2_score)
    },
    "observados_vs_interpolados": {
        "mae_observados": float(mae_obs),
        "rmse_observados": float(rmse_obs),
        "mae_interpolados": float(mae_interp),
        "rmse_interpolados": float(rmse_interp),
        "ratio_mae": float(ratio_mae),
        "ratio_rmse": float(ratio_rmse)
    }
}

with open('resultados_ejercicio2.json', 'w') as f:
    json.dump(resultados, f, indent=2)

print(f"\n>> Resultados guardados en 'resultados_ejercicio2.json'")

print("\n" + "="*70)
print("EJERCICIO 2 COMPLETADO")
print("="*70)
