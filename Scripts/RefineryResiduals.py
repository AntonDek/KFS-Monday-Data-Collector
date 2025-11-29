import csv
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

def kronos(segundos):
    minutos, segs = divmod(segundos, 60)
    horas, minutos = divmod(minutos, 60)
    return f"{int(horas):02d}:{int(minutos):02d}:{int(segs):02d}"

def ultima_conexion(driver, serial_ID):
    url_detail = f"https://fs-us.kyocera.biz/XXXXXXX/XXXXXXX/{serial_ID}"
    driver.get(url_detail)

    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td.w-large ul.list li span:last-child"))
        )
    except:
        print(f"No se pudo cargar la última conexión para {serial_ID}")
        return None

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    li = soup.select_one("td.w-large ul.list li span:last-child")
    if li:
        fecha = li.text.strip().replace(": ", "")
        return fecha
    return None

def galgo(soup, tag, attr, patron=None, atributo_texto=True):
    for elemento in soup.find_all(tag, attrs={attr: True}):
        if patron is None or patron in elemento.get(attr, ""):
            return elemento.text.strip() if atributo_texto else elemento[attr]
    return None

def obtener_empresa(soup):
    return galgo(soup, tag="a", attr="href", patron="/Device/Index/")

def obtener_modelo(soup):
    a = galgo(soup, tag="div", attr="class", patron="pt5")
    if a:
        partes = a.split()
        return partes[1] if len(partes) > 1 else partes[0]
    return None

def datos_toner(driver):
    toner = {}

    try:
        boton_pedido = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, "btn-action-order-toner"))
        )
        boton_pedido.click()
    except:
        print("No se pudo hacer click en el botón Pedido")
        return None

    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "toner-order-wizard-1"))
        )
    except:
        print("El modal de pedido no se cargó")
        return None

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    first_row = soup.select_one("#selected-toners-list tbody tr")
    if not first_row:
        print("No se encontraron toners")
        return None

    modelo = first_row.find("td", class_="ellipsis").text.strip()
    serie = first_row.find_all("td", class_="ellipsis")[1].text.strip()

    for row in soup.select("#selected-toners-list tbody tr"):
        color = row.find("div", class_="tonar-color").text.strip()
        porcentaje_text = row.find("div", class_="tonar-percentage").text.strip()
        try:
            porcentaje = int(porcentaje_text.replace("%",""))
        except:
            porcentaje = None

        dias_restantes_text = row.find_all("td")[4].text.strip()
        try:
            dias_restantes = int(dias_restantes_text)
        except:
            dias_restantes = None

        toner[color] = {
            "porcentaje": porcentaje,
            "dias_restantes": dias_restantes
        }

    return {
        "Serie_ID": f"PD_{serie}",
        "Serie": serie,
        "Modelo": modelo,
        "Toner": toner
    }

def recoleccion(driver, serial_ID):
    url = f"https://fs-us.kyocera.biz/XXXXXXX/{serial_ID}/XXXXXXX"
    driver.get(url)

    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#toner-list"))
        )
    except:
        print(f"Advertencia: No se cargó correctamente la serie {serial_ID}")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    empresa = obtener_empresa(soup)

    toner_info = datos_toner(driver)
    if not toner_info:
        print(f"No se pudo extraer info de toner para {serial_ID}")
        return {
            "url": url,
            "Empresa": empresa,
            "Modelo": None,
            "Serie_ID": serial_ID,
            "Serie": None,
            "Toner": None
        }

    ult_conexion = ultima_conexion(driver, serial_ID)

    return {
        "url": url,
        "Empresa": empresa,
        "Modelo": toner_info["Modelo"],
        "Serie_ID": serial_ID,
        "Serie": toner_info["Serie"],
        "Toner": toner_info["Toner"],
        "Ultima_conexion": ult_conexion
    }


def autenticacion():
    try:
        options = Options()
        # pyrefly: ignore  # missing-attribute
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

        if "Login" in driver.title or "Sign In" in driver.title:
            print("Error: sesión no válida")
            driver.quit()
            return None

        print("Autenticación correcta")
        return driver

    except Exception as e:
        print(f"Error en autenticación: {e}")
        return None


def main():
    krono_total = time.time()

    serial_list = []
    with open("data/filter/SinFiltro.json", "r", encoding="utf-8") as f:
        reader = json.load(f)
        for row in reader:
            if row and "Serie_ID" in row:
                serial_list.append(row["Serie_ID"].strip())

    print(f" Se cargaron {len(serial_list)} series desde SinFiltro.json")

    driver = autenticacion()
    if not driver:
        print("No se pudo autenticar, deteniendo ejecución")
        return

    impresoras = []
    
    for idx, serie in enumerate(serial_list, 1):
        krono_serial_ID = time.time()

        try:
            impresora_info = recoleccion(driver, serie)
            impresoras.append(impresora_info)
            print(f"[{idx}/{len(serial_list)}] Serie {serie} recolectada")
        except Exception as e:
            print(f"Error con la serie {serie}: {e}")

    driver.quit()

    with open("data/intermediate/DataRefineryFinal.json", "w", encoding="utf-8") as f:
        json.dump(impresoras, f, indent=4, ensure_ascii=False)

    fin_total = time.time()
    tiempo_total = fin_total - krono_total
    print(f"Se recolectaron {len(impresoras)} impresoras y se guardaron en DataFinal.json")
    print(f"Tiempo total de ejecución: {kronos(tiempo_total)}\n")


if __name__ == "__main__":
    main()
