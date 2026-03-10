import os
from datetime import datetime

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def calcular_1rm(peso, reps):
    if reps == 1: return peso
    return round(peso / (1.0278 - (0.0278 * reps)), 2)

def generar_grafica(historial_ejercicio):
    if not historial_ejercicio: return
    print("\nTENDENCIA DE VOLUMEN (Ultimas 5 sesiones):")
    ultimos = historial_ejercicio[-5:]
    max_vol = max(e["volumen"] for e in ultimos)
    for e in ultimos:
        barra_longitud = int((e["volumen"] / max_vol) * 20) if max_vol > 0 else 0
        barra = "X" * barra_longitud # Cambiado por 'X' para mayor sobriedad
        print(f"{e['fecha']} | {barra} {e['volumen']:.2f} kg")

def mostrar_evolucion_imc(usuario):
    if "peso" not in usuario or "altura" not in usuario:
        print("\nERROR: Datos insuficientes en el perfil de usuario.")
        return

    altura = usuario["altura"]
    if altura > 3:
        altura = altura / 100

    peso_actual = usuario["peso"]
    imc_actual = round(peso_actual / (altura ** 2), 2)

    estatus = "Normal"
    if imc_actual < 18.5: estatus = "Bajo peso"
    elif imc_actual >= 25 and imc_actual < 30: estatus = "Sobrepeso"
    elif imc_actual >= 30: estatus = "Obesidad"

    peso_min = round(18.5 * (altura ** 2), 2)
    peso_max = round(24.9 * (altura ** 2), 2)

    print(f"\n" + "="*45)
    print(f"   ANALISIS ANTROPOMETRICO")
    print(f"="*45)
    print(f"IMC Actual:     {imc_actual:.2f} ({estatus})")
    print(f"Peso Actual:    {peso_actual:.2f} kg")
    print(f"Estatura:       {altura:.2f} m")
    print(f"-"*45)
    print(f"RANGO SALUDABLE ESTIMADO:")
    print(f"Peso minimo:    {peso_min:.2f} kg")
    print(f"Peso maximo:    {peso_max:.2f} kg")
    print(f"="*45)
    
    if "historial_peso" in usuario and len(usuario["historial_peso"]) > 0:
        print("\nHISTORIAL DE PROGRESION:")
        print(f"{'Fecha':<12} | {'Peso':<10} | {'IMC':<6}")
        print("-" * 35)
        
        for registro in usuario["historial_peso"]:
            p = registro["peso"]
            i = round(p / (altura ** 2), 2)
            print(f"{registro['fecha']:<12} | {p:<7.2f} kg | {i:<6.2f}")