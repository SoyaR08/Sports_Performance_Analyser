import matplotlib.pyplot as plt

def plot_top_players(df, value_col, title, filename, top_n=10):
    """
    Genera un gráfico de barras de los top jugadores y lo guarda en PDF.

    df        : DataFrame con columnas 'name' y value_col
    value_col : columna a graficar ('goals', 'assists', 'saves_pm')
    title     : título del gráfico
    filename  : nombre del archivo PDF donde guardar
    top_n     : cuántos jugadores mostrar
    """

    # Seleccionamos los top N
    top_df = df.sort_values(value_col, ascending=False).head(top_n)

    plt.figure(figsize=(10,6))
    bars = plt.bar(top_df["name"], top_df[value_col], color="#1f77b4")
    plt.title(title, fontsize=16)
    plt.xlabel("Jugador", fontsize=12)
    plt.ylabel(value_col.replace("_", " ").title(), fontsize=12)
    plt.xticks(rotation=45, ha="right")

    # Añadir valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.05, f'{height:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(filename, format="pdf")
    plt.close()

def plot_top_scorers(scorers, top_n=10):
    plot_top_players(scorers, "goals", "Top Goleadores", "top_goleadores.pdf", top_n)

def plot_top_assistants(assistants, top_n=10):
    plot_top_players(assistants, "assists", "Top Asistentes", "top_asistentes.pdf", top_n)

def plot_top_goalkeepers(goalkeepers, top_n=10):
    plot_top_players(goalkeepers, "saves_pm", "Mejores Porteros (Saves/90min)", "top_porteros.pdf", top_n)