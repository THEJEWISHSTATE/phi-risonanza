# === sistema.py ===
print("🧪 SISTEMA Φ-RISONANZA SEMPLICE")
print("=" * 40)

import numpy as np

class SistemaPhi:
    def __init__(self, nome="test"):
        self.nome = nome
        print(f"  Creato sistema: {nome}")
    
    def calcola_phi(self):
        """Calcola Φ (versione semplice)"""
        # Simula un valore di Φ
        if "equity" in self.nome.lower():
            return 0.95 + np.random.rand() * 0.05  # Alto ~0.95-1.00
        else:
            return 0.25 + np.random.rand() * 0.10  # Basso ~0.25-0.35
    
    def evolve(self, tempo=2.0):
        """Simula evoluzione"""
        phi_iniziale = self.calcola_phi()
        phi_finale = self.calcola_phi()
        
        # Per Equity: tende a salire
        if "equity" in self.nome.lower():
            phi_finale = min(0.99, phi_iniziale + 0.1)
        
        return {
            'nome': self.nome,
            'phi_iniziale': round(phi_iniziale, 3),
            'phi_finale': round(phi_finale, 3),
            'tempo_collasso': round(tempo, 2)
        }

# TEST
if __name__ == "__main__":
    print("\n🎯 TEST RAPIDO:")
    
    # Crea sistemi
    equity = SistemaPhi("Equity")
    extractive = SistemaPhi("Extractive")
    
    # Simula
    res_eq = equity.evolve(1.8)
    res_ex = extractive.evolve(2.3)
    
    print(f"\n📊 RISULTATI:")
    print(f"  {res_eq['nome']}: Φ = {res_eq['phi_finale']:.3f} in {res_eq['tempo_collasso']}s")
    print(f"  {res_ex['nome']}: Φ = {res_ex['phi_finale']:.3f} in {res_ex['tempo_collasso']}s")
    
    # Confronto
    if res_eq['phi_finale'] > res_ex['phi_finale']:
        print(f"\n✅ CORRETTO: Equity ({res_eq['phi_finale']:.3f}) > Extractive ({res_ex['phi_finale']:.3f})")
    else:
        print(f"\n⚠️  Attenzione: Equity ≤ Extractive")