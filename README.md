Filosofía del Proyecto
A diferencia de las aplicaciones convencionales, este sistema prioriza tres pilares fundamentales:

Privacidad por Diseño: Implementación de un protocolo de acceso local mediante PIN y preguntas de seguridad, asegurando que la información sensible permanezca bajo control del usuario.

Arquitectura Modular: El código está dividido funcionalmente para facilitar su mantenimiento. La lógica de la interfaz, el motor de base de datos y los cálculos matemáticos operan de forma independiente pero coordinada.

Orientación a Resultados: El sistema no solo registra; calcula tendencias como el 1RM estimado, el Índice de Masa Corporal (IMC) y genera informes técnicos listos para auditoría personal.

Componentes del Ecosistema
El software se distribuye en módulos especializados para garantizar una ejecución limpia:

Gestión de Flujo (main.py): Orquestador de la experiencia de usuario y validación de seguridad.

Motor de Persistencia (database.py): Responsable del ciclo de vida de los datos, incluyendo un sistema de copias de seguridad automáticas (backups) para prevenir la pérdida de registros históricos.

Núcleo de Cálculo (utils.py): Contiene la lógica matemática detrás de las métricas de salud y las visualizaciones de progresión en terminal.

Configuración Global (config.py): Centraliza las rutas de archivos y variables del sistema para una rápida adaptación a diferentes entornos.

Capacidades de Análisis
Monitoreo Antropométrico: Análisis de peso y estatura con normalización de unidades y diagnóstico de rangos saludables.

Seguimiento de Cargas: Registro de volumen de entrenamiento y estimación de fuerza máxima.

Exportación Profesional: Capacidad de generar archivos CSV y TXT estructurados, permitiendo que el usuario sea el dueño de su información y pueda procesarla en herramientas externas.

Notas de Implementación
Lenguaje: Python 3.x

Dependencias: Librerías estándar (sin necesidad de instalaciones externas complejas).

Seguridad: Incluye un archivo .gitignore configurado para evitar la exposición accidental de datos personales en repositorios públicos.
