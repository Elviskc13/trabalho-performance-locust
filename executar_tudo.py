import subprocess
import sys
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


HOST = "https://restful-booker.herokuapp.com"


testes = [
    {
        "nome": "20 usuários",
        "usuarios": 20,
        "taxa": 2,
        "tempo": "1m",
        "saida": "resultados/teste_20",
        "csv": "resultados/teste_20_stats.csv"
    },
    {
        "nome": "75 usuários",
        "usuarios": 75,
        "taxa": 5,
        "tempo": "1m",
        "saida": "resultados/teste_75",
        "csv": "resultados/teste_75_stats.csv"
    },
    {
        "nome": "150 usuários",
        "usuarios": 150,
        "taxa": 10,
        "tempo": "1m",
        "saida": "resultados/teste_150",
        "csv": "resultados/teste_150_stats.csv"
    }
]


def executar_testes():
    for teste in testes:
        print("=" * 60)
        print(f"Executando teste com {teste['nome']}")
        print("=" * 60)

        comando = [
            sys.executable,
            "-m",
            "locust",
            "-f",
            "locustfile.py",
            "--headless",
            "-u",
            str(teste["usuarios"]),
            "-r",
            str(teste["taxa"]),
            "-t",
            teste["tempo"],
            "--host",
            HOST,
            "--csv",
            teste["saida"],
            "--exit-code-on-error",
            "0"
        ]

        subprocess.run(comando, check=True)


def gerar_graficos():
    print("=" * 60)
    print("Gerando gráficos com analisar_resultados.py")
    print("=" * 60)

    subprocess.run([sys.executable, "analisar_resultados.py"], check=True)


def ler_resultados():
    resumo = []

    for teste in testes:
        dados = pd.read_csv(teste["csv"])
        agregado = dados[dados["Name"] == "Aggregated"]

        if not agregado.empty:
            resumo.append({
                "teste": teste["nome"],
                "requisicoes": agregado["Request Count"].values[0],
                "falhas": agregado["Failure Count"].values[0],
                "tempo_medio": agregado["Average Response Time"].values[0],
                "p90": agregado["90%"].values[0],
                "p95": agregado["95%"].values[0],
                "rps": agregado["Requests/s"].values[0]
            })

    return resumo


def gerar_pdf_dinamico(resumo):
    caminho_pdf = "relatorio/relatorio_dinamico.pdf"

    documento = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph(
        "Relatório Dinâmico de Teste de Performance com Locust",
        estilos["Title"]
    ))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("1. Introdução", estilos["Heading1"]))
    elementos.append(Paragraph(
        "Este relatório foi gerado automaticamente após a execução dos testes com Locust. "
        "O sistema utilizado foi a API Restful-Booker, simulando acessos de usuários "
        "em diferentes níveis de carga.",
        estilos["BodyText"]
    ))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("2. Planejamento dos testes", estilos["Heading1"]))
    elementos.append(Paragraph(
        "Foram definidos cenários comuns em uma API de reservas, como consultar reservas, "
        "filtrar por data, abrir detalhes, autenticar e criar uma nova reserva. "
        "As tarefas possuem pesos diferentes para simular um uso mais próximo do real.",
        estilos["BodyText"]
    ))
    elementos.append(Spacer(1, 12))

    dados_cenarios = [
        ["Cenário", "Método", "Endpoint", "Peso"],
        ["Verificar API online", "GET", "/ping", "1"],
        ["Listar reservas", "GET", "/booking", "5"],
        ["Filtrar por data", "GET", "/booking?checkin=...&checkout=...", "3"],
        ["Consultar detalhe", "GET", "/booking/{id}", "4"],
        ["Criar autenticação", "POST", "/auth", "2"],
        ["Criar nova reserva", "POST", "/booking", "1"],
    ]

    tabela_cenarios = Table(
        dados_cenarios,
        colWidths=[5.5 * cm, 2 * cm, 6.5 * cm, 1.5 * cm]
    )

    tabela_cenarios.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elementos.append(tabela_cenarios)
    elementos.append(Spacer(1, 16))

    elementos.append(Paragraph("3. Resultados obtidos", estilos["Heading1"]))

    dados_resultados = [
        ["Teste", "Req.", "Falhas", "Média", "p90", "p95", "Req/s"]
    ]

    for item in resumo:
        dados_resultados.append([
            item["teste"],
            str(item["requisicoes"]),
            str(item["falhas"]),
            f"{item['tempo_medio']:.2f} ms",
            f"{item['p90']:.2f} ms",
            f"{item['p95']:.2f} ms",
            f"{item['rps']:.2f}",
        ])

    tabela_resultados = Table(
        dados_resultados,
        colWidths=[3 * cm, 2 * cm, 1.6 * cm, 2.3 * cm, 2 * cm, 2 * cm, 2 * cm]
    )

    tabela_resultados.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elementos.append(tabela_resultados)
    elementos.append(Spacer(1, 16))

    elementos.append(Paragraph("4. Gráficos", estilos["Heading1"]))

    graficos = [
        "graficos/tempo_medio_resposta.png",
        "graficos/percentis_p90_p95.png",
        "graficos/throughput.png",
        "graficos/falhas.png",
    ]

    for grafico in graficos:
        elementos.append(Image(grafico, width=15 * cm, height=8 * cm))
        elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("5. Análise automática", estilos["Heading1"]))

    maior_tempo = max(resumo, key=lambda item: item["tempo_medio"])
    maior_rps = max(resumo, key=lambda item: item["rps"])
    total_falhas = sum(item["falhas"] for item in resumo)

    elementos.append(Paragraph(
        f"O maior tempo médio de resposta ocorreu no teste com {maior_tempo['teste']}, "
        f"com {maior_tempo['tempo_medio']:.2f} ms.",
        estilos["BodyText"]
    ))
    elementos.append(Spacer(1, 8))

    elementos.append(Paragraph(
        f"O maior throughput ocorreu no teste com {maior_rps['teste']}, "
        f"com {maior_rps['rps']:.2f} requisições por segundo.",
        estilos["BodyText"]
    ))
    elementos.append(Spacer(1, 8))

    elementos.append(Paragraph(
        f"Somando todas as execuções, o total de falhas registradas foi {total_falhas}.",
        estilos["BodyText"]
    ))
    elementos.append(Spacer(1, 8))

    elementos.append(Paragraph(
        "Como os dados vêm diretamente dos arquivos CSV, o relatório pode ser atualizado "
        "executando novamente o arquivo executar_tudo.py.",
        estilos["BodyText"]
    ))

    documento.build(elementos)

    print("PDF dinâmico gerado em relatorio/relatorio_dinamico.pdf")


def main():
    executar_testes()
    gerar_graficos()

    resumo = ler_resultados()

    print("=" * 60)
    print("Gerando PDF dinâmico")
    print("=" * 60)

    gerar_pdf_dinamico(resumo)

    print("=" * 60)
    print("Processo finalizado")
    print("=" * 60)


if __name__ == "__main__":
    main()