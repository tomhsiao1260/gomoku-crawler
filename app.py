import csv
import requests
from bs4 import BeautifulSoup

rows = []
MAX_PAGE = 5
USER = 'wgg1576g'
DOMAIN = 'https://www.playok.com'
URL = f'{DOMAIN}/zh/stat.phtml?u={USER}&g=gm&sk=2'

filename = f'{USER}.csv'
fieldnames = ['日期 (持續時間)', '玩家', '結果', '對弈連結', '對弈細節']

# crawl through each page
for i in range(MAX_PAGE):
    # send request & turn into BeautifulSoup
    response = requests.get(URL + f'&page={i+1}')
    soup = BeautifulSoup(response.content, 'html.parser')

    # find out all TR element
    table = soup.find('table', {'class': 'ktb'})
    tr = table.find_all('tr')[1:]
    if (len(tr) == 0): break

    # save all data info for each TR element
    for row in tr:
        cells = row.find_all('td') or row.find_all('th')
        data = []
        for cell in cells:
            span = cell.find('span', {'class': 'gr'})
            # find txt file & its URL
            if span:
                a = span.find('a')
                if a:
                    href = a['href']
                    text = requests.get(DOMAIN + href).content
                    data.append(DOMAIN + href)
                    data.append(text)
            else:
                data.append(cell.get_text().strip())
        rows.append(data)
        print(f'DATA{len(rows)}\n{data}\n')

# save as CSV file
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for row in rows:
        writer.writerow(row)

