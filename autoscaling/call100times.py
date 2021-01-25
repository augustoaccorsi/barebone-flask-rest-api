import requests

url = "http://flask-env.eba-n6uz9bum.us-east-1.elasticbeanstalk.com/"

for i in range(100):
    res = requests.get(url) 
    print("Call " + str(i+1) + " : " + str(res.status_code))