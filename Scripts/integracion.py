import pandas as pd
import json
import os

EXCEL_FILE = "data/raw/Cli.xlsx"
DATOS_M = "data/intermediate/DatosM.json"
DATA_FINAL = "data/intermediate/DataFinal.json"
NO_INTEGRADO = "data/intermediate/No_Integrado.json"

COLUMNS = [
    "Name",
    "Estatus Cliente",
    "Sucursal",
    "Equipos",
    "No. Serie",
    "Tóner",
    "KFS",
    "Contrato",
    "LOCAL O FORANEO",
    "Stock Autorizado",
    "Original o compatible"
]

def excel_to_json():
    df = pd.read_excel(EXCEL_FILE, dtype=str, header=2)

    df.columns = df.columns.str.strip()

    missing = [col for col in COLUMNS if col not in df.columns]
    if missing:
        print(f"Advertencia: faltaban columnas {missing}. Se llenarán con valores vacíos.")
        for col in missing:
            df[col] = None

    df = df[[col for col in COLUMNS]]

    df = df.where(pd.notnull(df), None)

    data = []
    for _, row in df.iterrows():
        record = {
            "ID_Excel": row["Name"],
            "Serie": row["No. Serie"],
            "Estatus": row["Estatus Cliente"],
            "Sucursal": row["Sucursal"],
            "Equipos": row["Equipos"],
            "KFS": row["KFS"],
            "Contrato": row["Contrato"],
            "Ubicacion": row["LOCAL O FORANEO"],
            "Stock Autorizado": row["Stock Autorizado"],
            "Modelo Toner": row["Tóner"],
            "Tipo": row["Original o compatible"]
        }
        data.append(record)

    with open(DATOS_M, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data


def integrar_datos(datos_excel):
    try:
        if os.path.exists(DATA_FINAL) and os.path.getsize(DATA_FINAL) > 0:
            with open(DATA_FINAL, "r", encoding="utf-8") as f:
                data_final = json.load(f)
        else:
            data_final = []
    except json.JSONDecodeError:
        print("Advertencia: DataFinal.json corrupto, se reinicia vacío.")
        data_final = []

    no_integrados = []

    final_dict = {item["Serie"]: item for item in data_final if item.get("Serie")}

    integrados_count = 0
    no_integrados_count = 0

    for record in datos_excel:
        serie = record["Serie"]

        if not serie:
            no_integrados.append(record)
            no_integrados_count += 1
        elif serie in final_dict:
            final_dict[serie].update(record)
            integrados_count += 1
        else:
            no_integrados.append(record)
            no_integrados_count += 1

    data_final = list(final_dict.values())

    with open(DATA_FINAL, "w", encoding="utf-8") as f:
        json.dump(data_final, f, indent=4, ensure_ascii=False)

    if no_integrados:
        with open(NO_INTEGRADO, "w", encoding="utf-8") as f:
            json.dump(no_integrados, f, indent=4, ensure_ascii=False)

    print(f"Integración completada.")
    print(f"   Registros integrados: {integrados_count}")
    print(f"   Registros no integrados: {no_integrados_count}")


def main():
    datos_excel = excel_to_json()
    integrar_datos(datos_excel)


if __name__ == "__main__":
    main()
