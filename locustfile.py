from locust import HttpUser, task, between


class UsuarioReserva(HttpUser):
    wait_time = between(1, 3)

    @task
    def verificar_api_online(self):
        self.client.get("/ping", name="GET /ping")
