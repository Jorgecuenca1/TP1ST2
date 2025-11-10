"""
Script para ejecutar el Ejercicio 1 y capturar resultados
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import json

# Semilla para reproducibilidad
np.random.seed(42)

print("="*70)
print("EJERCICIO 1: MOVIMIENTO BROWNIANO GEOMÉTRICO")
print("="*70)

# Parámetros del problema
P0 = 60.0          # Precio inicial ($)
mu = 0.20          # Retorno esperado (20% anual)
sigma = 0.40       # Volatilidad (40% anual)
T = 2.0            # Tiempo (2 años)

print("\n" + "="*70)
print("PARÁMETROS DEL MODELO")
print("="*70)
print(f"Precio inicial P(0):    ${P0:.2f}")
print(f"Retorno esperado (mu):  {mu*100:.1f}% anual")
print(f"Volatilidad (sigma):    {sigma*100:.1f}% anual")
print(f"Tiempo (T):             {T} anios")

# PARTE A: Distribución de probabilidad
print("\n" + "="*70)
print("PARTE A: DISTRIBUCIÓN DE PROBABILIDAD")
print("="*70)

mu_ln = np.log(P0) + (mu - 0.5 * sigma**2) * T
sigma_ln = sigma * np.sqrt(T)

print(f"\nLn(P(T)) ~ Normal(mu_ln, sigma_ln^2)")
print(f"donde:")
print(f"  mu_ln = ln(P0) + (mu - sigma^2/2)T = {mu_ln:.6f}")
print(f"  sigma_ln = sigma*sqrt(T) = {sigma_ln:.6f}")
print(f"\nPor lo tanto:")
print(f"  P(T) ~ LogNormal({mu_ln:.4f}, {sigma_ln:.4f})")

# PARTE B: Media, desviación estándar e intervalo de confianza
print("\n" + "="*70)
print("PARTE B: ESTADÍSTICAS Y INTERVALO DE CONFIANZA 95%")
print("="*70)

# Cálculo de la media
media_PT = np.exp(mu_ln + 0.5 * sigma_ln**2)

# Cálculo de la varianza
varianza_PT = np.exp(2*mu_ln + sigma_ln**2) * (np.exp(sigma_ln**2) - 1)
std_PT = np.sqrt(varianza_PT)

# Intervalo de confianza del 95%
alpha = 0.05
IC_lower = stats.lognorm.ppf(alpha/2, s=sigma_ln, scale=np.exp(mu_ln))
IC_upper = stats.lognorm.ppf(1-alpha/2, s=sigma_ln, scale=np.exp(mu_ln))

print(f"\nValor Esperado (Media):")
print(f"  E[P(T)] = ${media_PT:.2f}")
print(f"\nDesviacion Estandar:")
print(f"  sigma[P(T)] = ${std_PT:.2f}")
print(f"\nIntervalo de Confianza 95%:")
print(f"  Limite Inferior = ${IC_lower:.2f}")
print(f"  Limite Superior = ${IC_upper:.2f}")
print(f"  Amplitud = ${IC_upper - IC_lower:.2f}")

# PARTE C: Simulación de Montecarlo
print("\n" + "="*70)
print("PARTE C: SIMULACIÓN DE MONTECARLO")
print("="*70)

n_simulaciones = 100000

print(f"\nEjecutando {n_simulaciones:,} simulaciones...")

# Simulación usando solución exacta
Z = np.random.normal(0, 1, n_simulaciones)
precios_finales_MC = P0 * np.exp((mu - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)

# Estadísticas de la simulación
media_MC = np.mean(precios_finales_MC)
std_MC = np.std(precios_finales_MC, ddof=1)
IC_lower_MC = np.percentile(precios_finales_MC, 2.5)
IC_upper_MC = np.percentile(precios_finales_MC, 97.5)

print(f"\nResultados de la Simulación:")
print(f"  Media MC:              ${media_MC:.2f}")
print(f"  Desv. Std MC:          ${std_MC:.2f}")
print(f"  IC 95% Inferior:       ${IC_lower_MC:.2f}")
print(f"  IC 95% Superior:       ${IC_upper_MC:.2f}")

# COMPARACIÓN
print("\n" + "="*70)
print("COMPARACIÓN: ANALÍTICO vs MONTECARLO")
print("="*70)

error_media = abs(media_PT - media_MC)
error_std = abs(std_PT - std_MC)
error_IC_lower = abs(IC_lower - IC_lower_MC)
error_IC_upper = abs(IC_upper - IC_upper_MC)

error_rel_media = (error_media / media_PT) * 100
error_rel_std = (error_std / std_PT) * 100

print(f"\n{'Metrica':<25} {'Analitico':<15} {'Montecarlo':<15} {'Error Abs':<15} {'Error Rel %':<15}")
print("-" * 85)
print(f"{'Media E[P(T)]':<25} ${media_PT:<14.2f} ${media_MC:<14.2f} ${error_media:<14.2f} {error_rel_media:<14.3f}%")
print(f"{'Desv. Std sigma[P(T)]':<25} ${std_PT:<14.2f} ${std_MC:<14.2f} ${error_std:<14.2f} {error_rel_std:<14.3f}%")
print(f"{'IC 95% Inferior':<25} ${IC_lower:<14.2f} ${IC_lower_MC:<14.2f} ${error_IC_lower:<14.2f}")
print(f"{'IC 95% Superior':<25} ${IC_upper:<14.2f} ${IC_upper_MC:<14.2f} ${error_IC_upper:<14.2f}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
if error_rel_media < 1:
    print(">> EXCELENTE CONCORDANCIA entre resultados analiticos y simulacion")
    print(f"  Error relativo en la media: {error_rel_media:.3f}% < 1%")
else:
    print(f">> Buena concordancia: Error relativo en la media: {error_rel_media:.3f}%")

# Verificacion formula alternativa
media_alternativa = P0 * np.exp(mu * T)
print(f"\nVerificacion usando E[P(T)] = P0*e^(mu*T):")
print(f"  ${media_alternativa:.2f} (diferencia: ${abs(media_PT - media_alternativa):.6f})")

# Guardar resultados
resultados = {
    "parametros": {
        "P0": P0,
        "mu": mu,
        "sigma": sigma,
        "T": T
    },
    "analitico": {
        "mu_ln": float(mu_ln),
        "sigma_ln": float(sigma_ln),
        "media": float(media_PT),
        "std": float(std_PT),
        "IC_lower": float(IC_lower),
        "IC_upper": float(IC_upper)
    },
    "montecarlo": {
        "n_simulaciones": n_simulaciones,
        "media": float(media_MC),
        "std": float(std_MC),
        "IC_lower": float(IC_lower_MC),
        "IC_upper": float(IC_upper_MC)
    },
    "errores": {
        "error_media_absoluto": float(error_media),
        "error_media_relativo": float(error_rel_media),
        "error_std_absoluto": float(error_std),
        "error_std_relativo": float(error_rel_std)
    }
}

with open('resultados_ejercicio1.json', 'w') as f:
    json.dump(resultados, f, indent=2)

print(f"\n>> Resultados guardados en 'resultados_ejercicio1.json'")

print("\n" + "="*70)
print("EJERCICIO 1 COMPLETADO")
print("="*70)
