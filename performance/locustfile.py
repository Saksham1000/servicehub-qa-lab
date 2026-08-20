import os
from locust import HttpUser,between,task
class ServiceHubUser(HttpUser):
    wait_time=between(1,3)
    def on_start(self):
        r=self.client.post('/api/auth/login',json={'email':os.getenv('LOAD_EMAIL','admin@servicehub.example'),'password':os.getenv('LOAD_PASSWORD','Admin123!')})
        self.headers={'Authorization':f"Bearer {r.json()['access_token']}"} if r.ok else {}
    @task(4)
    def list_services(self):self.client.get('/api/services',name='/api/services')
    @task(2)
    def search_services(self):self.client.get('/api/services?search=massage',name='/api/services?search=[term]')
    @task(2)
    def availability(self):self.client.get('/api/providers/1/availability',name='/api/providers/[id]/availability')
    @task(1)
    def appointments(self):self.client.get('/api/bookings/me',headers=self.headers,name='/api/bookings/me')

