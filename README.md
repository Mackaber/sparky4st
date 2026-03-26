## Version original por [Nestor Quiñones](https://github.com/Nesthings/sparky4)

Disponible aquí: https://sparky4st.streamlit.app/

## Descripción General

Este proyecto nace de la observación y el análisis profundo de un conjunto de datos históricos compuesto por más de 11,900 sorteos del sorteo Chispazo de la Lotería Nacional.

El objetivo fue validar empíricamente la existencia de patrones ocultos en las combinaciones ganadoras y, posteriormente, desarrollar un algoritmo en Python capaz de generar nuevas jugadas altamente probables utilizando "fuerza bruta inteligente" y filtros estadísticos estrictos.

---

## Metodología de Investigación

Se utilizó Python (junto con la librería `pandas`) para ingestar y analizar el historial completo de sorteos. Se pusieron a prueba hipótesis de intuición humana frente a la rigurosidad matemática, midiendo frecuencias, distancias entre números (deltas), paridad, sumatorias y la distribución de números primos y compuestos.

---

## Hallazgos Estadísticos 

Tras analizar las miles de filas de resultados, la estadística confirmó la existencia de patrones dominantes fuertemente marcados:

### 1. El Efecto de Arrastre
El **66.21%** de los sorteos contiene al menos un número que resultó ganador en el sorteo inmediatamente anterior. Es decir, 2 de cada 3 sorteos arrastran un número del pasado.

### 2. La Ley del Gemelo (Mismo último dígito)
En el **56.81%** de las combinaciones ganadoras, existen al menos dos números que terminan en el mismo dígito (ejemplo: 7 y 17, ó 14 y 24).

### 3. El Imán Consecutivo (Diferencias)
- Al analizar las diferencias entre casillas (D-P1-P2, etc.), la diferencia más común es el **1**.
- En el **56.83%** de los sorteos aparece al menos un par de números consecutivos.
- El "rango" (la diferencia entre el número más grande y el más pequeño de la serie) promedia consistentemente entre **19 y 21**.

### 4. Distribución de Primos y Compuestos
> Matemáticamente, el número 1 no se considera ni primo ni compuesto.

Las estructuras más exitosas son:

| Estructura | Frecuencia |
|---|---|
| 2 Primos y 3 Compuestos | 29.7% — La configuración reina |
| 1 Primo y 4 Compuestos | 27.6% |
| 5 primos o 5 compuestos | < 2% de probabilidad histórica |

### 5. El "Centro de Gravedad" (Regla de la Suma)
- Al sumar los 5 números de una combinación ganadora, la **media histórica converge exactamente en 72**.
- El rango seguro de sumatoria para una jugada estadísticamente viable se encuentra entre **60 y 85**.

### 6. Equilibrio Par / Impar

| Distribución | Probabilidad |
|---|---|
| 3 Impares y 2 Pares | 34.3% |
| 2 Impares y 3 Pares | 33.2% |

El **67.5%** de las jugadas ganadoras mantienen este balance, descartando casi por completo jugadas que sean 100% pares o 100% impares.

### 7. Mapa de Calor (Histórico Absoluto)

- **Números Calientes** (Alta frecuencia): `10, 17, 21, 18, 23`
- **Números Fríos** (Baja frecuencia): `13, 3, 27, 26, 28`

---

## Como funciona el Algoritmo (Sparky4)

El algoritmo no genera números al azar a ciegas; utiliza un enfoque de **Fuerza Bruta Guiada con Filtros de Rechazo**. Funciona en dos fases:

### Fase 1: Generación Guiada (Intuición Aleatoria)

Se construye un set inicial de 5 números donde la aleatoriedad está sesgada positivamente:

1. Extrae obligatoriamente **1 número aleatorio del sorteo anterior** que el usuario ingresa.
2. Agrega aleatoriamente un número **consecutivo** a este (sumando o restando 1).
3. Busca y agrega una **"pareja"** que comparta el último dígito con alguno de los números ya elegidos.
4. Rellena los huecos restantes ponderando fuertemente los **Números Calientes** y excluyendo los **Números Fríos**.

### Fase 2: El Escudo de Filtros (Aprobación Estricta)

Una vez generada la serie de 5 números, pasa por 3 filtros inquebrantables. Si la serie falla en uno solo de ellos, el algoritmo la destruye y vuelve a la Fase 1.

| Filtro | Condición |
|---|---|
| **Filtro A** | La suma total de los 5 números DEBE estar entre **60 y 85** |
| **Filtro B** | DEBE contener exactamente **3 impares/2 pares** o **2 impares/3 pares** |
| **Filtro C** | DEBE coincidir con la estructura de Primos/Compuestos elegida por el usuario (2/3 ó 1/4) |

El script puede iterar miles de veces en milisegundos hasta encontrar la combinación que pase todos los filtros.

---

## Uso

1. Clona el repositorio y ejecuta el script en cualquier entorno **Python 3.x**.
2. Ingresa los **5 números del sorteo inmediato anterior** cuando la consola lo solicite.
3. Elige tu estrategia de Primos/Compuestos (**Opción 1** u **Opción 2**).
4. Espera la animación de carga interactiva en la consola para recibir tu combinación óptima.

---

> **Disclaimer:** Este proyecto es un ejercicio de exploración de datos y estadística aplicada. La lotería y los juegos de azar son eventos independientes; los patrones históricos aumentan la viabilidad matemática de una estructura, pero no garantizan la victoria. ¡Juega con responsabilidad!
