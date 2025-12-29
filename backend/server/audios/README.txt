Carpeta para almacenar los archivos de audio (.wav) asociados a las llamadas. Los archivos deben tener nombres como PIN_FECHA_T_HH-MM-SS.wav para que el backend pueda encontrarlos y servirlos correctamente.

Ejemplo de nombre: 123_2025-04-29_T20-00-00.wav

Asegúrate de que FastAPI exponga esta carpeta como archivos estáticos en /audios/ para que el frontend pueda accederlos por URL.
