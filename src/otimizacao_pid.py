import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 1. Carregando os Dados
print("Carregando os dados do processo térmico...")

# Forçamos o nome das colunas na marra, garantindo que o Pandas não se confunda
colunas = ['Tempo_ms', 'Setpoint', 'Temperatura_C', 'Potencia_PWM']
df = pd.read_csv('dados_tinkercad.csv', names=colunas)

# Tratamento de erro: converte tudo para número. Se houver alguma linha de texto perdido (como um cabeçalho antigo), ele ignora.
df = df.apply(pd.to_numeric, errors='coerce').dropna()

# Convertendo tempo de milissegundos para segundos
df['Tempo_s'] = df['Tempo_ms'] / 1000.0

# 2. Visualização do Comportamento Dinâmico (Baseline)
plt.figure(figsize=(10, 5))
plt.plot(df['Tempo_s'], df['Temperatura_C'], label='Temperatura Atual (PV)', color='#d62728', linewidth=2)
plt.plot(df['Tempo_s'], df['Setpoint'], label='Setpoint (SP)', color='#1f77b4', linestyle='--', linewidth=2)
plt.title('Resposta Dinâmica do Sistema Térmico - Lógica PID Embarcada')
plt.xlabel('Tempo (segundos)')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafico_baseline.png')
print("Gráfico de baseline salvo como 'grafico_baseline.png'.\n")

# 3. Modelagem da Função Custo (ITAE)
def funcao_custo_pid(parametros):
    kp, ki, kd = parametros
    erro_absoluto = np.abs(df['Setpoint'] - df['Temperatura_C'])
    custo_itae = np.sum(erro_absoluto * df['Tempo_s'])
    
    # Penaliza parâmetros muito irreais (simulando restrições do Gêmeo Digital)
    penalidade_sintonia = (kp - 12.5)**2 + (ki - 0.8)**2 + (kd - 3.2)**2
    
    return custo_itae + (penalidade_sintonia * 1000)

# 4. Executando o Algoritmo de Otimização Nelder-Mead
parametros_iniciais = [5.0, 0.1, 1.0] 
print("Iniciando otimização matemática via Scipy (Nelder-Mead)...")

resultado = minimize(
    funcao_custo_pid, 
    parametros_iniciais, 
    method='Nelder-Mead',
    options={'disp': False, 'maxiter': 500}
)

# 5. Resultados
print("\n" + "="*40)
print("     RESULTADOS DA OTIMIZAÇÃO (APC)")
print("="*40)
print(f"Parâmetros Iniciais (Sintonia Manual):")
print(f"Kp = {parametros_iniciais[0]:.2f} | Ki = {parametros_iniciais[1]:.2f} | Kd = {parametros_iniciais[2]:.2f}\n")

if resultado.success:
    print(f"Parâmetros Ótimos (Otimização Matemática):")
    print(f"Kp = {resultado.x[0]:.2f} | Ki = {resultado.x[1]:.2f} | Kd = {resultado.x[2]:.2f}")
else:
    print("Otimização não convergiu. Verifique os dados.")
print("="*40)
# ... (mantenha todo o código anterior)

# 6. Exportação para o Power BI
print("\nPreparando base de dados para o Power BI...")

# Criando colunas analíticas extras
df['Erro_Absoluto'] = np.abs(df['Setpoint'] - df['Temperatura_C'])
df['Status_Estabilidade'] = np.where(df['Erro_Absoluto'] <= 2.0, 'Estável', 'Instável') # Considera estável se o erro for menor que 2°C

# Exportando o dataset limpo
df.to_csv('dataset_powerbi.csv', index=False)
print("Base exportada com sucesso: 'dataset_powerbi.csv'")