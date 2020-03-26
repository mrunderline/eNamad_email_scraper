from bs4 import BeautifulSoup
from requests import get
import re

emails = []
sites = []

with open('sites.txt') as f:
    sites = f.readlines()

for site in sites:
    site = site.replace('\n', '')
    print('<<< === ', site, ' === >>>')
    try:
        r = get(site)
        if r.status_code != 200:
            continue

        content = r.text
        for line in content.split('<div'):
            if 'trustseal.enamad.ir' in line:
                link_uniq = 'https://trustseal.enamad.ir/?id='
                if 'Verify.aspx' in line:
                    link_uniq = 'https://trustseal.enamad.ir/Verify.aspx'
                i = line.index(link_uniq)
                j = i + 80
                if '&quot' in line[i:]:
                    j = line[i:].index('&quot')
                elif '"' in line[i:]:
                    j = line[i:].index('"')

                saman_link = line[i:i+j].replace('&amp;', '&')
                headers = {'Referer': site}
                r2 = get(saman_link, verify=False, headers=headers)
                soup = BeautifulSoup(r2.content, "html.parser")

                email = None
                if 'Verify.aspx' in saman_link:
                    tbody = soup.find(id='subContent1')
                    trows = tbody.find_all('tr')
                    items = []
                    for tr in trows:
                        for td in tr.find_all('td'):
                            items.append(td.text)
                else:
                    items = soup.select("div.licontent")
                    items = [i.text for i in items]

                items = [" ".join(i.split()) for i in items]
                email = [i for i in items if '[at]' in i][0]
                email = email.replace('[at]', '@')
                print(email)
                emails.append(email)
                break

    except Exception as e:
        print(e)

print('\n'.join(emails), file=open('emails.txt', 'w+'))
