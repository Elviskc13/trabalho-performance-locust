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
