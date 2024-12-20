import requests
  
url = "https://scraper-api.smartproxy.com/v2/scrape"
  
payload = {
      "url": "http://httpbin.org/ip",
      "geo": "Japan"
}
  
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "96053157820b4746e3e621bba69c1c776c14ecbbe42329c70612156cfdb9b18772bf95798a1b17cdf7250a237928977dd27d7b8dd86bcbbe7931971c14e852bef5590416301ba05aae6db1fa0cefaa1e"
}
  
response = requests.post(url, json=payload, headers=headers)
  
print(response.text)