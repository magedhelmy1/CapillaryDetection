from locust import HttpUser, task, constant


class TestImage(HttpUser):
    host = "http://64.227.106.224/"

    @task
    def get_users(self):
        self.client.get(url="api/hello/")
