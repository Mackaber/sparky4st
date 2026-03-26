import random
import time
import sys
import os

# Habilitar colores en la consola
if os.name == 'nt':
    os.system('color')

# --- COLORES PARA LA CONSOLA ---
RESET = '\033[0m'
BOLD = '\033[1m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
RED = '\033[91m'

# --- CONFIGURACIÓN DE PATRONES ---
NUMERO_MAXIMO = 28
PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}
NUMEROS_CALIENTES = {10, 17, 21, 18, 23}
NUMEROS_FRIOS = {13, 3, 27, 26, 28}

def es_primo(n):
    return n in PRIMOS

def es_compuesto(n):
    return n > 1 and n not in PRIMOS

def generar_combinacion(sorteo_anterior, opcion_primos):
    if opcion_primos == 1:
        target_primos = 2
        target_compuestos = 3
    elif opcion_primos == 2:
        target_primos = 1
        target_compuestos = 4
    else:
        print(f"{RED}Opción no válida. Se usará por defecto 2 Primos y 3 Compuestos.{RESET}")
        target_primos = 2
        target_compuestos = 3

    intentos = 0
    while True:
        intentos += 1
        combo = set()

        # REGLA 1: Repetir
        numero_repetido = random.choice(sorteo_anterior)
        combo.add(numero_repetido)

        # REGLA 2: Consecutivo
        paso = 1 if random.random() > 0.5 else -1
        consecutivo = numero_repetido + paso
        if consecutivo < 1: consecutivo = numero_repetido + 1
        if consecutivo > NUMERO_MAXIMO: consecutivo = numero_repetido - 1
        combo.add(consecutivo)

        # REGLA 3: Mismo último dígito
        base_num = random.choice(list(combo))
        ultimo_digito = base_num % 10
        posibles_parejas = [x for x in range(1, NUMERO_MAXIMO + 1) if x % 10 == ultimo_digito and x not in combo]
        if posibles_parejas:
            combo.add(random.choice(posibles_parejas))

        # Rellenar con Calientes y evitar Fríos
        piscina_numeros = [x for x in range(1, NUMERO_MAXIMO + 1) if x not in combo and x not in NUMEROS_FRIOS]
        piscina_numeros.extend([x for x in NUMEROS_CALIENTES if x not in combo])
        
        while len(combo) < 5:
            combo.add(random.choice(piscina_numeros))
            
        jugada = list(combo)[:5]

        # --- FILTROS FINALES ---
        suma_total = sum(jugada)
        if not (60 <= suma_total <= 85):
            continue
            
        impares = sum(1 for x in jugada if x % 2 != 0)
        pares = 5 - impares
        if not ((impares == 3 and pares == 2) or (impares == 2 and pares == 3)):
            continue
            
        cant_primos = sum(1 for x in jugada if es_primo(x))
        cant_compuestos = sum(1 for x in jugada if es_compuesto(x))
        
        if cant_primos != target_primos or cant_compuestos != target_compuestos:
            continue
            
        jugada.sort()
        return jugada, intentos


def barra_de_progreso_emocionante(segundos=10):
    mensajes = [
        "Iniciando motor matemático...",
        "Aplicando Regla del 66% (Extrayendo del sorteo anterior)...",
        "Forzando patrón de diferencias...",
        "Calculando emparejamiento de último dígito...",
        "Pesando Números Calientes y descartando Fríos...",
        "Ajustando centro de gravedad...",
        "Equilibrando balanza de Pares e Impares (3:2)...",
        "Validando estructura estricta de Primos/Compuestos...",
        "Descartando combinaciones estadísticamente débiles...",
        "¡Alineación probabilística completada con éxito!"
    ]
    
    pasos = 100
    tiempo_por_paso = segundos / pasos
    longitud_barra = 40

    print("\n")
    for i in range(pasos + 1):
        # Determinar qué mensaje mostrar basado en el progreso
        idx_mensaje = int((i / 100) * len(mensajes))
        if idx_mensaje >= len(mensajes):
            idx_mensaje = len(mensajes) - 1
            
        mensaje_actual = mensajes[idx_mensaje]
        
        # Dibujar la barra
        relleno = int(longitud_barra * i // 100)
        barra = '█' * relleno + '-' * (longitud_barra - relleno)
        porcentaje = f"{i}%"
        
        # Imprimir en la misma línea sobrescribiéndola
        sys.stdout.write(f"\r{GREEN}[{barra}] {YELLOW}{porcentaje:<4}{RESET} | {CYAN}{mensaje_actual:<60}{RESET}")
        sys.stdout.flush()
        time.sleep(tiempo_por_paso)
    print("\n")

# --- INTERFAZ DEL PROGRAMA ---
print(f"{CYAN}=================================================={RESET}")
print(f"""{YELLOW}
          .
         / \\
      --( * )--
         \\ /
          '{CYAN}
    ____                    _          _  _  
   / ___| _ __   __ _ _ __ | | ___   _| || | 
   \___ \| '_ \ / _` | '__|| |/ / | | | || |_
    ___) | |_) | (_| | |   |   <| |_| |__   _|
   |____/| .__/ \__,_|_|   |_|\_\\__, |  |_| 
         |_|                     |___/       
{RESET}""")
print(f"{CYAN}=================================================={RESET}\n")

# 1. Pedir el sorteo anterior
print(f"{BOLD}{MAGENTA}Paso 1:{RESET} Datos Base")
entrada = input(f"Ingresa los 5 números del {YELLOW}SORTEO ANTERIOR{RESET} separados por un espacio (Ej: 4 12 17 21 28):\n> ")
sorteo_anterior = [int(x) for x in entrada.strip().split()]

# 2. Pedir la estructura de Primos/Compuestos
print(f"\n{BOLD}{MAGENTA}Paso 2:{RESET} Selecciona la arquitectura de la jugada")
print(f"{GREEN}1){RESET} 2 Primos y 3 Compuestos {YELLOW}(Recomendada: 29.7% prob.){RESET}")
print(f"{GREEN}2){RESET} 1 Primo y 4 Compuestos  {YELLOW}(Recomendada: 27.6% prob.){RESET}")
opcion = int(input(f"> Opción {CYAN}(1 o 2){RESET}: "))

# Ocultamos la generación en background
combinacion_final, iteraciones = generar_combinacion(sorteo_anterior, opcion)

# 3. La barra de progreso de 10 segundos (se puede modificar a tu antojo)
barra_de_progreso_emocionante(10)

# 4. Mostrar resultados
print(f"{YELLOW}=================================================={RESET}")
print(f"{BOLD}{GREEN}✓ ¡COMBINACIÓN ENCONTRADA Y VERIFICADA!{RESET}")
print(f"Combinación sugerida: {CYAN}{BOLD}{combinacion_final}{RESET}")
print(f"Centro de gravedad (Suma): {MAGENTA}{sum(combinacion_final)}{RESET}")
print(f"Fuerza bruta utilizada: {RED}{iteraciones} iteraciones{RESET} para hallar el patrón perfecto.")
print(f"{YELLOW}=================================================={RESET}\n")
