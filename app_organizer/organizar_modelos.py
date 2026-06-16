import os
import shutil
import glob
import time

def organizar_modelo():
    # Detectar la ruta exacta donde está guardado este script (.py)
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    carpeta_objetivo = os.path.join(ruta_script, "modelo")
    
    print(f"Buscando carpeta de trabajo en: {carpeta_objetivo}")
    
    if not os.path.exists(carpeta_objetivo):
        print(f"La carpeta '{carpeta_objetivo}' no existe. Creando una nueva carpeta vacía.")
        os.makedirs(carpeta_objetivo)
        return

    # 1. Buscar archivos comprimidos
    extensiones_comprimidos = ["*.zip", "*.rar", "*.7z", "*.tar.xz"]
    archivos_comprimidos = []
    for ext in extensiones_comprimidos:
        archivos_comprimidos.extend(glob.glob(os.path.join(carpeta_objetivo, ext)))
        archivos_comprimidos.extend(glob.glob(os.path.join(carpeta_objetivo, ext.upper())))
    
    if not archivos_comprimidos:
        print("❌ Error: No se encontró ningún archivo comprimido dentro de la carpeta 'modelo'.")
        return
    
    # Obtener el nombre base del archivo comprimido
    nombre_comp = os.path.basename(archivos_comprimidos[0])
    nombre_base, _ = os.path.splitext(nombre_comp)
    if nombre_base.endswith('.tar'):
        nombre_base = nombre_base[:-4]

    print(f"▶️ Procesando el modelo basado en el archivo: {nombre_comp}")

    # 2. Buscar todas las fotos en la carpeta
    extensiones_fotos = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
    fotos_originales = []
    for ext in extensiones_fotos:
        fotos_originales.extend(glob.glob(os.path.join(carpeta_objetivo, ext)))
        fotos_originales.extend(glob.glob(os.path.join(carpeta_objetivo, ext.upper())))
    
    # Ordenar de forma estricta las rutas absolutas originales
    fotos_originales = sorted(list(set(fotos_originales)))

    # 3. Mapear los nuevos nombres antes de renombrar para evitar colisiones dinámicas
    operaciones_renombrado = []
    for indice, ruta_foto in enumerate(fotos_originales):
        ext_foto = os.path.splitext(ruta_foto)[1].lower()
        if indice == 0:
            nuevo_nombre = f"{nombre_base}{ext_foto}"
        else:
            nuevo_nombre = f"{nombre_base}_{indice + 1:02d}{ext_foto}"
        
        ruta_nueva = os.path.join(carpeta_objetivo, nuevo_nombre)
        operaciones_renombrado.append((ruta_foto, ruta_nueva))

    # 4. Ejecutar el renombrado de fotos con manejo de sincronización
    for ruta_origen, ruta_destino in operaciones_renombrado:
        if os.path.exists(ruta_origen):
            if ruta_origen != ruta_destino:
                try:
                    os.rename(ruta_origen, ruta_destino)
                    print(f" 📸 Foto renombrada: {os.path.basename(ruta_origen)} -> {os.path.basename(ruta_destino)}")
                    # Pequeña pausa de seguridad de 50ms por si OneDrive está indexando
                    time.sleep(0.05)
                except Exception as e:
                    print(f"⚠️ No se pudo renombrar temporalmente {os.path.basename(ruta_origen)}: {e}")
        else:
            print(f"⚠️ El archivo ya no se encuentra en el origen: {os.path.basename(ruta_origen)}")

    # 5. Renombrar la carpeta contenedora 'modelo'
    nueva_ruta_carpeta = os.path.join(ruta_script, nombre_base)
    
    if os.path.exists(nueva_ruta_carpeta):
        print(f"⚠️ Advertencia: Ya existe una carpeta llamada '{nombre_base}'. Se añadirá un sufijo.")
        contador = 1
        while os.path.exists(f"{nueva_ruta_carpeta}_{contador}"):
            contador += 1
        nueva_ruta_carpeta = f"{nueva_ruta_carpeta}_{contador}"

    # Pausa antes de mover la carpeta completa para asegurar que los descriptores de archivos estén cerrados
    time.sleep(0.2)
    
    try:
        shutil.move(carpeta_objetivo, nueva_ruta_carpeta)
        print(f"📁 Carpeta 'modelo' renombrada con éxito a: {os.path.basename(nueva_ruta_carpeta)}")
    except Exception as e:
        print(f"❌ Error crítico al mover la carpeta. Es posible que OneDrive la tenga bloqueada: {e}")
        return

    # 6. Crear una nueva carpeta vacía llamada 'modelo' para el siguiente ciclo
    os.makedirs(carpeta_objetivo)
    print("✨ Nueva carpeta vacía 'modelo' creada y lista para el siguiente proyecto.")

if __name__ == "__main__":
    organizar_modelo()