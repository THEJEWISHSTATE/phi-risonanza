# === analisi_grafici.py ===
print("📊 ANALISI GRAFICA RISULTATI 50 REPLICHE")
print("=" * 50)

import json
import numpy as np
import matplotlib.pyplot as plt
import os

# Trova l'ultima cartella risultati
cartelle = [d for d in os.listdir('.') if d.startswith('RISULTATI_50_')]
if not cartelle:
    print("❌ Nessuna cartella risultati trovata!")
    exit()

ultima_cartella = max(cartelle)  # Prende la più recente
print(f"📁 Analisi cartella: {ultima_cartella}")

# Carica risultati completi
with open(f"{ultima_cartella}/RISULTATI_COMPLETI.json", 'r') as f:
    dati = json.load(f)

# Estrai dati
eq_phi = dati['statistiche']['equity']['phi_valori']
ex_phi = dati['statistiche']['extractive']['phi_valori']
eq_tempo = dati['statistiche']['equity']['tempo_valori']
ex_tempo = dati['statistiche']['extractive']['tempo_valori']

print(f"\n📈 DATI CARICATI:")
print(f"   Equity: {len(eq_phi)} valori Φ")
print(f"   Extractive: {len(ex_phi)} valori Φ")

# === CREA GRAFICI ===
plt.figure(figsize=(15, 10))

# 1. Istogramma distribuzione Φ
plt.subplot(2, 3, 1)
plt.hist(eq_phi, alpha=0.7, bins=15, label='Equity', color='blue', density=True)
plt.hist(ex_phi, alpha=0.7, bins=15, label='Extractive', color='red', density=True)
plt.xlabel('Valore Φ finale')
plt.ylabel('Densità')
plt.title('Distribuzione Φ (50 repliche)')
plt.legend()
plt.grid(True, alpha=0.3)

# 2. Boxplot comparativo
plt.subplot(2, 3, 2)
data = [eq_phi, ex_phi]
plt.boxplot(data, labels=['Equity', 'Extractive'])
plt.ylabel('Valore Φ')
plt.title('Boxplot: Equity vs Extractive')
plt.grid(True, alpha=0.3)

# 3. Scatter plot Φ vs Tempo
plt.subplot(2, 3, 3)
plt.scatter(eq_tempo, eq_phi, alpha=0.6, label='Equity', color='blue', s=30)
plt.scatter(ex_tempo, ex_phi, alpha=0.6, label='Extractive', color='red', s=30)
plt.xlabel('Tempo collasso (s)')
plt.ylabel('Φ finale')
plt.title('Φ vs Tempo di collasso')
plt.legend()
plt.grid(True, alpha=0.3)

# 4. Grafico a barre medie
plt.subplot(2, 3, 4)
categorie = ['Equity', 'Extractive']
medie = [np.mean(eq_phi), np.mean(ex_phi)]
errori = [np.std(eq_phi), np.std(ex_phi)]
bars = plt.bar(categorie, medie, yerr=errori, capsize=10, 
               color=['blue', 'red'], alpha=0.7)
plt.ylabel('Φ medio')
plt.title('Φ medio ± deviazione standard')
plt.grid(True, alpha=0.3, axis='y')

# Aggiungi valori sulle barre
for bar, val in zip(bars, medie):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'{val:.3f}', ha='center', va='bottom')

# 5. Coefficiente di variazione
plt.subplot(2, 3, 5)
cv_eq = np.std(eq_phi) / np.mean(eq_phi) * 100
cv_ex = np.std(ex_phi) / np.mean(ex_phi) * 100
plt.bar(['Equity', 'Extractive'], [cv_eq, cv_ex], color=['blue', 'red'])
plt.ylabel('Coefficiente di variazione (%)')
plt.title('CV = (σ/μ) × 100%')
plt.grid(True, alpha=0.3, axis='y')

# 6. Rapporto varianze
plt.subplot(2, 3, 6)
var_ratio = (np.std(ex_phi)**2) / (np.std(eq_phi)**2)
plt.bar(['Rapporto varianze'], [var_ratio], color='purple')
plt.ylabel('Extractive var / Equity var')
plt.title(f'Rapporto varianze: {var_ratio:.1f}x')
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()

# Salva grafico
nome_file = f"{ultima_cartella}/analisi_grafica.png"
plt.savefig(nome_file, dpi=150)
print(f"\n💾 Grafico salvato: {nome_file}")

# === TABELLA RIASSUNTIVA ===
print(f"\n{'='*60}")
print("📋 RIEPILOGO STATISTICO COMPLETO")
print(f"{'='*60}")

print(f"\n{'Metrica':<25} {'Equity':<15} {'Extractive':<15} {'Rapporto':<10}")
print(f"{'-'*25} {'-'*15} {'-'*15} {'-'*10}")

print(f"{'Φ medio':<25} {np.mean(eq_phi):<15.4f} {np.mean(ex_phi):<15.4f} {'':<10}")
print(f"{'Φ dev.std.':<25} {np.std(eq_phi):<15.4f} {np.std(ex_phi):<15.4f} {np.std(ex_phi)/np.std(eq_phi):<10.1f}x")
print(f"{'Φ varianza':<25} {np.var(eq_phi):<15.6f} {np.var(ex_phi):<15.6f} {np.var(ex_phi)/np.var(eq_phi):<10.1f}x")
print(f"{'CV (%)':<25} {cv_eq:<15.2f} {cv_ex:<15.2f} {cv_ex/cv_eq:<10.1f}x")
print(f"{'Tempo medio (s)':<25} {np.mean(eq_tempo):<15.2f} {np.mean(ex_tempo):<15.2f} {'':<10}")
print(f"{'ΔΦ (E - Ex)':<25} {'':<15} {'':<15} {np.mean(eq_phi)-np.mean(ex_phi):<10.4f}")

print(f"\n✅ Analisi completata!")
print(f"📊 Guarda il grafico in: {nome_file}")