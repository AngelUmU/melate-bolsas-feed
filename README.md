# melate-bolsas-feed

Relevo de datos para la rutina semanal de análisis de lotería. El entorno cloud
donde corre esa rutina (`claude.ai/code/routines`) no tiene salida de red hacia
`loterianacional.gob.mx`, así que un GitHub Action (que sí tiene internet normal)
descarga las bolsas vigentes cada lunes y las deja en `bolsas.json`. La rutina
clona este repo y lee ese archivo en vez de intentar descargar directamente.

- `scripts/actualizar_bolsas.py` — baja los 4 CSVs oficiales, toma la fila del
  concurso más reciente de cada uno y escribe `bolsas.json`.
- `.github/workflows/actualizar-bolsas.yml` — corre el script 8:50am hora CDMX
  (10 min antes de la rutina) los días con sorteo esa noche: domingo, martes,
  miércoles, viernes y sábado. También se puede disparar a mano desde la
  pestaña Actions ("Run workflow").
- Además de la bolsa vigente, `bolsas.json` guarda los números ganadores del
  último sorteo de cada juego (`numeros_ganadores` + `adicional`), que la
  rutina usa para verificar si las combinaciones sugeridas coincidieron.
