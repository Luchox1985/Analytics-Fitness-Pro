import json
import shutil
import os
import csv
from datetime import datetime
from config import ARCHIVO_FITNESS, BACKUP_FITNESS, BASE_DIR

def gestionar_backup():
    if os.path.exists(ARCHIVO_FITNESS):
        shutil.copy(ARCHIVO_FITNESS, BACKUP_FITNESS)

def guardar_db(db):
    gestionar_backup()
    with open(ARCHIVO_FITNESS, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

def cargar_db():
    if os.path.exists(ARCHIVO_FITNESS):
        try:
            with open(ARCHIVO_FITNESS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def exportar_informe(usuario):
    fecha_hoy = datetime.now().strftime("%Y%m%d_%H%M")
    nombre_archivo = f"informe_{usuario['nombre'].replace(' ', '_')}_{fecha_hoy}.txt"
    ruta_completa = os.path.join(BASE_DIR, nombre_archivo)
    
    try:
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(f"REPORTE DE RENDIMIENTO ANALITICO\n")
            f.write(f"Usuario: {usuario['nombre'].upper()}\n")
            f.write(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write("-" * 50 + "\n")
            for e in usuario.get("entrenamientos", []):
                f.write(f"[{e['fecha']}] {e['ejercicio']}: {e['volumen']:.2f}kg | 1RM: {e.get('1rm_est'):.2f}kg\n")
        print(f"\nNOTIFICACION: Informe TXT creado exitosamente: {nombre_archivo}")
    except Exception as e:
        print(f"ERROR en generacion de informe TXT: {e}")

def exportar_csv(usuario):
    fecha_hoy = datetime.now().strftime("%Y%m%d")
    nombre_archivo = f"data_entrenamiento_{usuario['nombre'].replace(' ', '_')}_{fecha_hoy}.csv"
    ruta_completa = os.path.join(BASE_DIR, nombre_archivo)
    
    try:
        with open(ruta_completa, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Fecha", "Ejercicio", "Volumen_kg", "1RM_Estimado_kg"])
            for e in usuario.get("entrenamientos", []):
                escritor.writerow([e['fecha'], e['ejercicio'], e['volumen'], e.get('1rm_est', 0)])
        print(f"\nNOTIFICACION: Datos de entrenamiento exportados: {nombre_archivo}")
    except PermissionError:
        print(f"\nERROR: El archivo '{nombre_archivo}' esta abierto en Excel. Cierrelo y reintente.")
    except Exception as e:
        print(f"ERROR al exportar CSV: {e}")

def exportar_csv_antropometrico(usuario):
    fecha_hoy = datetime.now().strftime("%Y%m%d")
    nombre_archivo = f"evolucion_salud_{usuario['nombre'].replace(' ', '_')}_{fecha_hoy}.csv"
    ruta_completa = os.path.join(BASE_DIR, nombre_archivo)
    
    try:
        with open(ruta_completa, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Fecha", "Peso_kg", "Altura_m", "IMC", "Estatus"])
            
            altura = usuario["altura"]
            # Normalizacion por si acaso
            if altura > 3: altura /= 100

            for r in usuario.get("historial_peso", []):
                peso = r['peso']
                imc = round(peso / (altura ** 2), 2)
                
                estatus = "Normal"
                if imc < 18.5: estatus = "Bajo peso"
                elif imc >= 25 and imc < 30: estatus = "Sobrepeso"
                elif imc >= 30: estatus = "Obesidad"
                
                escritor.writerow([r['fecha'], f"{peso:.2f}", f"{altura:.2f}", f"{imc:.2f}", estatus])
        print(f"\nNOTIFICACION: Datos de evolucion de salud exportados: {nombre_archivo}")
    except PermissionError:
        print(f"\nERROR: Acceso denegado al archivo CSV. Verifique que no este abierto.")
    except Exception as e:
        print(f"ERROR en exportacion antropometrica: {e}")