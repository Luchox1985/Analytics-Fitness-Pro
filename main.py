from datetime import datetime
from config import EJERCICIOS_BASE
from utils import limpiar_pantalla, calcular_1rm, generar_grafica, mostrar_evolucion_imc
from database import (cargar_db, guardar_db, exportar_informe, 
                      exportar_csv, exportar_csv_antropometrico)

# =======================================================
# 1. PROTOCOLOS DE SEGURIDAD Y VALIDACION
# =======================================================

def validar_pin():
    while True:
        pin = input("Defina su PIN de seguridad (4 digitos): ")
        if pin.isdigit() and len(pin) == 4:
            return pin
        print("ERROR: El PIN debe contener exactamente 4 numeros.")

def recuperar_acceso(db):
    limpiar_pantalla()
    print("=== RECUPERACION DE ACCESO ===")
    uid = input("Ingrese su ID: ")
    if uid in db:
        usuario = db[uid]
        if "respuesta" not in usuario:
            print("AVISO: Este perfil no tiene configurada la recuperacion.")
            input(); return
        
        print(f"\nPregunta de seguridad: {usuario['pregunta']}")
        intento = input("Tu respuesta: ").strip().lower()
        
        if intento == usuario["respuesta"].lower():
            print("\nIDENTIDAD CONFIRMADA.")
            usuario["pin"] = validar_pin()
            guardar_db(db)
            print("CONFIRMACION: PIN actualizado con exito.")
        else:
            print("ERROR: Respuesta incorrecta.")
    else:
        print("ERROR: ID no encontrado.")
    input("\nPresione Enter para continuar...")

# =======================================================
# 2. FUNCIONES DE OPERACION (CRUD Y REGISTROS)
# =======================================================

def registrar_entrenamiento(usuario, db):
    limpiar_pantalla()
    print(f"REGISTRO DE SESION: {usuario['nombre'].upper()}")
    grupos = list(EJERCICIOS_BASE.keys())
    for i, g in enumerate(grupos, 1): print(f"{i}. {g}")
    
    try:
        g_idx = int(input("\nSeleccione Grupo Muscular: ")) - 1
        ejs = EJERCICIOS_BASE[grupos[g_idx]]
        for i, e in enumerate(ejs, 1): print(f"{i}. {e}")
        
        e_idx = int(input("\nSeleccione Ejercicio: ")) - 1
        nombre_ej = ejs[e_idx]
        
        series = int(input("Series: "))
        reps = int(input("Repeticiones: "))
        peso = float(input("Peso (kg): "))
        
        vol_actual = series * reps * peso
        un_rm = calcular_1rm(peso, reps)
        
        usuario["entrenamientos"].append({
            "fecha": datetime.now().strftime("%d/%m"),
            "ejercicio": nombre_ej,
            "volumen": vol_actual,
            "1rm_est": un_rm
        })
        
        historial_ej = [e for e in usuario["entrenamientos"] if e["ejercicio"] == nombre_ej]
        generar_grafica(historial_ej)
        guardar_db(db)
        print(f"\nFuerza Maxima (1RM): {un_rm:.2f} kg. Registro guardado.")
    except Exception as e:
        print(f"ERROR: {e}")

def actualizar_estatus_fisico(usuario, db):
    limpiar_pantalla()
    print(f"ACTUALIZAR DATOS ANTROPOMETRICOS: {usuario['nombre'].upper()}")
    try:
        nuevo_peso = float(input("Ingrese su peso actual (kg): "))
        fecha = datetime.now().strftime("%d/%m/%Y")
        
        if "historial_peso" not in usuario:
            usuario["historial_peso"] = []
            
        usuario["historial_peso"].append({"fecha": fecha, "peso": nuevo_peso})
        usuario["peso"] = nuevo_peso 
        guardar_db(db)
        print(f"\nEXITO: Peso actualizado a {nuevo_peso:.2f} kg.")
    except ValueError:
        print("ERROR: Ingrese un valor numerico valido.")

def borrar_perfil(db, uid):
    usuario = db[uid]
    limpiar_pantalla()
    print(f"ADVERTENCIA: Esta a punto de eliminar el perfil de {usuario['nombre'].upper()}")
    confirmar = input("\nConfirmacion (escriba 'ELIMINAR' para continuar): ")
    
    if confirmar.upper() == "ELIMINAR":
        pin_verif = input("Ingrese su PIN para confirmar: ")
        if pin_verif == usuario["pin"]:
            del db[uid]
            guardar_db(db)
            print("\nNOTIFICACION: Perfil eliminado correctamente.")
            return True
        else:
            print("ERROR: PIN incorrecto. Operacion cancelada.")
    return False

# =======================================================
# 3. LOGICA DE INTERFAZ Y DASHBOARD
# =======================================================

def menu_usuario(db, uid):
    while True:
        db = cargar_db()
        if uid not in db: break 
        usuario = db[uid]
        
        limpiar_pantalla()
        print(f"==================================================")
        print(f"   PANEL DE CONTROL: {usuario['nombre'].upper()}")
        print(f"==================================================")
        
        if "historial_peso" in usuario and len(usuario["historial_peso"]) > 0:
            peso_inicial = usuario["historial_peso"][0]["peso"]
            peso_actual = usuario["peso"]
            diferencia = peso_actual - peso_inicial
            # Formato de tendencia formal
            tendencia = f"(+{diferencia:.2f} kg)" if diferencia > 0 else f"({diferencia:.2f} kg)"
            
            ultimo_ej = "N/A"
            if usuario["entrenamientos"]:
                ultimo_ej = f"{usuario['entrenamientos'][-1]['ejercicio']} [{usuario['entrenamientos'][-1]['fecha']}]"

            print(f"RESUMEN EJECUTIVO:")
            print(f"   - Peso Inicial: {peso_inicial:.2f} kg")
            print(f"   - Peso Actual:  {peso_actual:.2f} kg")
            print(f"   - Variacion:    {tendencia}")
            print(f"   - Ultima Actividad: {ultimo_ej}")
        else:
            print(f"ESTATUS: Sin datos historicos registrados.")
        
        print(f"--------------------------------------------------")
        print("1. Registrar Entrenamiento")
        print("2. Ver Grafica de Volumen")
        print("3. Salud y Evolucion IMC")
        print("4. Exportacion de Informes")
        print("5. Configuracion de Perfil")
        print("6. Finalizar Sesion")
        
        opc = input("\nSeleccione opcion: ")
        
        if opc == "1":
            registrar_entrenamiento(usuario, db)
            input("\nPresione Enter...")
        elif opc == "2":
            limpiar_pantalla()
            if usuario["entrenamientos"]:
                ultimo = usuario["entrenamientos"][-1]["ejercicio"]
                hist = [e for e in usuario["entrenamientos"] if e["ejercicio"] == ultimo]
                print(f"Analisis de tendencia: {ultimo}")
                generar_grafica(hist)
            else: print("AVISO: Sin registros suficientes."); 
            input("\nPresione Enter...")
        elif opc == "3":
            limpiar_pantalla()
            print(f"MODULO DE SALUD - {usuario['nombre'].upper()}")
            print("1. Registrar peso")
            print("2. Ver Analisis IMC")
            print("3. Exportar CSV Antropometrico")
            sub = input("\nOpcion: ")
            if sub == "1": actualizar_estatus_fisico(usuario, db)
            elif sub == "2": mostrar_evolucion_imc(usuario)
            elif sub == "3": exportar_csv_antropometrico(usuario)
            input("\nPresione Enter...")
        elif opc == "4":
            print("1. Informe TXT | 2. Datos Entrenamiento CSV")
            sub = input("\nOpcion: ")
            if sub == "1": exportar_informe(usuario)
            elif sub == "2": exportar_csv(usuario)
            input("\nPresione Enter...")
        elif opc == "5":
            if borrar_perfil(db, uid): break
            input("\nPresione Enter...")
        elif opc == "6": break

def main():
    while True:
        limpiar_pantalla()
        db = cargar_db()
        print("=" * 50)
        print("   ANALYTICS FITNESS PRO - VERSION 3.9")
        print("=" * 50)
        print("1. Acceso mediante ID")
        print("2. Registro de Nuevo Perfil")
        print("3. Recuperar PIN de Seguridad")
        print("4. Directorio de Usuarios")
        print("5. Salir del Sistema")
        
        opc = input("\nSeleccione: ")
        if opc == "1":
            uid = input("ID de Usuario: ")
            if uid in db:
                usuario = db[uid]
                acceso = input(f"PIN para {usuario['nombre']}: ")
                if acceso == usuario["pin"]: menu_usuario(db, uid)
                else: print("ERROR: PIN Incorrecto."); input()
            else: print("ERROR: ID no encontrado."); input()
        elif opc == "2":
            try:
                nom = input("Nombre completo: ")
                pin = validar_pin()
                pregunta = input("Pregunta de seguridad: ")
                respuesta = input("Respuesta secreta: ").strip().lower()
                peso_ini = float(input("Peso (kg): "))
                alt_raw = float(input("Altura (m): "))
                if alt_raw > 3: alt_raw /= 100
                
                nid = str(len(db) + 101)
                db[nid] = {
                    "nombre": nom, "pin": pin, "pregunta": pregunta, "respuesta": respuesta,
                    "peso": peso_ini, "altura": alt_raw, "entrenamientos": [], 
                    "historial_peso": [{"fecha": datetime.now().strftime("%d/%m/%Y"), "peso": peso_ini}]
                }
                guardar_db(db)
                print(f"CONFIRMACION: Perfil ID {nid} creado exitosamente."); input()
            except ValueError: print("ERROR: Formato de datos invalido."); input()
        elif opc == "3": recuperar_acceso(db)
        elif opc == "4":
            print("\nDIRECTORIO DE ATLETAS REGISTRADOS:")
            for k, v in db.items(): print(f"ID: {k} | {v['nombre']}")
            input("\nPresione Enter...")
        elif opc == "5": break

if __name__ == "__main__":
    main()