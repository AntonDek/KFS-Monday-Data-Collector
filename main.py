import subprocess
import os
import sys
from datetime import datetime

SCRIPTS_DIR = "Scripts"

PIPELINE = [
    "GetListSerial.py",
    "GetDataMachine.py",
    "DataFilter.py",
    "RefineryResiduals.py",
    "DataRefineryFilter.py",
    "integracion.py"
]

def run_script(script):
    script_path = os.path.join(SCRIPTS_DIR, script)

    if not os.path.exists(script_path):
        print(f"\nERROR: No se encontró el script {script_path}")
        return False

    print(f"\nEjecutando: {script}")
    print(f"   Ruta: {script_path}")


    result = subprocess.run([sys.executable, script_path])

    if result.returncode != 0:
        print(f"\nERROR: Falló la ejecución de {script}. Código: {result.returncode}")
        return False
    
    print(f"Finalizado correctamente: {script}")
    return True


def main():
    start = datetime.now()
    print("===========================================")
    print("   EJECUCIÓN DEL PIPELINE INICIADA")
    print(f"   {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print("===========================================\n")

    for script in PIPELINE:
        success = run_script(script)
        if not success:
            print("\nPipeline detenido por error.\n")
            end = datetime.now()
            print(f"Duración total: {end - start}")
            return

    print("\n===========================================")
    print("PIPELINE COMPLETADO EXITOSAMENTE")
    print("===========================================")
    end = datetime.now()
    print(f"Duración total: {end - start}")


if __name__ == "__main__":
    main()
