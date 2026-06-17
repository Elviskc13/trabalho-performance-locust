from locust import HttpUser, task, between
import random

class UsuarioReserva(HttpUser):
    wait_time = between(1, 3)
    def on_start(self):
        self.ids_reservas = []

    @task
    def verificar_api_online(self):
        self.client.get("/ping", name="GET /ping")

    @task(5)
    def listar_reservas(self):
        resposta = self.client.get("/booking", name="GET /booking")

        if resposta.status_code == 200:
            reservas = resposta.json()

            if reservas:
                self.ids_reservas = [
                    reserva["bookingid"] for reserva in reservas[:10]
                ]

    @task(3)
    def filtrar_reservas_por_data(self):
        self.client.get(
            "/booking?checkin=2022-01-01&checkout=2022-12-31",
            name="GET /booking com filtro por data"
        )

    @task(4)
    def consultar_detalhe_reserva(self):
        if self.ids_reservas:
            reserva_id = random.choice(self.ids_reservas)

        self.client.get(
            f"/booking/{reserva_id}",
            name="GET /booking/{id}"
        )
    
    @task(2)
    def criar_token_autenticacao(self):
        dados_login = {
            "username": "admin",
            "password": "password123"
        }

        self.client.post(
            "/auth",
            json=dados_login,
            name="POST /auth"
        )

    @task(1)
    def criar_reserva(self):
        nova_reserva = {
            "firstname": "Elvis",
            "lastname": "Aula",
            "totalprice": random.randint(100, 500),
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-07-01",
                "checkout": "2026-07-05"
            },
            "additionalneeds": "Breakfast"
        }

        self.client.post(
            "/booking",
            json=nova_reserva,
            headers={"Content-Type": "application/json"},
            name="POST /booking"
        )