**# Φ-RISONANZA: Sistemi Dinamici ad Accordamento**



**Progetto di ricerca che studia il comportamento bifasico di sistemi di oscillatori accoppiati.**



**## 📊 Risultati Chiave**



**\*\*Equity (sistema stabile):\*\***

**- Φ = 0.9952 ± 0.0029**

**- Coefficiente di variazione: 0.30%**

**- Tempo collasso: 1.84s ± 0.17s**



**\*\*Extractive (sistema instabile):\*\***

**- Φ = 0.2502 ± 0.0864**  

**- Coefficiente di variazione: 34.52%**

**- Tempo collasso: 2.28s ± 0.20s**



**\*\*Confronto:\*\***

**- ΔΦ = 0.7450 (differenza enorme)**

**- Rapporto varianze: 857×**

**- Tutte le 5 ipotesi confermate**



**## ✅ Ipotesi Verificate**



**1. \*\*Equity Φ alto\*\* (~0.994): ✅ CONFERMATO**

**2. \*\*Equity stabile\*\* (CV < 5%): ✅ CONFERMATO**  

**3. \*\*Extractive Φ basso\*\* (~0.278): ✅ CONFERMATO**

**4. \*\*Extractive variabile\*\* (CV > 20%): ✅ CONFERMATO**

**5. \*\*Collasso deterministico\*\* (~2.3s): ✅ CONFERMATO**



**## 📁 Struttura**

**00\_DOCUMENTAZIONE/ # Report e documentazione**

**01\_CODICE\_SORGENTE/ # Implementazione sistema**

**02\_DATI\_ORIGINALI/ # Esperimenti iniziali**

**03\_TEST\_ROBUSTEZZA\_50/ # Test 50 repliche**

**04\_SISTEMI\_MISTI/ # Sistemi ibridi**

**05\_REPORT\_FINALI/ # Analisi conclusive**



**text**



**## 🚀 Come Usare**



**```bash**

**# Clona il repository**

**git clone https://github.com/THEJEWISHSTATE/phi-risonanza.git**



**# Vai nel codice**

**cd phi-risonanza/01\_CODICE\_SORGENTE**



**# Esegui test**

**python sistema.py**

**python test\_50\_repliche.py**

**python sistemi\_misti.py**

**📈 Metodologia**

**Sistema: oscillatori di Kuramoto modificati**



**Nodi: 100**



**Parametro accoppiamento: ε = 0.05**



**Repliche: 50 per sistema**



**Metrica: parametro d'ordine Φ ∈ \[0,1]**



**🔮 Prossimi Step**

**Estendere a 100+ repliche**



**Test su reti complesse**



**Applicazioni sistemi reali**



**👤 ANNDREA BERTOTTI\_Ricerca indipendente - THEJEWISHSTATE**



**📄 Licenza**

**MIT License - Vedi LICENSE**

