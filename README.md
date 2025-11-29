# KyoceraFleetServices–Monday Data Collector

Automated tool for collecting, classifying, and merging printer information obtained from **Kyocera Fleet Services (KFS)** and internal data from the **Cli** file (exported from **Monday**).  
The project generates structured files categorized by toner levels, urgency, and operational status of each device.

---

## System Workflow

1. **GetListSerial.py**  
   Retrieves all available serial numbers from KFS and generates `serial.csv`.

2. **GetDataMachine.py**  
   Downloads toner levels, model, company, and last connection timestamp for each device, producing `DataFinal.json`.

3. **DataFilter.py**  
   Classifies devices based on toner levels, remaining days, and assigned company. Outputs:  
   - `Taller.json`  
   - `Atencion.json`  
   - `NoKFS.json`  
   - `Toner_Estable.json`  
   - `Toner_MaximaPrioridad.json`  
   - `SinFiltro.json`

4. **RefineryResiduals.py**  
   Re-processes devices that could not be filtered due to missing information and retrieves updated data.

5. **DataRefineryFilter.py**  
   Applies a second filtering stage using the newly gathered data, generating the same categories as before.

6. **integracion.py**  
   Integrates processed KFS data with the internal **Cli** file (Monday export) to complete the final dataset.

---

## Generated Output Files

- **Taller.json** — Devices in warehouse or under maintenance.  
- **Toner_MaximaPrioridad.json** — Devices with critical toner levels or special models.  
- **Atencion.json** — Devices with low toner but not urgent.  
- **Toner_Estable.json** — Devices operating without immediate risks.  
- **NoKFS.json** — Devices without available data in KFS.  
- **SinFiltro.json** — Records that did not match any category.

---

## Master Script

The repository includes a master script that runs the entire sequence in order and stops execution if any step fails, ensuring each stage completes successfully before moving to the next.

---

## Project Status

This repository is a **reconstructed version** of the original project.  

Containerization using Docker was started but not completed, so minor adjustments may still be needed.  
However, the full workflow remains documented and functional for review or further improvement.

All real company data has been replaced with fictitious or generic values to avoid the exposure of confidential information.  
Data structures are preserved, but no file contains information tied to real systems, customers, or devices.
