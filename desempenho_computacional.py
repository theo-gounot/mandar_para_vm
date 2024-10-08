import psutil
import time
import pandas as pd
import matplotlib.pyplot as plt
import os

# Função para monitorar CPU e RAM ao longo do tempo
def monitor_system(duration=60, interval=1):
    # Listas para armazenar os dados
    cpu_percentages = []
    ram_percentages = []
    timestamps = []

    start_time = time.time()

    while (time.time() - start_time) < duration:
        # Registrar uso de CPU e memória
        cpu_percent = psutil.cpu_percent(interval=interval)
        ram_percent = psutil.virtual_memory().percent

        # Registrar timestamp
        timestamps.append(time.time() - start_time)
        cpu_percentages.append(cpu_percent)
        ram_percentages.append(ram_percent)

        # Printar os valores (opcional)
       # print(f"Tempo: {timestamps[-1]:.2f}s | CPU: {cpu_percent}% | RAM: {ram_percent}%")

    # Retornar os dados
    return timestamps, cpu_percentages, ram_percentages

# Função para encontrar o menor número disponível para a pasta 'teste n'
def get_next_test_folder(base_folder='automacao'):
    n = 1
    while os.path.exists(os.path.join(base_folder, f'teste {n}')):
        n += 1
    return os.path.join(base_folder, f'teste {n}')

# Monitorar por 60 segundos com intervalos de 1 segundo
timestamps, cpu_data, ram_data = monitor_system(duration=100, interval=1)

# Criar um DataFrame com os dados
df = pd.DataFrame({
    'Time (s)': timestamps,
    'CPU Usage (%)': cpu_data,
    'RAM Usage (%)': ram_data
})

# Criar a pasta 'teste n'
test_folder = get_next_test_folder()

# Criar a pasta caso ela não exista
os.makedirs(test_folder, exist_ok=True)

# Salvar o DataFrame como CSV na pasta 'teste n'
csv_path = os.path.join(test_folder, 'teste.csv')
df.to_csv(csv_path, index=False)

# Plotar os gráficos
plt.figure(figsize=(10, 5))
plt.plot(df['Time (s)'], df['CPU Usage (%)'], label='Uso de CPU (%)')
plt.plot(df['Time (s)'], df['RAM Usage (%)'], label='Uso de RAM (%)')
plt.xlabel('Tempo (s)')
plt.ylabel('Uso (%)')
plt.title('Uso de CPU e RAM ao longo do tempo')
plt.legend()
plt.grid(True)

# Salvar o gráfico na pasta 'teste n' como 'teste n.png'
graph_path = os.path.join(test_folder, f'teste {test_folder.split()[-1]}.png')
plt.savefig(graph_path)

print(f'Dados salvos em {csv_path}')
print(f'Gráfico salvo em {graph_path}')
