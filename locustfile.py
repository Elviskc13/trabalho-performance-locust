from locust import HttpUser, task, between


class UsuarioReserva(HttpUser):
    wait_time = between(1, 3)

    @task
    def verificar_api_online(self):
        self.client.get("/ping", name="GET /ping")

    @task(5)
    def listar_reservas(self):
        self.client.get("/booking", name="GET /booking")

    @task(3)
    def filtrar_reservas_por_data(self):
        self.client.get(
            "/booking?checkin=2022-01-01&checkout=2022-12-31",
            name="GET /booking com filtro por data"
        )