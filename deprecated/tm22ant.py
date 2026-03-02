import http.client

conn = http.client.HTTPSConnection("api.scrapingant.com")

headers = {
    'x-api-key': "61ad5504be314580926ac033dfc25baf",
    
}

conn.request("GET", "/v1/general?url=https%3A%2F%2Fwww.transfermarkt.de%2Fbundesliga%2Fmarktwerte%2Fwettbewerb%2FL1%2Fajax%2Fyw1%2Fpos%2F%2Fdetailpos%2F0%2Faltersklasse%2Falle%2Fpage%2F2&return_text=true", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))