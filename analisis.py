from pathlib import Path
import sys
import pandas as pd

# analisis.py
# Herramienta rápida de análisis para "comportamientos.csv"
# Usa: python analisis.py
# Requiere: pandas (pip install pandas)


CSV_NOMBRE = "comportamientos.csv"
TOP_N = 10  # cantidad de entradas principales a mostrar

TIPO_MAP = {
    1: "ingreso",
    2: "click",
    3: "consulta",
    4: "descarga",
    # otros códigos se mantendrán como "otro_{codigo}" si aparecen
}


def cargar_dataframe(path: Path) -> pd.DataFrame:
    if not path.exists():
        print(f"Error: no existe el archivo '{path}'. Colócalo en la misma carpeta que este script.")
        sys.exit(1)

    try:
        df = pd.read_csv(path, dtype=str)
    except Exception as e:
        print(f"Error al leer CSV: {e}")
        sys.exit(1)

    # Normalizar columnas esperadas a nombres simples (quitar espacios alrededor)
    df.columns = [c.strip() for c in df.columns]

    # Asegurar columnas mínimas
    columnas_esperadas = {"ip_usuario", "tipo_movimiento", "origen", "elementos_involucrados", "fecha_hora", "comentarios"}
    faltantes = columnas_esperadas - set(df.columns)
    if faltantes:
        print("Advertencia: faltan columnas esperadas en el CSV:", ", ".join(sorted(faltantes)))
        # Continuar el análisis con las columnas disponibles

    # Convertir tipos
    if "tipo_movimiento" in df.columns:
        # intentar convertir a int donde sea posible
        df["tipo_movimiento_raw"] = df["tipo_movimiento"]
        try:
            df["tipo_movimiento"] = pd.to_numeric(df["tipo_movimiento"], errors="coerce").astype("Int64")
        except Exception:
            # dejar como string si no puede
            df["tipo_movimiento"] = df["tipo_movimiento"].astype(str)

        # mapa a etiquetas legibles
        def map_tipo(x):
            try:
                xi = int(x)
                return TIPO_MAP.get(xi, f"otro_{xi}")
            except Exception:
                return str(x)

        df["tipo_movimiento_lbl"] = df["tipo_movimiento"].apply(map_tipo)

    # fecha_hora -> datetime
    if "fecha_hora" in df.columns:
        df["fecha_hora_raw"] = df["fecha_hora"]
        df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], errors="coerce", infer_datetime_format=True)

    # Trim de strings en columnas de texto
    for col in ["ip_usuario", "origen", "elementos_involucrados", "comentarios"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({"nan": pd.NA})

    return df


def resumen_general(df: pd.DataFrame):
    print("==== RESUMEN GENERAL ====")
    print(f"Registros: {len(df)}")
    print("Columnas:", ", ".join(df.columns))
    print("\nTipos de datos:")
    print(df.dtypes)
    print("\nValores faltantes por columna:")
    print(df.isna().sum().sort_values(ascending=False))
    print("\nValores únicos por columna (muestra):")
    print(df.nunique().sort_values(ascending=False).head(20))


def distribuciones_clave(df: pd.DataFrame, top_n: int = TOP_N):
    print("\n==== DISTRIBUCIONES CLAVE ====")
    if "origen" in df.columns:
        print(f"\nTop {top_n} orígenes (conteo y %) :")
        vc = df["origen"].value_counts(dropna=True).head(top_n)
        pct = (vc / len(df) * 100).round(2)
        print(pd.concat([vc, pct.rename("porcentaje")], axis=1))

    if "tipo_movimiento_lbl" in df.columns:
        print(f"\nDistribución de tipo_movimiento:")
        vm = df["tipo_movimiento_lbl"].value_counts(dropna=False)
        pct = (vm / len(df) * 100).round(2)
        print(pd.concat([vm, pct.rename("porcentaje")], axis=1))

    if "elementos_involucrados" in df.columns:
        print(f"\nTop {top_n} elementos involucrados:")
        print(df["elementos_involucrados"].value_counts(dropna=True).head(top_n))

    if "ip_usuario" in df.columns:
        print(f"\nTop {top_n} usuarios por número de registros (ip_usuario):")
        print(df["ip_usuario"].value_counts(dropna=True).head(top_n))


def analisis_temporal(df: pd.DataFrame):
    if "fecha_hora" not in df.columns:
        print("\nNo se dispone de fecha_hora para análisis temporal.")
        return

    print("\n==== ANÁLISIS TEMPORAL ====")
    n_validas = df["fecha_hora"].notna().sum()
    print(f"Fechas válidas: {n_validas} / {len(df)}")
    if n_validas == 0:
        return

    fecha_min = df["fecha_hora"].min()
    fecha_max = df["fecha_hora"].max()
    print(f"Rango temporal: {fecha_min}  ->  {fecha_max}")

    # Registros por día
    por_dia = df.loc[df["fecha_hora"].notna(), "fecha_hora"].dt.date.value_counts().sort_index()
    print(f"\nMuestra de registros por día (primeras 10 entradas):")
    print(por_dia.head(10))

    # Horas más activas
    horas = df.loc[df["fecha_hora"].notna(), "fecha_hora"].dt.hour.value_counts().sort_values(ascending=False)
    print(f"\nHoras más activas (hora : registros) top 10:")
    print(horas.head(10))


def cruces_y_pivotes(df: pd.DataFrame):
    print("\n==== CRUCES Y PIVOTES ÚTILES ====")
    # Origen vs tipo_movimiento
    if "origen" in df.columns and "tipo_movimiento_lbl" in df.columns:
        ct = pd.crosstab(df["origen"], df["tipo_movimiento_lbl"])
        # mostrar las 10 filas con más interacciones totales
        ct["total"] = ct.sum(axis=1)
        ct = ct.sort_values("total", ascending=False).drop(columns=["total"])
        print("\nCrosstab origen x tipo_movimiento (primeras 10 filas):")
        print(ct.head(10))

    # Elemento más asociado a cada tipo de movimiento
    if "elementos_involucrados" in df.columns and "tipo_movimiento_lbl" in df.columns:
        print("\nElemento más frecuente por tipo_movimiento:")
        grp = df.dropna(subset=["elementos_involucrados", "tipo_movimiento_lbl"]).groupby("tipo_movimiento_lbl")["elementos_involucrados"]
        top_elementos = grp.apply(lambda s: s.value_counts().head(1))
        # top_elementos es un Series multindex, mostrar de forma resumida
        for tipo, sub in top_elementos.groupby(level=0):
            try:
                el = sub.index[0][1]
                cnt = sub.iloc[0]
                print(f"- {tipo}: {el} ({cnt} veces)")
            except Exception:
                pass


def muestras_comentarios(df: pd.DataFrame, n: int = 5):
    print("\n==== MUESTRAS DE COMENTARIOS ====")
    if "comentarios" not in df.columns:
        print("No hay columna 'comentarios'.")
        return
    comentarios = df["comentarios"].dropna()
    total = len(comentarios)
    print(f"Comentarios no nulos: {total}")
    if total == 0:
        return
    n = min(n, total)
    print(f"Muestra aleatoria de {n} comentarios:")
    try:
        muestra = comentarios.sample(n)
    except Exception:
        muestra = comentarios.head(n)
    for i, c in enumerate(muestra.tolist(), 1):
        print(f"{i}. {c}")


def guardar_resumen_simple(df: pd.DataFrame, out_path: Path):
    resumen = {}
    resumen["total_registros"] = len(df)
    if "origen" in df.columns:
        resumen["top_origen"] = df["origen"].value_counts().head(10).to_dict()
    if "tipo_movimiento_lbl" in df.columns:
        resumen["top_tipo_movimiento"] = df["tipo_movimiento_lbl"].value_counts().head(10).to_dict()
    if "elementos_involucrados" in df.columns:
        resumen["top_elementos"] = df["elementos_involucrados"].value_counts().head(10).to_dict()

    # Guardar como CSV sencillo (cada clave en una fila) para revisión rápida
    rows = []
    for k, v in resumen.items():
        rows.append({"clave": k, "valor": str(v)})
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f"\nResumen guardado en: {out_path}")


def main():
    ruta_csv = Path(__file__).parent / CSV_NOMBRE
    df = cargar_dataframe(ruta_csv)

    resumen_general(df)
    distribuciones_clave(df)
    analisis_temporal(df)
    cruces_y_pivotes(df)
    muestras_comentarios(df)

    # Guardar resumen simple
    out_csv = Path(__file__).parent / "reporte_resumen.csv"
    guardar_resumen_simple(df, out_csv)
    print("\nAnálisis finalizado.")


if __name__ == "__main__":
    main()