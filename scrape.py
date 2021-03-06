import requests
from bs4 import BeautifulSoup

so_url = "https://stackoverflow.com/jobs?r=true&q="
base_so_url = "https://stackoverflow.com"
ww_url = "https://weworkremotely.com/remote-jobs/search?term="
base_ww_url = "https://weworkremotely.com"
ro_url = "https://remoteok.io/remote-dev+"
base_ro_url = "https://remoteok.io"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def scrape_so(term):
  db = []

  url = so_url + term
  req = requests.get(url).text
  soup = BeautifulSoup(req, "html.parser")
  try:
    pages = soup.find(class_="s-pagination").find_all(class_="s-pagination--item")
    last_page = int(pages[-4].text.strip())
  except:
    last_page = 1
  # for i in pages[:-3]:
    # page= int(i.text.strip()

  for page in range(1, last_page+1):
    last_url = url+"&r=true&pg="+str(page)
    print("scrapping " + last_url)
    req = requests.get(last_url).text
    soup = BeautifulSoup(req, "html.parser")
    job_box = soup.find(class_="listResults")
    jobs = job_box.find_all(class_="js-result", recursive=False)
    for job in jobs:
      try:
        info = {}
        title = job.find(class_="stretched-link").text
        company = job.find(class_="fc-black-700").find("span").text.strip()
        link = job.find(class_="stretched-link")['href']

        info["title"] = title
        info["company"] = company
        info["link"] = base_so_url + link
        db.append(info)
      except:
        continue
  return db


def scrape_ww(term):
  db = []
  url = ww_url + term
  req = requests.get(url).text
  soup = BeautifulSoup(req, "html.parser")
  job_box = soup.find("article").find("ul")
  jobs = job_box.find_all("li")
  print("scrapping " + url)
  for job in jobs:
    try:
      info = {}
      link = job.find("a")['href']
      title = job.find(class_="title").text
      company = job.find(class_="company").text

      info["title"] = title
      info["company"] = company
      info["link"] = base_ww_url + link
      db.append(info)
    except:
      continue
  return db


def scrape_ro(term):
  db = []
  url = ro_url + term + "-jobs"
  print("scrapping " + url)
  req = requests.get(url, headers=headers).text
  soup = BeautifulSoup(req, "html.parser")
  tables = soup.find("table", id="jobsboard").find_all(class_="job")
  for table in tables:
    try:
      info = {}
      link = table.find(class_="preventLink")['href']
      title = table.find("h2", {"itemprop":"title"}).text
      company = table.find("h3", {"itemprop":"name"}).text

      info["title"] = title
      info["company"] = company
      info["link"] = base_ro_url + link
      db.append(info)
    except:
      continue
  return db


