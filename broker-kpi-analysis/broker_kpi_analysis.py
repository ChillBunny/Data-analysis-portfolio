# Comparative KPI Analysis of Stock Brokers — Dominican securities market
#
# IMPORTANT: the data below is SIMULATED. Broker names and SIVCV codes come from
# the PUBLIC registry of the Superintendencia del Mercado de Valores (SIMV), but
# every figure (returns, fees, AUM, execution) is fictional and invented for
# demonstration purposes. See the full disclaimer in README.md — this is a
# portfolio exercise, not real financial data and not investment advice.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Simulated broker data (real names/codes, fictional figures)
data = """
Broker,Retorno Promedio Anual (%),Clasificación de Riesgos,Comisiones (%),Activos Bajo Gestión (MM USD),Ejecución Órdenes (%)
Wendy Peña (SIVCV-531),13.2,5,0.25,1450,97.5
Pedro Ciccone (SIVCV-440),11.0,6,0.10,1600,96.2
Omar Paula (SIVCV-397),8.3,7,0.35,900,92.8
Nathalie Machado (SIVCV-169),14.8,4,0.30,1800,98.9
Nabila Ramia (SIVCV-140),10.7,2,0.15,1100,93.5
Mario Mera (SIVCV-519),9.1,8,0.20,1300,94.4
Maria Lembert (SIVCV-333),6.2,1,0.12,750,95.1
Maria Jose Chami (SIVCV-474),13.9,3,0.18,1650,96.7
Luis Molina (SIVCV-441),11.3,6,0.27,1400,94.8
Leyvi Castillo (SIVCV-366),15.7,9,0.40,950,97.1
Jean Elmúdesi (SIVCV-218),12.2,5,0.22,1700,95.9
"""

df = pd.read_csv(StringIO(data))

# One consistent color per broker across every chart
palette = sns.color_palette("husl", len(df))
broker_colors = dict(zip(df["Broker"], palette))


def plot_scatter(x, y, xlabel, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    for broker in df["Broker"]:
        broker_data = df[df["Broker"] == broker]
        plt.scatter(
            broker_data[x],
            broker_data[y],
            s=200,
            label=broker,
            color=broker_colors[broker],
            alpha=0.85,
        )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize="small")
    plt.tight_layout()
    plt.savefig(f"images/{filename}", dpi=150)
    plt.show()


# Comparison table, best return first
print("\n=== Broker comparison ===\n")
print(df.sort_values(by="Retorno Promedio Anual (%)", ascending=False))

# 1. Risk vs annual return
plot_scatter(
    x="Clasificación de Riesgos",
    y="Retorno Promedio Anual (%)",
    xlabel="Risk rating (1 = low, 9 = high)",
    ylabel="Average annual return (%)",
    title="Risk vs Annual Return",
    filename="risk_vs_return.png",
)

# 2. Fees vs return
plot_scatter(
    x="Comisiones (%)",
    y="Retorno Promedio Anual (%)",
    xlabel="Fees (%)",
    ylabel="Average annual return (%)",
    title="Fees vs Average Return",
    filename="fees_vs_return.png",
)

# 3. Order execution vs risk
plot_scatter(
    x="Clasificación de Riesgos",
    y="Ejecución Órdenes (%)",
    xlabel="Risk rating (1 = low, 9 = high)",
    ylabel="Order execution (%)",
    title="Order Execution vs Risk",
    filename="execution_vs_risk.png",
)

# 4. Return vs assets under management
plot_scatter(
    x="Activos Bajo Gestión (MM USD)",
    y="Retorno Promedio Anual (%)",
    xlabel="Assets under management (MM USD)",
    ylabel="Average annual return (%)",
    title="Return vs Assets Under Management",
    filename="return_vs_aum.png",
)

# 5. Risk vs assets under management
plot_scatter(
    x="Clasificación de Riesgos",
    y="Activos Bajo Gestión (MM USD)",
    xlabel="Risk rating (1 = low, 9 = high)",
    ylabel="Assets under management (MM USD)",
    title="Risk vs Assets Under Management",
    filename="risk_vs_aum.png",
)
