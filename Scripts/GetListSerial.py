from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

inicio = time.perf_counter()

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

driver.get("https://fs-us.kyocera.biz/XXXXXXX/XXXXXXX/XXXXXXX")

cookies = {
    ".AspNetCore.Identity.Application": "Cookie",
    "Identity.TwoFactorRememberMe": "Cookie"
}
for name, value in cookies.items():
    driver.add_cookie({"name": name, "value": value, "domain": "fs-us.kyocera.biz", "path": "/"})

driver.get("https://fs-us.kyocera.biz/XXXXXXX/XXXXXXX/XXXXXXX")

all_series = []

while True:
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    page_series = []
    for a_tag in soup.find_all("a", href=True):
        if "/Device/Detail/" in a_tag['href']:
            serial = a_tag['href'].split("/Device/Detail/")[-1]
            all_series.append(serial)
    all_series.extend(page_series)

    try:
        a_next = driver.find_element(By.CSS_SELECTOR, "li.next a")
        li_next = driver.find_element(By.CSS_SELECTOR, "li.next")
        # pyrefly: ignore  # unsupported-operation
        if "disabled" in li_next.get_attribute("class"):
            break 
        driver.execute_script("arguments[0].click();", a_next)
    except:
        break


#print(all_series)

with open("data/raw/series.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for serie in all_series:
        writer.writerow([serie])

with open("data/raw/series.csv", "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row[0])

print(f"Total de series extraídas: {len(all_series)}")


driver.quit()

fin = time.perf_counter()
duracion = fin - inicio
print(f"Tiempo total de ejecución: {duracion:.2f} segundos")
