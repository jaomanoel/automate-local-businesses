import csv
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

filename = "google-clients.csv"
header = (
    "Search",
    "Emprise",
    "Name",
    "Office",
    "Site",
    "Address",
    "Phone",
    "Email",
    "Instagram",
    "LinkedIn"
)
data_clients = []
browser = webdriver.Firefox()
searchs = [
    "Saloni di bellezza a Parma, Italia",
    "parrucchierea a Parma, Italia",
    "Centro venessere a Parma, Italia",
    "Terme di Parma, Italia",
    "Clinica sanitaria a Parma, Italia",
    "Palestra fitness a Parma, Italia",
    "Studio di Yoga a Parma, Italia",
    "Nutrizionista a Parma, Italia",
    "Medico di medicina alternativa a Parma, Italia",
    "Massaggiatrice a Parma, Italia",
    "Negozio di produtti naturali a Parma, Italia",
    "Centro terapeutico a Parma, Italia"
]


def write(header, data, filename):
    with open(filename, "w", newline="") as file:
        clients = csv.writer(file)
        clients.writerow(header)
        for x in data:
            clients.writerow(x)


def get_search(search):
    browser.get("https://google.com")
    input = browser.find_element(By.CLASS_NAME, "gLFyf")
    input.clear()
    input.send_keys(search)
    sleep(1)
    input.send_keys(Keys.ENTER)
    sleep(5)

    try:
        more_businesses = browser.find_element(
            By.TAG_NAME, "g-more-link")
        more_businesses.click()

    except Exception as e:
        print(e)


def get_infos_bs4(search):
    sleep(3)

    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    sleep(2)

    try:
        businesses = soup.find_all(
            "div", attrs={"data-test-id": "organic-list-card"})

        for business in businesses:
            name_emprise = ""
            site = ""
            address = ""
            phone = ""

            try:
                name_emprise = business.find(
                    "div", attrs={"class": "I9iumb"}).get_text()
            except Exception:
                name_emprise = "Not Found"

            try:
                url = business.find(
                    "a", attrs={"aria-label": "Site"}).get("href")
                start_index = url.find("url=")
                end_index = url.find("&ved=")

                site = url[start_index+4:end_index]
            except Exception:
                site = "Not Found"

            try:
                address = business.find(
                    "a", attrs={"aria-label": "Rotas"}).get("href")
            except Exception:
                address = "Not Found"

            try:
                phone = business.find(
                    "a", attrs={"aria-label": "Ligar"}
                ).get("data-phone-number")
            except Exception:
                phone = "Not Found"

            instagram = "Not Found"
            if (site.find("instagram.com/") != -1):
                instagram = site

            sleep(3)

            data = (
                search,
                name_emprise,
                "Not Found",  # Name
                "Not Found",  # Office
                site,
                address,
                phone,
                "Not Found",  # Email
                instagram,
                "Not Found"  # LinkedIn
            )

            data_clients.append(data)
            print(data_clients)
    except Exception as e:
        raise e

    sleep(2)

    try:
        browser.find_element(
            By.CSS_SELECTOR, '[aria-label="Próxima"]'
        ).click()

        sleep(5)

        get_infos_bs4(search)
    except Exception:
        print("End")


def main():
    for search in searchs:
        get_search(search)
        sleep(2)
        get_infos_bs4(search)

    browser.quit()
    write(header, data_clients, filename)


main()
