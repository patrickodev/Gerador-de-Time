import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para calcular o custo de uma divisão de times
def calcular_custo(times):
    custo_total = 0
    atributos = ['velocidade', 'ataque', 'defesa', 'stamina']
    for atributo in atributos:
        medias = [np.mean([j[atributo] for j in time]) for time in times]
        desvio = np.std(medias)
        custo_total += desvio

    medias_totais = [
        np.mean([np.mean([j[attr] for attr in atributos]) for j in time])
        for time in times
    ]
    custo_total += np.std(medias_totais)
    return custo_total

# Função para gerar os times equilibrados
def gerar_times(jogadores):
    melhor_custo = float('inf')
    melhor_divisao = None
    for _ in range(10000):
        np.random.shuffle(jogadores)
        t1, t2, t3 = jogadores[:6], jogadores[6:12], jogadores[12:]
        custo = calcular_custo([t1, t2, t3])
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_divisao = (t1, t2, t3)
    return melhor_divisao

# Função para calcular a média dos atributos por time
def media_por_time(time):
    atributos = ['velocidade', 'ataque', 'defesa', 'stamina']
    return [np.mean([j[attr] for j in time]) for attr in atributos]

# Função para plotar o gráfico radar de cada time
def plotar_radar(times, frame):
    atributos = ['Vel', 'Ata', 'Def', 'Sta']
    fig, axs = plt.subplots(1, 3, subplot_kw={'polar': True}, figsize=(18, 3))
    angulos = np.linspace(0, 2 * np.pi, len(atributos), endpoint=False).tolist()
    atributos_completo = atributos + [atributos[0]]
    angulos_completo = angulos + [angulos[0]]

    for i, time in enumerate(times):
        medias = media_por_time(time)
        medias_completo = medias + [medias[0]]
        ax = axs[i]
        ax.plot(angulos_completo, medias_completo, label=f'Time {i+1}', linewidth=2)
        ax.fill(angulos_completo, medias_completo, alpha=.5)
        ax.set_title(f'Time {i+1}')
        ax.set_xticks(angulos)
        ax.set_xticklabels(atributos)
        ax.set_yticklabels([])

    plt.tight_layout()

    # Desenha o gráfico dentro do frame do Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    plt.close(fig)  # evita gráficos duplicados



# Função chamada ao clicar em "Carregar CSV"
def carregar_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filename:
        return
    try:
        data = pd.read_csv(filename)
        jogadores = data.to_dict(orient='records')
        for j in jogadores:
            for k in ['velocidade', 'ataque', 'defesa', 'stamina']:
                j[k] = int(j[k])
        times = gerar_times(jogadores)
        exibir_times(times)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar o CSV:\n{str(e)}")

# Função para exibir os times e o radar
def exibir_times(times):
    for widget in resultado_frame.winfo_children():
        widget.destroy()

    times_frame = tk.Frame(resultado_frame)
    times_frame.pack(pady=10)

    for i, time in enumerate(times):
        time_frame = tk.Frame(times_frame, bd=2, relief='groove', padx=10, pady=10)
        time_frame.grid(row=0, column=i, padx=50)

        label = tk.Label(time_frame, text=f"Time {i+1}", font=("Arial", 12, "bold"))
        label.pack()
        for j in time:
            info = f"{j['nome']} - Vel: {j['velocidade']}, Atq: {j['ataque']}, Def: {j['defesa']}, Sta: {j['stamina']}"
            tk.Label(time_frame, text=info, font=("Arial", 10)).pack()

    plotar_radar(times, resultado_frame)

# GUI principal
root = tk.Tk()
root.title("Montador de Times de Futebol")
root.geometry("1100x800")

carregar_btn = tk.Button(root, text="Carregar CSV e Gerar Times", command=carregar_csv, font=("Arial", 14))
carregar_btn.pack(pady=20)

resultado_frame = tk.Frame(root)
resultado_frame.pack(fill='both', expand=True)

root.mainloop()