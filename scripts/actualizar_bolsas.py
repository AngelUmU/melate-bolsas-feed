import csv
import io
import json
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

FUENTES = {
    "melate": "https://www.loterianacional.gob.mx/Documentos/Historicos/Melate.csv",
    "revancha": "https://www.loterianacional.gob.mx/Documentos/Historicos/Revancha.csv",
    "revanchita": "https://www.loterianacional.gob.mx/Documentos/Historicos/Revanchita.csv",
    "melate_retro": "https://www.loterianacional.gob.mx/Documentos/Historicos/Melate-Retro.csv",
}


def ultima_fila(url: str) -> dict:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as r:
        texto = r.read().decode("utf-8", errors="replace")
    filas = list(csv.DictReader(io.StringIO(texto)))
    if not filas:
        raise ValueError("CSV vacío")
    fila = max(filas, key=lambda f: int(f["CONCURSO"]))
    return {
        "concurso": int(fila["CONCURSO"]),
        "bolsa": int(fila["BOLSA"]),
        "fecha": fila["FECHA"],
    }


def main() -> int:
    salida = {
        "generado_utc": datetime.now(timezone.utc).isoformat(),
        "juegos": {},
        "errores": {},
    }
    for juego, url in FUENTES.items():
        try:
            salida["juegos"][juego] = ultima_fila(url)
            print(f"{juego}: OK -> {salida['juegos'][juego]}")
        except Exception as e:
            salida["errores"][juego] = str(e)
            print(f"{juego}: ERROR -> {e}", file=sys.stderr)

    with open("bolsas.json", "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False)

    return 0


if __name__ == "__main__":
    sys.exit(main())
