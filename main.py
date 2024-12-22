import requests
from bs4 import BeautifulSoup
import json
from bs4 import Tag

url = 'http://quotes.toscrape.com/' 
response = requests.get(url)  
if response.status_code != 200:
    print(f"Ошибка при запросе к сайту: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

quote_elements = soup.find_all('div', class_='quote')  

print(f"Найдено: {len(quote_elements)} цитат")  

list_quotes = []  
list_authors = []  

for quote in quote_elements:  
    text = quote.select_one('.text').get_text(strip=True)
    list_quotes.append(text)

    author = quote.select_one('.author').get_text(strip=True)
    list_authors.append(author)

for i in range(len(list_quotes)): 
    print(f"{i + 1}. Quote: {list_quotes[i]}; Author: {list_authors[i]};")


file_json = "data.json"
writer_list = []

for i in range(len(list_quotes)):
    writer = {'Quote': list_quotes[i], 'Author': list_authors[i]}
    writer_list.append(writer)

print("Записываем данные в файл data.json")
with open(file_json, "w", encoding='utf-8') as file:
    json.dump(writer_list, file, indent=4)

print("Проверяем содержимое файла data.json:")
with open(file_json, "r", encoding='utf-8') as file:
    data = json.load(file)
    print(json.dumps(data, indent=4))  

def generate_html(data_file="data.json", template_file="template.html", output_file="index.html"):
    with open(data_file, "r", encoding="utf-8") as f: 
        quotes = json.load(f)

    with open(template_file, "r", encoding="utf-8") as f: 
        template = f.read()

    soup = BeautifulSoup(template, "html.parser")  
    container = soup.find("div", class_="place-here")  
    if not container:
        raise ValueError("В шаблоне отсутствует элемент с классом 'place-here' для вставки таблицы.")

    table = Tag(name="table", attrs={"class": "quotes-table"})  

    
    thead = Tag(name="thead") 
    tr_head = Tag(name="tr")
    headers = ["№", "Quotes", "Author"]
    for header in headers:
        th = Tag(name="th")
        th.string = header
        tr_head.append(th)
    thead.append(tr_head)
    table.append(thead)

   
    tbody = Tag(name="tbody")
    for idx, quote in enumerate(quotes, start=1):
        tr = Tag(name="tr")

        td_num = Tag(name="td")
        td_num.string = str(idx)
        tr.append(td_num)

        td_quote = Tag(name="td")
        td_quote.string = quote["Quote"]
        tr.append(td_quote)

        td_author = Tag(name="td")
        td_author.string = quote["Author"]  
        tr.append(td_author)

        tbody.append(tr)
    table.append(tbody)

   
    container.append(table)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())


generate_html()
print("HTML файл создан: index.html")