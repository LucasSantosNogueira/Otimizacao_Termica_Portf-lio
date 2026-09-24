# 🏭 Otimização Térmica e Monitoramento Industrial (Gêmeo Digital)

Um estudo de caso de engenharia de processos focado em **Controle Avançado de Processos (APC)** e **Sistemas Supervisórios**. O projeto integra a simulação de uma malha de controle PID com otimização numérica em Python e visualização analítica em tempo quase-real no Power BI.

---

## 📌 Visão Geral do Problema
Sistemas térmicos industriais (como reatores e trocadores de calor) sujeitos a controle manual ou sintonia inadequada apresentam alta variabilidade, gerando instabilidade operacional, consumo excessivo de energia e risco de desgaste do equipamento por overshooting.

**Objetivo:** Desenvolver um gêmeo digital do processo térmico para recalibrar as constantes do controlador PID ($K_p$, $K_i$, $K_d$) e construir um painel supervisório estático (estilo SCADA) para monitoramento de estabilidade.

---

## 🛠️ Tecnologias e Ferramentas
* **Python (NumPy, SciPy, Pandas):** Algoritmo de otimização numérica (*Nelder-Mead*) para minimização da função custo (Erro Quadrático Médio) e geração do modelo de dados.
* **C++ / Tinkercad:** Validação lógica e temporização da resposta do processo.
* **Power BI:** Modelagem em DAX e desenvolvimento do dashboard supervisório com estética SCADA.
* **Git & GitHub:** Versionamento de código e documentação.

---

## 📊 Arquitetura do Projeto e Resultados

### 1. Sintonia Fina do Controlador (Python / SciPy)
A malha PID foi submetida a uma função objetivo de minimização de erro em relação ao *Setpoint* de temperatura fixado em **60 °C**.

* **Parâmetros Otimizados:**
  * $K_p$ (Ganho Proporcional): **12,50**
  * $K_i$ (Ganho Integral): **0,80**
  * $K_d$ (Ganho Derivativo): **3,20**

### 2. Indicadores do Dashboard (Power BI)
* **Desvio Médio do Processo (Offset):** Redução drástica da oscilação após o período de transição.
* **Índice de Estabilidade da Malha:** Medida em DAX avaliando a porcentagem de tempo em que a temperatura variou em $\pm 1,5^\circ\text{C}$ do Setpoint em regime permanente.
* **Sinal de Atuação (PWM):** Análise do esforço do elemento final de controle para otimização de consumo energético.

---

## 📁 Estrutura do Repositório

```text
├── src/
│   ├── otimizacao_pid.py       # Algoritmo de otimização em Python (SciPy)
│   └── gerar_dados_finais.py   # Simulação do processo térmico
├── data/
│   └── dataset_powerbi.csv     # Dados do processo formatados
├── dashboard/
│   └── relatorio_pid.pbix      # Painel Power BI
├── .gitignore
└── README.md
