# KFS–Monday Data Collector

Herramienta automatizada para recolectar, clasificar y unificar información de impresoras obtenida desde **Kyocera Fleet Services (KFS)** y datos internos provenientes del archivo **Cli** (exportado desde **Monday**).  
El proyecto genera archivos organizados por niveles de tóner, urgencia y estado operativo de cada equipo.

---

## Flujo del Sistema

1. **GetListSerial.py**  
   Obtiene todas las series disponibles en KFS y genera `serial.csv`.

2. **GetDataMachine.py**  
   Descarga niveles de tóner, modelo, empresa y última conexión de cada impresora, generando `DataFinal.json`.

3. **DataFilter.py**  
   Clasifica las impresoras según niveles de tóner, días restantes y empresa. Produce:  
   - `Taller.json`  
   - `Atencion.json`  
   - `NoKFS.json`  
   - `Toner_Estable.json`  
   - `Toner_MaximaPrioridad.json`  
   - `SinFiltro.json`

4. **RefineryResiduals.py**  
   Recolecta nuevamente los datos que no pudieron filtrarse por falta de información.

5. **DataRefineryFilter.py**  
   Aplica un segundo filtrado a los datos refinados, generando las mismas categorías anteriores.

6. **integracion.py**  
   Integra los datos procesados con la información del archivo **Cli** (derivado de Monday), completando el dataset final.

---

## 📁 Archivos principales generados

- **Taller.json** — Equipos en bodega o mantenimiento.  
- **Toner_MaximaPrioridad.json** — Equipos con tóner crítico o modelos especiales.  
- **Atencion.json** — Equipos con niveles bajos pero no urgentes.  
- **Toner_Estable.json** — Equipos sin riesgos inmediatos.  
- **NoKFS.json** — Equipos sin datos disponibles en KFS.  
- **SinFiltro.json** — Registros sin categoría asignada.

---

## 🧩 Script Maestro

El repositorio incluye un script que ejecuta toda la secuencia en orden y detiene el proceso ante cualquier error, asegurando que cada fase se complete correctamente antes de continuar.

---

## Estado del Proyecto

Este repositorio corresponde a una **versión reconstruida** del proyecto original.  

La implementación con contenedores no se completó y podrían existir detalles pendientes, pero el flujo principal está documentado y listo para revisión o mejora.

Además, los datos reales utilizados por la empresa se han reemplazado por valores ficticios o genéricos para evitar la exposición de información confidencial. Las estructuras se mantienen, pero ningún dato corresponde a sistemas, equipos o clientes reales.
