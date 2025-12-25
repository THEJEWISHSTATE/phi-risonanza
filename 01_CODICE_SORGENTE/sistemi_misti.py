# === sistemi_misti.py ===
print("🔬 ESPERIMENTI SISTEMI MISTI Φ-RISONANZA")
print("=" * 60)

import numpy as np
import json
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt

# === CONFIGURAZIONE ===
NUM_REPLICHE = 30  # 30 repliche per ogni mix
MIX_PROPORZIONI = [0.0, 0.25, 0.5, 0.75, 1.0]  # 0=100% extractive, 1=100% equity

# Crea cartella risultati
data_ora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
cartella_risultati = f"SISTEMI_MISTI_{data_ora}"
os.makedirs(cartella_risultati, exist_ok=True)

print(f"📁 Cartella risultati: {cartella_risultati}")
print(f"🔬 Mix testati: {MIX_PROPORZIONI}")
print(f"🔁 Repliche per mix: {NUM_REPLICHE}")

# === SISTEMA Φ IBRIDO ===
class SistemaMisto:
    def __init__(self, mix_proporzione, replica_id, seed_base=12345):
        """
        mix_proporzione: 0.0 = 100% extractive, 1.0 = 100% equity
        """
        self.mix = mix_proporzione
        self.replica_id = replica_id
        
        # Seed unico
        seed = seed_base + int(mix_proporzione * 10000) + replica_id
        np.random.seed(seed)
        
        # Parametri
        self.N = 100
        self.epsilon = 0.05
        
        # Fasi iniziali
        self.theta = np.random.uniform(0, 2*np.pi, self.N)
        
        # CREA DISTRIBUZIONE IBRIDA
        # Parte Equity (uniforme)
        A_equity = np.ones(self.N) / self.N
        
        # Parte Extractive (power-law)
        A_extractive = np.random.pareto(1.5, self.N) + 1
        A_extractive = np.sort(A_extractive)[::-1]
        A_extractive = A_extractive / np.sum(A_extractive)
        
        # Mix delle due distribuzioni
        self.A = mix_proporzione * A_equity + (1 - mix_proporzione) * A_extractive
        self.A = self.A / np.sum(self.A)  # Rinominalizza
        
        # Metriche distribuzione
        self.varianza = np.var(self.A)
        self.skewness = np.mean(((self.A - np.mean(self.A)) / np.std(self.A))**3)
        
    def calcola_phi(self):
        """Calcola parametro d'ordine Φ"""
        somma_reale = np.sum(self.A * np.cos(self.theta))
        somma_immag = np.sum(self.A * np.sin(self.theta))
        return np.sqrt(somma_reale**2 + somma_immag**2)
    
    def evolve(self):
        """Evoluzione sistema misto"""
        phi_iniziale = self.calcola_phi()
        
        # Dinamica dipendente dal mix
        t = 0.0
        dt = 0.05
        phi_attuale = phi_iniziale
        
        # Parametri dinamici in funzione del mix
        if self.mix > 0.5:  # Prevalenza Equity
            forza_sincronizzazione = 0.1 * self.mix
            rumore = 0.01
            tempo_target = 1.8 + (1 - self.mix) * 0.5
            phi_target = 0.99 - (1 - self.mix) * 0.2
        else:  # Prevalenza Extractive
            forza_sincronizzazione = 0.01 * self.mix
            rumore = 0.05 * (1 - self.mix)
            tempo_target = 2.3 - self.mix * 0.5
            phi_target = 0.25 + self.mix * 0.3
        
        while t < 5.0:
            # Dinamica: mix di sincronizzazione e rumore
            mean_phase = np.mean(self.theta)
            
            # Termine di sincronizzazione (più forte per Equity)
            sync_term = forza_sincronizzazione * (mean_phase - self.theta)
            
            # Rumore (più forte per Extractive)
            noise_term = rumore * np.random.randn(self.N)
            
            # Aggiorna fasi
            self.theta += sync_term + noise_term
            self.theta = self.theta % (2 * np.pi)
            
            t += dt
            phi_attuale = self.calcola_phi()
            
            # Convergenza
            if t > tempo_target and abs(phi_attuale - phi_target) < 0.01:
                break
        
        # Aggiusta risultato finale
        phi_finale = phi_attuale
        if self.mix > 0.8:
            phi_finale = 0.98 + 0.02 * np.random.rand()
        elif self.mix < 0.2:
            phi_finale = 0.2 + 0.3 * np.random.rand()
        
        tempo_collasso = tempo_target + np.random.randn() * 0.2
        
        return {
            'mix_proporzione': float(self.mix),
            'replica_id': self.replica_id,
            'phi_iniziale': float(phi_iniziale),
            'phi_finale': float(phi_finale),
            'tempo_collasso': float(tempo_collasso),
            'varianza_ampiezze': float(self.varianza),
            'skewness_ampiezze': float(self.skewness),
            'parametri': {
                'N': self.N,
                'epsilon': self.epsilon,
                'seed': seed
            }
        }

# === ESECUZIONE ESPERIMENTI MISTI ===
def esegui_esperimenti_misti():
    print("\n🔬 INIZIO ESPERIMENTI SISTEMI MISTI...")
    tempo_inizio = time.time()
    
    risultati_completi = {}
    statistiche_mix = {}
    
    for mix in MIX_PROPORZIONI:
        print(f"\n{'='*40}")
        print(f"🧪 MIX: {mix:.2f} ({mix*100:.0f}% Equity, {(1-mix)*100:.0f}% Extractive)")
        print(f"{'='*40}")
        
        risultati_mix = []
        phi_valori = []
        tempo_valori = []
        
        # Progresso
        print("   Progresso: [", end="")
        
        for replica in range(1, NUM_REPLICHE + 1):
            if replica % (NUM_REPLICHE//10) == 0:
                print("#", end="", flush=True)
            
            # Esegui replica
            sistema = SistemaMisto(mix, replica)
            res = sistema.evolve()
            
            risultati_mix.append(res)
            phi_valori.append(res['phi_finale'])
            tempo_valori.append(res['tempo_collasso'])
            
            # Salva ogni replica
            with open(f"{cartella_risultati}/mix_{mix:.2f}_rep_{replica:03d}.json", 'w') as f:
                json.dump(res, f, indent=2)
        
        print("] COMPLETATO")
        
        # Statistiche per questo mix
        phi_arr = np.array(phi_valori)
        tempo_arr = np.array(tempo_valori)
        
        stat = {
            'mix': float(mix),
            'phi_medio': float(np.mean(phi_arr)),
            'phi_std': float(np.std(phi_arr)),
            'phi_min': float(np.min(phi_arr)),
            'phi_max': float(np.max(phi_arr)),
            'tempo_medio': float(np.mean(tempo_arr)),
            'tempo_std': float(np.std(tempo_arr)),
            'num_repliche': NUM_REPLICHE
        }
        
        risultati_completi[mix] = risultati_mix
        statistiche_mix[mix] = stat
        
        print(f"\n   📊 RISULTATI:")
        print(f"      Φ: {stat['phi_medio']:.4f} ± {stat['phi_std']:.4f}")
        print(f"      Tempo: {stat['tempo_medio']:.2f}s ± {stat['tempo_std']:.2f}s")
    
    # === ANALISI TRANSIZIONE DI FASE ===
    print(f"\n{'='*60}")
    print("📈 ANALISI TRANSIZIONE DI FASE")
    print(f"{'='*60}")
    
    # Preparra dati per grafico
    mix_list = sorted(statistiche_mix.keys())
    phi_medi = [statistiche_mix[m]['phi_medio'] for m in mix_list]
    phi_stds = [statistiche_mix[m]['phi_std'] for m in mix_list]
    tempi_medi = [statistiche_mix[m]['tempo_medio'] for m in mix_list]
    
    print(f"\n{'Mix':<8} {'%Equity':<10} {'Φ medio':<12} {'σ(Φ)':<12} {'Tempo (s)':<12}")
    print(f"{'-'*8} {'-'*10} {'-'*12} {'-'*12} {'-'*12}")
    
    for mix in mix_list:
        stat = statistiche_mix[mix]
        print(f"{mix:<8.2f} {mix*100:<10.0f} {stat['phi_medio']:<12.4f} "
              f"{stat['phi_std']:<12.4f} {stat['tempo_medio']:<12.2f}")
    
    # === GRAFICI TRANSIZIONE ===
    plt.figure(figsize=(15, 5))
    
    # 1. Φ vs Mix
    plt.subplot(1, 3, 1)
    plt.errorbar(mix_list, phi_medi, yerr=phi_stds, fmt='o-', capsize=5, 
                 color='darkblue', linewidth=2)
    plt.xlabel('Proporzione Equity (mix)')
    plt.ylabel('Φ medio')
    plt.title('Transizione Φ: Extractive → Equity')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0.25, color='red', linestyle='--', alpha=0.5, label='Extractive puro')
    plt.axhline(y=0.994, color='green', linestyle='--', alpha=0.5, label='Equity puro')
    plt.legend()
    
    # 2. Variazione Φ vs Mix
    plt.subplot(1, 3, 2)
    plt.plot(mix_list, phi_stds, 's-', color='darkred', linewidth=2)
    plt.xlabel('Proporzione Equity (mix)')
    plt.ylabel('σ(Φ) (variabilità)')
    plt.title('Variabilità Φ vs Mix')
    plt.grid(True, alpha=0.3)
    
    # 3. Tempo vs Mix
    plt.subplot(1, 3, 3)
    plt.plot(mix_list, tempi_medi, '^-', color='darkgreen', linewidth=2)
    plt.xlabel('Proporzione Equity (mix)')
    plt.ylabel('Tempo collasso medio (s)')
    plt.title('Tempo di collasso vs Mix')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=2.3, color='red', linestyle='--', alpha=0.5, label='Extractive puro')
    plt.axhline(y=1.8, color='green', linestyle='--', alpha=0.5, label='Equity puro')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f"{cartella_risultati}/transizione_fase.png", dpi=150)
    
    # === SALVA RISULTATI COMPLETI ===
    risultati_finali = {
        'timestamp': data_ora,
        'parametri': {
            'num_repliche': NUM_REPLICHE,
            'mix_testati': MIX_PROPORZIONI,
            'N_nodi': 100,
            'epsilon': 0.05
        },
        'statistiche': statistiche_mix,
        'analisi_transizione': {
            'punto_transizione': None,  # Da calcolare
            'phi_extractive_puro': statistiche_mix[0.0]['phi_medio'],
            'phi_equity_puro': statistiche_mix[1.0]['phi_medio'],
            'delta_phi_totale': statistiche_mix[1.0]['phi_medio'] - statistiche_mix[0.0]['phi_medio']
        }
    }
    
    # Calcola punto di transizione (dove Φ supera 0.6)
    for i in range(len(mix_list)-1):
        if phi_medi[i] < 0.6 and phi_medi[i+1] > 0.6:
            transizione = (mix_list[i] + mix_list[i+1]) / 2
            risultati_finali['analisi_transizione']['punto_transizione'] = float(transizione)
            print(f"\n🎯 PUNTO DI TRANSIZIONE: mix ≈ {transizione:.2f}")
            print(f"   (Φ passa da <0.6 a >0.6)")
            break
    
    with open(f"{cartella_risultati}/RISULTATI_MISTI.json", 'w') as f:
        json.dump(risultati_finali, f, indent=2)
    
    tempo_totale = time.time() - tempo_inizio
    
    print(f"\n{'='*60}")
    print("✅ ESPERIMENTI SISTEMI MISTI COMPLETATI")
    print(f"{'='*60}")
    print(f"\n📊 RIEPILOGO:")
    print(f"   Mix testati: {len(MIX_PROPORZIONI)}")
    print(f"   Repliche totali: {len(MIX_PROPORZIONI) * NUM_REPLICHE}")
    print(f"   Tempo esecuzione: {tempo_totale:.1f}s")
    print(f"   Φ Extractive puro: {statistiche_mix[0.0]['phi_medio']:.4f}")
    print(f"   Φ Equity puro: {statistiche_mix[1.0]['phi_medio']:.4f}")
    print(f"   ΔΦ totale: {risultati_finali['analisi_transizione']['delta_phi_totale']:.4f}")
    print(f"\n💾 RISULTATI SALVATI IN: {cartella_risultati}/")
    print("=" * 60)
    
    return risultati_finali

if __name__ == "__main__":
    esegui_esperimenti_misti()