import pandas as pd
import numpy as np

# Parâmetros da simulação
tempo_total = 300 # 5 minutos de processo
dt = 1.0 # 1 segundo por ciclo
setpoint = 50.0

# Arrays para guardar os dados
tempos = np.arange(0, tempo_total, dt)
temperaturas = np.zeros(len(tempos))
pwms = np.zeros(len(tempos))

# Condições Iniciais (Temperatura Ambiente)
temperatura_atual = 25.0
erro_anterior = 0.0
soma_erro = 0.0

# Parâmetros Ótimos que a nossa IA (Scipy) encontrou
Kp = 12.50
Ki = 0.80
Kd = 3.20

print("Simulando Gêmeo Digital com PID Otimizado...")

for i in range(len(tempos)):
    # 1. Leitura com leve ruído de sensor real (+/- 0.2 °C)
    ruido = np.random.normal(0, 0.2)
    leitura = temperatura_atual + ruido
    
    # 2. Cálculo do Erro
    erro = setpoint - leitura
    soma_erro += erro * dt
    derivada = (erro - erro_anterior) / dt
    
    # 3. PID
    pwm = (Kp * erro) + (Ki * soma_erro) + (Kd * derivada)
    
    # Saturação do PWM (0 a 255)
    pwm = max(0, min(255, pwm))
    
    # 4. Dinâmica do Processo Térmico (Física do aquecimento)
    # A temperatura sobe baseada no PWM, mas perde calor para o ambiente (25°C)
    ganho_aquecedor = 0.015
    perda_ambiente = 0.005 * (temperatura_atual - 25.0)
    temperatura_atual = temperatura_atual + (pwm * ganho_aquecedor) - perda_ambiente
    
    # Salvando dados
    temperaturas[i] = leitura
    pwms[i] = pwm
    erro_anterior = erro

# Criando o DataFrame
df = pd.DataFrame({
    'Tempo_s': tempos,
    'Setpoint': setpoint,
    'Temperatura_C': np.round(temperaturas, 2),
    'Potencia_PWM': np.round(pwms, 0)
})

# Calculando a Estabilidade (Margem de 1.5°C)
df['Erro_Absoluto'] = np.round(np.abs(df['Setpoint'] - df['Temperatura_C']), 2)
df['Status_Estabilidade'] = np.where(df['Erro_Absoluto'] <= 1.5, 'Estável', 'Instável')

# Exportando
df.to_csv('dataset_powerbi.csv', index=False)
print("Novo 'dataset_powerbi.csv' gerado com sucesso! Sistema estabilizado.")
# Substitua as vírgulas originais do CSV por ponto e vírgula
# e converta os pontos decimais para vírgulas (Padrão BR)
df.to_csv('dataset_powerbi.csv', sep=';', decimal=',', index=False)
print("Novo 'dataset_powerbi.csv' gerado no padrão brasileiro (vírgula decimal) com sucesso!")