import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_FITNESS = os.path.join(BASE_DIR, "db_fitness_pro_v3.json")
BACKUP_FITNESS = os.path.join(BASE_DIR, "db_backup.json")

EJERCICIOS_BASE = {
    "Pecho": ["Press de Banca", "Aperturas con Mancuernas", "Fondos", "Press Inclinado", "Cruces de Polea", "Flexiones", "Press con Maquina"],
    "Espalda": ["Dominadas", "Remo con Barra", "Jalon al Pecho", "Remo en Polea Baja", "Pull-over con Polea", "Peso Muerto", "Remo Kroc"],
    "Pierna": ["Sentadilla Libre", "Prensa", "Peso Muerto Rumano", "Zancadas", "Extension de Cuadriceps", "Curl Femoral", "Elevacion de Gemelos"],
    "Hombro": ["Press Militar", "Elevaciones Laterales", "Facepull", "Press Arnold", "Pajaros (Posterior)", "Elevaciones Frontales", "Remo al Mentón"],
    "Brazos": ["Curl de Biceps", "Press Frances", "Extensiones de Triceps", "Martillo", "Copa de Triceps", "Curl en Banco Scott", "Dips entre Bancos"]
}