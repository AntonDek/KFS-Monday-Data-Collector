import json
import time

INPUT_FILE = "data/intermediate/DataFinal.json"

OUTPUT_FILES = {
    "data/filter/Taller.json": [],
    "data/filter/Toner_MaximaPrioridad.json": [],
    "data/filter/Atencion.json": [],
    "data/filter/Toner_Estable.json": [],
    "data/filter/SinFiltro.json": [],
    "data/filter/NoKFS.json": []
}

MODELOS_ESPECIALES = {"M2040dn", "M5526cdw", "M6230cidn"}
EMPRESAS_NOKFS = {"Caja De Ahorros", "Arizlu", "Sesajal", "Budowa", "BIOZOO", "De la rosa"}


def clasificar_equipo(equipo):
    empresa = equipo.get("Empresa")
    modelo = equipo.get("Modelo")
    toner_data = equipo.get("Toner", {})

    if not empresa or not modelo:
        OUTPUT_FILES["data/filter/SinFiltro.json"].append(equipo)
        return

    if any(nombre in empresa for nombre in EMPRESAS_NOKFS):
        OUTPUT_FILES["data/filter/NoKFS.json"].append(equipo)
        return

    if empresa == "Taller Copymart GDL":
        OUTPUT_FILES["data/filter/Taller.json"].append(equipo)
        return

    try:
        porcentajes = []
        dias = []

        for v in toner_data.values():
            p = v.get("porcentaje") if v.get("porcentaje") is not None else None
            d = v.get("dias_restantes") if v.get("dias_restantes") is not None else None

            if p is not None:
                porcentajes.append(p)
            if d is not None:
                dias.append(d)

        if not porcentajes and not dias:
            OUTPUT_FILES["data/filter/SinFiltro.json"].append(equipo)
            return

    except Exception:
        OUTPUT_FILES["data/filter/SinFiltro.json"].append(equipo)
        return

    if any(p <= 15 or d <= 15 for p, d in zip(porcentajes, dias)):
        OUTPUT_FILES["data/filter/Toner_MaximaPrioridad.json"].append(equipo)
        return

    if modelo in MODELOS_ESPECIALES:
        if any(p <= 50 or d <= 30 for p, d in zip(porcentajes, dias)):
            OUTPUT_FILES["data/filter/Toner_MaximaPrioridad.json"].append(equipo)
        else:
            OUTPUT_FILES["data/filter/Toner_Estable.json"].append(equipo)
        return

    if any(p <= 30 or d <= 25 for p, d in zip(porcentajes, dias)):
        OUTPUT_FILES["data/filter/Atencion.json"].append(equipo)
        return

    OUTPUT_FILES["data/filter/Toner_Estable.json"].append(equipo)


def main():
    inicio = time.perf_counter()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        equipos = json.load(f)

    for equipo in equipos:
        clasificar_equipo(equipo)

    for filename, lista in OUTPUT_FILES.items():
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)

    print("\nResumen de clasificación:")
    for filename, lista in OUTPUT_FILES.items():
        print(f"- {filename}: {len(lista)} equipos")

    print(sum(len(lista) for lista in OUTPUT_FILES.values()))
    fin = time.perf_counter()
    duracion = fin - inicio
    print(f"Tiempo total de ejecución: {duracion:.2f} segundos")


if __name__ == "__main__":
    main()
