# import libraries
from socket import timeout
from requests_html import HTMLSession

session = HTMLSession()

url = 'https://www.skysports.com/premier-league-table/2021'
response = session.get(url)
page_html = response.html

page_html.render(timeout = 1000)

leauge_table  = page_html.find('tbody')

for team in leauge_table:
    rows = team.find('tr')
    for row in rows:
        PL_team = row.find('.standing-table__cell--name')[0].text.strip()
        PL_points = row.find('.standing-table__cell')[9].text.strip()
        print(PL_team , ' : ' , PL_points)


