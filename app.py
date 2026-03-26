import random
import time
import streamlit as st
import sparky4


def _parse_sorteo_anterior(raw: str) -> tuple[list[int] | None, str | None]:
	tokens = [t for t in raw.replace(",", " ").split() if t]
	if len(tokens) != 5:
		return None, "Ingresa exactamente 5 números separados por espacios (ej: 4 12 17 21 28)."
	try:
		nums = [int(t) for t in tokens]
	except ValueError:
		return None, "Todos los valores deben ser números enteros."

	if any(n < 1 or n > sparky4.NUMERO_MAXIMO for n in nums):
		return None, f"Todos los números deben estar entre 1 y {sparky4.NUMERO_MAXIMO}."
	if len(set(nums)) != 5:
		return None, "No repitas números: deben ser 5 valores distintos."
	return nums, None


def _progreso(segundos: int) -> None:
	mensajes = sparky4.MENSAJES_PROGRESO

	progress = st.progress(0, text=mensajes[0])
	if segundos <= 0:
		progress.progress(100, text=mensajes[-1])
		return

	pasos = 100
	delay = float(segundos) / pasos
	for i in range(pasos + 1):
		idx = int((i / 100) * len(mensajes))
		if idx >= len(mensajes):
			idx = len(mensajes) - 1
		progress.progress(i, text=mensajes[idx])
		# Sleep
		time.sleep(delay)
		#st.sleep(delay)


def main() -> None:
	st.set_page_config(page_title="Sparky4", layout="centered")
	st.title("Sparky4")

	st.subheader("Paso 1: Datos Base")
	raw = st.text_input(
		"Ingresa los 5 números del SORTEO ANTERIOR separados por un espacio",
		placeholder="Ej: 4 12 17 21 28",
	)

	st.subheader("Paso 2: Selecciona la arquitectura de la jugada")
	opcion = st.selectbox(
		"Estructura Primos/Compuestos",
		options=[
			(1, "2 Primos y 3 Compuestos (Recomendada: 29.7% prob.)"),
			(2, "1 Primo y 4 Compuestos (Recomendada: 27.6% prob.)"),
		],
		index=0,
		format_func=lambda x: x[1],
	)[0]

	col1, col2, col3 = st.columns(3)
	with col1:
		segundos = st.number_input(
			"Duración del progreso (seg)",
			min_value=0,
			max_value=30,
			value=10,
			step=1,
		)
	with col2:
		seed = st.text_input("Semilla (opcional)", value="")

	if st.button("Generar combinación", type="primary"):
		sorteo_anterior, error = _parse_sorteo_anterior(raw)
		if error:
			st.error(error)
			return

		if seed.strip():
			random.seed(seed.strip())

		# Reutilizamos el “motor” original.
		combinacion_final, iteraciones = sparky4.generar_combinacion(sorteo_anterior, opcion)

		# Y mostramos un progreso visual equivalente.
		_progreso(int(segundos))

		st.success("✓ ¡COMBINACIÓN ENCONTRADA Y VERIFICADA!")
		st.write("Combinación sugerida:")
		st.code(str(combinacion_final), language="text")
		st.write(f"Centro de gravedad (Suma): {sum(combinacion_final)}")
		st.write(f"Fuerza bruta utilizada: {iteraciones} iteraciones")
	

	st.markdown("Proyecto original de [Nestor Quiñones](https://github.com/Nesthings/sparky4)")

if __name__ == "__main__":
	main()
