import requests
from bs4 import BeautifulSoup


def in_regions(reg):
    page = requests.get("https://coronavirusstat.ru")
    soup = BeautifulSoup(page.text, "html.parser")
    data_sost = soup.find("h6", {"class": "text-muted"}).find("strong")
    in_region = soup.find_all("div", {"class": "row border border-bottom-0 c_search_row"})
    ans = "По состоянию на " + data_sost.text + ":\n"
    path = soup
    for x in in_region:
        name = x.find("a")
        if reg.lower() in name.text.lower():
            path = x
            break

    ans += "Регион: " + x.find("a").text + "\n"
    path = path.find("div", {"class": "p-1 col-7 row m-0"}).find("div", {"class": "p-1 col-4 col-sm-2"})
    s = path.text.split()
    ans += s[0] + ": " + s[1] + "\n"
    path = path.find_next_sibling()
    s = path.text.split()
    ans += s[0] + ": " + s[1] + "\n"
    path = path.find_next_sibling()
    s = path.text.split()
    ans += s[0] + ": " + s[1] + "\n"
    path = path.find_next_sibling()
    s = path.text.split()
    ans += s[0] + ": " + s[1] + "\n"
    return ans

print(in_regions('москва'))