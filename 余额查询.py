import http.client
import json

conn = http.client.HTTPSConnection("api.chatanywhere.tech")
payload = json.dumps({
   "model": "gpt-3.5-turbo%",
   "hours": 24
})
headers = {
   'Authorization': 'sk-qPQtTU47NOASDBYmjpu6nPMad959c6ZbR53OkufCAfFjw7yJ',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
conn.request("POST", "/v1/query/usage_details", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))