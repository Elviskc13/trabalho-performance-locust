import pandas as pd
import matplotlib.pyplot as plt


arquivos = {
    "20 usuarios": "resultados/teste_20_stats.csv",
    "75 usuarios": "resultados/teste_75_stats.csv",
    "150 usuarios": "resultados/teste_150_stats.csv"
}

nomes = []
tempos_medios = []


for nome_teste, caminho in arquivos.items():
    print("=" * 50)
    print(f"Resultado do teste: {nome_teste}")
    print("=" * 50)

    dados = pd.read_csv(caminho)

    agregado = dados[dados["Name"] == "Aggregated"]

    if not agregado.empty:
        total_requisicoes = agregado["Request Count"].values[0]
        total_falhas = agregado["Failure Count"].values[0]
        tempo_medio = agregado["Average Response Time"].values[0]
        p90 = agregado["90%"].values[0]
        p95 = agregado["95%"].values[0]
        rps = agregado["Requests/s"].values[0]

        print(f"Total de requisições: {total_requisicoes}")
        print(f"Total de falhas: {total_falhas}")
        print(f"Tempo médio de resposta: {tempo_medio:.2f} ms")
        print(f"Percentil p90: {p90:.2f} ms")
        print(f"Percentil p95: {p95:.2f} ms")
        print(f"Requisições por segundo: {rps:.2f}")
        print()

        nomes.append(nome_teste)
        tempos_medios.append(tempo_medio)

plt.figure()
plt.bar(nomes, tempos_medios)
plt.title("Tempo médio de resposta")
plt.xlabel("Carga de usuários")
plt.ylabel("Tempo médio (ms)")
plt.savefig("graficos/tempo_medio_resposta.png")
plt.close()

print("Gráfico de tempo médio gerado em graficos/tempo_medio_resposta.png")