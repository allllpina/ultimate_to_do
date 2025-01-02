import requests

url = "http://localhost:5000/predict"

data = {"features": [[158,  20.0,   39, 1]]} # 2
response = requests.post(url, json=data)
print("Прогноз:", response.json())

data = {"features": [[387,  2.0,   50, 5]]} # 3
response = requests.post(url, json=data)
print("Прогноз:", response.json())

data = {"features": [[25,  24.0,   51, 1]]} # 1
response = requests.post(url, json=data)
print("Прогноз:", response.json())