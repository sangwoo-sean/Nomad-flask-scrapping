import requests
from flask import Flask, render_template, request, send_file, redirect
from bs4 import BeautifulSoup
from scrape import scrape_so, scrape_ro, scrape_ww
import csv

fake_db = {}

def save_to_file(term, jobs):
  file = open(f"{term}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return

app = Flask("LastAssignment")

@app.route("/")
def home():
  return render_template('home.html')

@app.route("/search")
def result():
  term = request.args.get("term").lower()
  if fake_db.get(term):
    db = fake_db[term]
  else:
    db1 = scrape_so(term)
    db2 = scrape_ww(term)
    db3 = scrape_ro(term)
    db = db1 + db2 + db3
    fake_db[term] = db

  return render_template('search.html', term=term, db=db, db_leng=len(db))

@app.route("/expor")
def expor():
  try:
    term = request.args.get("term")
    if not term:
      raise Exception
    term.lower()
    jobs = fake_db.get(term)
    if not jobs:
      raise Exception
    save_to_file(term, jobs)
    return send_file(f"{term}.csv", mimetype='application/x-csv', attachment_filename=f'{term}.csv', as_attachment=True)

  except:
    return redirect("/")
  

app.run(host="0.0.0.0")