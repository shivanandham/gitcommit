import requests
from pprint import pprint
import json

url = f"https://api.github.com/repos/flutter/flutter/commits"
params = {
    "method": "GET",
    "headers" : "application/vnd.github.v3+json",
    "authorization" : "token 1f18f201a6b3fbbee95c5e3680789b6561c4f0d7",
    "per_page": "100"
}
since = ""
until = ""

start = input("Enter the start date: ")
end = input("Enter the end date: ")

if not start:
    if end:
        until+=(end[6:10]+"-"+end[3:5]+"-"+end[0:2])
        params["until"] = until
if not end:
    if start:
        since+=(start[6:10]+"-"+start[3:5]+"-"+start[0:2])
        params["since"] = since
if start:
    if end:
        since+=(start[6:10]+"-"+start[3:5]+"-"+start[0:2])
        untill+=(end[6:10]+"-"+end[3:5]+"-"+end[0:2])
        params["since"] = since
        params["until"] = until



response = requests.get(url= url , params= params)
data = response.json()


while 'next'in response.links.keys():
    response=requests.get(response.links['next']['url'],params=params)
    data.extend(response.json())

with open('test.json', 'w') as outfile:
    json.dump(data, outfile)

f = open('test.json', 'r')
data = json.loads(f.read())

temp = []

for i in range(len(data)):
    temp.append(data[i]['commit']['author']['name'])

temp = dict((k,0) for k in temp)

for i in range(len(data)):
    if data[i]['commit']['author']['name'] in temp:
        temp[data[i]['commit']['author']['name']] += 1

author = max(temp, key=temp.get)
number = temp[author]

temp =[]

for i in range(len(data)):
    if data[i]['commit']['author']['name'] == author:
        temp.append(data[i]['commit']['author']['date'][:10])

temp = dict((k,0) for k in temp)

for i in range(len(data)):
    if data[i]['commit']['author']['date'][:10] in temp:
        temp[data[i]['commit']['author']['date'][:10]] += 1

date = max(temp, key=temp.get)
date = str(date[8:10]+"/"+date[5:7]+"/"+date[0:4])

print("User name: {}\nNo of commits: {}\nDay in which user has high no of commit: {}".format(author, number, date))
