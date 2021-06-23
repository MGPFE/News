from requests_html import HTMLSession
import time
import csv

session = HTMLSession()

r = session.get("https://www.interia.pl/")

csv_file = open("news.csv", "a", newline="", encoding="utf-8")

writer = csv.writer(csv_file)
for _ in range(2): writer.writerow([])
writer.writerow([time.strftime("%d-%m-%Y %H:%M:%S %Z", time.localtime(time.time()))])

sections = r.html.find(".news")

for index, section in enumerate(sections):
    writer.writerow([])
    section_title = section.find(".header-a")[0].attrs["title"]

    writer.writerow([section_title])
    writer.writerow([])
    writer.writerow(["Tytuł", "Streszczenie", "Link"])

    main_href = section.find(".news-one-a")[0].attrs["href"]

    a = session.get(main_href)

    main_title = a.html.find(".article-title")[0].text
    main_summary = a.html.find(".article-lead")[0].text

    writer.writerow([main_title, main_summary, main_href])

    small_articles = section.find(".news-a")

    for index, article in enumerate(small_articles):
        href = article.attrs["href"]
        a = session.get(href)
        title = a.html.find(".article-title")[0].text
        summary = a.html.find(".article-lead")[0].text

        writer.writerow([title, summary, href])

csv_file.close()
