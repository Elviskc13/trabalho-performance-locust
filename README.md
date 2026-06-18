# trabalho-performance-locust

## Sistema escolhido

O sistema escolhido para este trabalho foi o Restful-Booker, uma API pública criada para prática de testes em sistemas web.

O sistema simula uma aplicação de reservas de hotel, permitindo consultar reservas, buscar detalhes, criar autenticação e cadastrar novas reservas.

A escolha foi feita porque o sistema possui endpoints acessíveis para testes, permite o uso de requisições GET e POST, pode ser utilizado sem afetar sistemas reais de produção.

## Objetivo do teste de performance

O objetivo deste teste é avaliar o comportamento da API Restful-Booker sob diferentes níveis de carga, observando o tempo de resposta, a quantidade de requisições por segundo, a ocorrência de falhas e o comportamento geral do sistema conforme o número de usuários simultâneos aumenta.

## Planejamento dos cenários de teste

Para o teste de performance foram escolhidos 6 cenários da API Restful-Booker. A ideia foi simular ações comuns em um sistema de reservas, como consultar reservas, buscar por data, abrir detalhes, autenticar e criar uma nova reserva.

| Cenário                          | Método | Endpoint                            | Peso |
| -------------------------------- | ------ | ----------------------------------- | ---- |
| Verificar se a API está online   | GET    | `/ping`                             | 1    |
| Listar reservas                  | GET    | `/booking`                          | 5    |
| Filtrar reservas por data        | GET    | `/booking?checkin=...&checkout=...` | 3    |
| Consultar detalhe de uma reserva | GET    | `/booking/{id}`                     | 4    |
| Criar autenticação               | POST   | `/auth`                             | 2    |
| Criar nova reserva               | POST   | `/booking`                          | 1    |

Usei pesos diferentes porque nem todas as ações acontecem com a mesma frequência. A listagem de reservas recebeu peso maior, pois é uma consulta mais comum. Já a criação de reserva ficou com peso menor, porque normalmente é uma ação menos frequente. Com isso, o teste fica mais próximo de um uso real do sistema.

## Justificativa da carga de usuários

Os testes serão executados com 20, 75 e 150 usuários simultâneos.

Com 20 usuários, a ideia é fazer uma carga inicial mais baixa, para verificar se os cenários funcionam corretamente e se a API responde sem falhas.

Com 75 usuários, o teste passa para uma carga intermediária. Nessa etapa é possível observar se o tempo de resposta começa a aumentar e se a API consegue manter uma boa quantidade de requisições por segundo.

Com 150 usuários, o objetivo é aplicar uma carga mais alta, procurando sinais de lentidão, falhas ou gargalos nos endpoints mais utilizados.

Esses três níveis foram escolhidos para comparar o comportamento da API conforme a quantidade de usuários simultâneos aumenta.

## Execução dos testes

Os testes serão executados em modo headless, ou seja, sem usar a interface web do Locust. Também será usado o parâmetro `--csv` para salvar os resultados dentro da pasta `resultados`.

### Teste com 20 usuários

```bash
python -m locust -f locustfile.py --headless -u 20 -r 2 -t 1m --host https://restful-booker.herokuapp.com --csv resultados/teste_20
```

### Teste com 75 usuários

```bash
python -m locust -f locustfile.py --headless -u 75 -r 5 -t 1m --host https://restful-booker.herokuapp.com --csv resultados/teste_75
```

### Teste com 150 usuários

```bash
python -m locust -f locustfile.py --headless -u 150 -r 10 -t 1m --host https://restful-booker.herokuapp.com --csv resultados/teste_150
```

Cada execução gera arquivos CSV com os dados do teste, como número de requisições, falhas, tempo médio de resposta, requisições por segundo.

## Como instalar o projeto

Para executar o projeto localmente, primeiro é necessário instalar as dependências do Python.

```bash
pip install -r requirements.txt
```

As principais bibliotecas usadas foram:

* Locust, para executar os testes de performance;
* pandas, para ler e organizar os resultados em CSV;
* matplotlib, para gerar os gráficos.

## Como executar com interface web

Para abrir o Locust com interface gráfica, use o comando:

```bash
python -m locust -f locustfile.py --host https://restful-booker.herokuapp.com
```

Depois acesse no navegador:

```text
http://localhost:8089
```

Na tela do Locust é possível informar a quantidade de usuários e a taxa de subida manualmente para acompanhar o teste em tempo real.

## Como executar com Docker

Também é possível executar o projeto usando Docker e Docker Compose.

Para subir o Locust pelo Docker, use:

```bash
docker compose up --build
```

Depois acesse no navegador:

```text
http://localhost:8089
```

Na tela do Locust, informe a quantidade de usuários, a taxa de subida e mantenha o host como:

```text
https://restful-booker.herokuapp.com
```

Para parar a execução, use `CTRL + C` no terminal e depois rode:

```bash
docker compose down
```
## Como gerar os gráficos

Depois de executar os testes e gerar os arquivos CSV dentro da pasta `resultados`, os gráficos podem ser gerados com o comando:

```bash
python analisar_resultados.py
```

Esse script lê os arquivos CSV dos testes com 20, 75 e 150 usuários, mostra um resumo no terminal e gera os gráficos dentro da pasta `graficos`.

Os gráficos gerados são:

* tempo médio de resposta;
* percentis p90 e p95;
* throughput, ou seja, requisições por segundo;
* total de falhas.

## Estrutura do projeto

```text
trabalho-performance-locust/
│
├── locustfile.py
├── analisar_resultados.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
│
├── resultados/
│   ├── teste_20_stats.csv
│   ├── teste_75_stats.csv
│   └── teste_150_stats.csv
│
├── graficos/
│   ├── tempo_medio_resposta.png
│   ├── percentis_p90_p95.png
│   ├── throughput.png
│   └── falhas.png
│
└── relatorio/
    ├── relatorio.md
    └── relatorio.pdf
```