# app.py
import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# =========================================
#           Répertoires du projet
# =========================================
# app.py est dans src/, on remonte à la racine du repo
ROOT   = Path(__file__).resolve().parent.parent
DATA   = ROOT / "data" / "raw" / "Cleaned_data" / "InUSE"
ASSETS = ROOT / "data" / "data_streamlit"

def safe_image(name: str, **kwargs):
    """Affiche l'image si elle existe; sinon un warning propre."""
    path = ASSETS / name
    if path.exists():
        st.image(str(path), **kwargs)
    else:
        st.warning(f"⚠️ Image manquante : {name} (attendue dans {ASSETS})")

# =========================================
#            Configuration page
# =========================================
st.set_page_config(
    page_title="London Fire Response - Analyse & Prévisions",
    page_icon="🚒",
    layout="wide",
)

# =========================================
#           Chargement des données
# =========================================
@st.cache_data
def charger_donnees():
    incidents_path = DATA / "cleaned_data_incidents.csv"
    mobilis_path   = DATA / "cleaned_data_mobilisations.csv"

    if not incidents_path.exists():
        st.error(f"Fichier introuvable : {incidents_path}")
        st.stop()
    if not mobilis_path.exists():
        st.error(f"Fichier introuvable : {mobilis_path}")
        st.stop()

    df    = pd.read_csv(incidents_path, low_memory=False, parse_dates=["DateOfCall"])
    # Ajuste parse_dates si une colonne date existe côté mobilisations
    df_mb = pd.read_csv(mobilis_path, low_memory=False)

    return df, df_mb

df, df_mb = charger_donnees()


# =========================================
#           Sidebar / Navigation
# =========================================
st.sidebar.title("Bienvenue dans l'application 🤗")

# Image sidebar (place "BrigadeLondres.jpeg" dans data/data_streamlit)
sidebar_img = "BrigadeLondres.jpeg"
if (ASSETS / sidebar_img).exists():
    st.sidebar.image(str(ASSETS / sidebar_img), caption="London Fire Brigade", use_container_width=True)
else:
    st.sidebar.warning(f"⚠️ Image '{sidebar_img}' introuvable – place-la dans {ASSETS}.")

menu = st.sidebar.radio(
    "Sections",
    [
        "1. Présentation du projet",
        "2. Données & Prétraitement",
        "3. Exploration des données",
        "4. Modélisation des séries temporelles",
        "5. Prédictions futures",
        "6. Comparaison des modèles",
        "7. Conclusion & Perspectives",
    ],
)

# =========================================
# 1. Présentation
# =========================================
if menu == "1. Présentation du projet":
    st.title("🚒 London Fire Response – Prédiction du nombre d'interventions futures")

    st.markdown("""
**Bienvenue dans l’univers de l’analyse prédictive des interventions de la London Fire Brigade !**

**👩‍🚒 Depuis 1865, la London Fire Brigade protège 9 millions de Londoniens grâce à plus de 100 casernes : des pompiers aguerris, dopés aux datas (et au thé anglais) qui surgissent avant même que le toast ne brûle.**

### 🎯 Objectif stratégique
Nos modèles estiment chaque jour le **nombre d’interventions** à venir pour :
- **Réduire les délais d’intervention** en prépositionnant les équipes où le volume sera le plus élevé.
- **Optimiser les coûts** en ajustant le nombre de camions et de personnels selon la charge prévue.
- **Renforcer la résilience** en détectant les anomalies (pics imprévus) et en adaptant la réponse.

### 📋 Contexte métier
Chaque jour, des milliers d’incidents sont gérés : feux, fausses alertes, secours médicaux…
La variance saisonnière (pics d’été, vagues de froid), événementielle (grands événements, crises) et géographique (arrondissements) complique la planification.

**Notre application Streamlit** permet de :
- Visualiser l’**historique des volumes** d’interventions.
- Comprendre les **patterns** via STL, SARIMA et Prophet.
- Afficher les **prévisions** de nombre quotidien d’appels, avec intervalles de confiance.

### 🔍 Valeur ajoutée technique
- **Pipeline de données** : ingestion, nettoyage.
- **Exploration interactive** : courbes dynamiques, filtres multi-dimensionnels.
- **Prédiction** :
  - **STL** pour isoler tendance et saisonnalité.
  - **SARIMA** pour capter la saisonnalité mensuelle.
  - **Prophet** pour intégrer effets calendaires et anomalies.

### 🚀 Perspectives métier
- **Tableau de bord** des volumes attendus par incident — extensible aux quartiers, arrondissements…
- **Alertes** automatiques si la demande excède les seuils critiques.
- **Optimisation des tournées** grâce aux prévisions couplées à la géolocalisation.

> « Nos modèles ne prévoient pas juste une tendance, ils comptent chaque intervention à venir ! »
""")

# =========================================
# 2. Données & Prétraitement
# =========================================
elif menu == "2. Données & Prétraitement":
    st.title("📊 Jeux de données")

    dataset_option = st.radio("Sélectionne un dataset :", ("Dataset Principal", "Dataset Secondaire"))

    if dataset_option == "Dataset Principal":
        st.header("DATASET PRINCIPAL")

        st.subheader("1. Source")
        st.markdown("""
Le jeu de données principal provient du [London Fire Brigade Incident Records](https://data.london.gov.uk/dataset/london-fire-brigade-incident-records),
mis à disposition par le **Greater London Authority**.
""")

        st.subheader("2. Période")
        st.markdown("""Incidents couvrant la période **1ᵉʳ janvier 2009 → 31 mars 2025**.""")

        st.subheader("3. Remarques")
        st.markdown("""
- Granularité **incident** ; nécessite nettoyage/harmonisation
- Colonnes redondantes ou vides à filtrer.
- Localisations enrichissables avec des jeux externes.
""")

        st.subheader("4. Extrait du DataFrame")
        st.dataframe(df.head(10))

        st.subheader("5. Statistiques descriptives")
        st.dataframe(df.describe(include="all").transpose())

    else:
        st.header("DATASET SECONDAIRE")

        st.subheader("1. Source")
        st.markdown("""Données de **mobilisation** issues du même portail officiel, disponibles en annexe.""")

        st.subheader("2. Période")
        st.markdown("""Couverture **2009 → 2025**, alignée sur le dataset incidents.""")

        st.subheader("3. Remarques")
        st.markdown("""
- Nombreuses valeurs manquantes sur les colonnes temps.
- Fichiers Excel converti en **CSV**.
- Jointure via la clé **`IncidentNumber`** harmonisée et formatée.
-La jointure a été analysée mais pas utilisée pour la modélisation car:
1-données incompletes
2-temps de traitement et volumétrie trop important pour l'usage
""")

        st.subheader("4. Extrait du DataFrame")
        st.dataframe(df_mb.head(10))

        st.subheader("5. Statistiques descriptives")
        st.dataframe(df_mb.describe(include="all").transpose())

# =========================================
# 3. Exploration des données
# =========================================

elif menu == "3. Exploration des données":
    st.title("🔍 Analyse exploratoire des données")

    choix_exploration = st.radio(
        "Sélectionner le type de données à explorer :",
        ("Incidents", "Mobilisations")
    )

    # -------------------- Incidents --------------------
    if choix_exploration == "Incidents":
        st.markdown("""
        Cette section explore **les incidents** : 
        - leur évolution dans le temps,  
        - leur typologie (nature),  
        - leur répartition géographique,  
        - et les délais d’intervention.

        **Objectif :** identifier les tendances, anomalies et zones à forte activité.
        """)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total incidents", f"{df.shape[0]:,}")
        col2.metric("Catégories d'incident", f"{df['IncidentGroup'].nunique()}")
        col3.metric("Arrondissements touchés", f"{df['IncGeo_BoroughName'].nunique()}")

        tab_vol, tab_types, tab_geo, tab_delais = st.tabs(
            ["📈 Volume annuel", "🌀 Typologie", "📍 Géographie", "⏱️ Délais"]
        )

        with tab_vol:
            st.subheader("Nombre d’incidents par an")
            safe_image("nombresincidents.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - **2009-2014** : baisse (-28 %) attribuable aux campagnes de prévention.
            - **2015-2023** : tendance stable avec des fluctuations saisonnières.
            - **Pic 2024** (> 134k) : probablement lié aux vagues de chaleur.
            - **2025** : données partielles (janvier à mars seulement).
            """)

        with tab_types:
            st.subheader("Répartition par type d’incident")
            safe_image("repartition.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - Les **False Alarm** représentent une part importante, impactant la charge opérationnelle.
            - Les incidents **Fire** et **Special Service** sont plus variables et sensibles aux saisons.
            """)

            st.markdown("**Évolution des ‘False Alarm’**")
            safe_image("evolutionfalsealarm.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - Progression nette depuis 2018, pouvant refléter un changement de protocole ou une hausse de signalements.
            """)

        with tab_geo:
            st.subheader("Top 15 arrondissements")
            safe_image("borough_top15.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - Forte concentration dans quelques boroughs (forte densité + zones à risque).
            - Ces zones pourraient être prioritaires pour un prépositionnement stratégique.
            """)

        with tab_delais:
            st.subheader("Distribution des délais d’arrivée (1er camion)")
            safe_image("delais_hist.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - La majorité des interventions sont réalisées en moins de **6 minutes**.
            - Quelques valeurs extrêmes indiquent des retards exceptionnels (embouteillages, conditions météo, incidents majeurs).
            """)

            st.subheader("Délai moyen par type d’incident")
            safe_image("delai_type.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - Les délais sont plus courts pour les **incendies** (priorité absolue).
            - Plus longs pour **Special Service** ou **False Alarm**.
            """)

    # ------------------ Mobilisations ------------------
    else:
        st.markdown("""
        Cette section se concentre sur les **mobilisations** :  
        volumes annuels, répartition horaire, délais d’intervention, et performance des casernes.
        
        **Objectif :** comprendre le rythme opérationnel et identifier les points de saturation.
        """)

        if df_mb.empty:
            st.error("Dataset mobilisations indisponible.")
            st.stop()

        col1, col2 = st.columns(2)
        col1.metric("Total mobilisations", f"{df_mb.shape[0]:,}")
        col2.metric("Nombre de casernes", f"{df_mb['StationName'].nunique()}")

        tab_vol_m, tab_heure, tab_delais_m, tab_caserne, tab_clean = st.tabs(
            ["📈 Volume annuel", "⏰ Heure d’appel", "🚒 Délais", "🏆 Casernes", "🔄 Avant/Après nettoyage"]
        )

        with tab_vol_m:
            st.subheader("Nombre de mobilisations par an")
            safe_image("mobilisationan.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - Variation similaire aux incidents, avec des hausses pendant les pics saisonniers.
            """)

        with tab_heure:
            st.subheader("Mobilisations par heure d’appel")
            safe_image("mobilisationheure.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - Deux pics majeurs : **matinée (8-10h)** et **fin d’après-midi (17-20h)**.
            - Creux prononcé la nuit.
            """)

        with tab_delais_m:
            st.subheader("Distribution des temps d’intervention")
            safe_image("intervention.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - La distribution est concentrée sous les **10 minutes**.
            - Les outliers méritent une analyse (distance, trafic, événements exceptionnels).
            """)

        with tab_caserne:
            st.subheader("Top 15 casernes les plus mobilisées")
            safe_image("mobilisationcaserne.png", use_container_width=True)
            st.markdown("""
            **Observation :**
            - Quelques casernes concentrent une forte proportion des départs.
            - Ce déséquilibre peut indiquer un besoin de rééquilibrage des ressources.
            """)

        with tab_clean:
            st.subheader("Comparaison avant / après nettoyage")
            safe_image("avantapres.jpeg", use_container_width=True)
            st.markdown("""
            **Observation :**
            - Nettoyage efficace : réduction des doublons et harmonisation des formats.
            - Impact direct sur la qualité des analyses suivantes.
            """)


# =========================================
# 4. Modélisation des séries temporelles
# =========================================

elif menu == "4. Modélisation des séries temporelles":
    st.title("📈 Modélisation des séries temporelles")

    # Choix des modèles (avant décomposition)
    st.subheader("Pourquoi SARIMA & Prophet ?")
    st.markdown("""
- **SARIMA** : adapté aux séries agrégées **mensuelles**, capture une **tendance** (*d=1*) et une **saisonnalité annuelle** (*D=1, m=12*) avec une structure parcimonieuse.
- **Prophet** : efficace au **journalier**, gère **tendance**, **saisonnalités multiples** (hebdo/annuelle) et **effets calendaires** ; robuste aux **outliers**.
""")
      # Indexation temporelle (concaténation date + heure -> datetime)
    st.subheader("🧱 Indexation temporelle")
    st.markdown("Apres l'EDA des colonnes pertinentes, nous avons créons un index `datetime` en concaténant la date et l'heure de l'appel qui déclenche une interventions, afin d'assurer un **horodatage précis** pour les modèles.")

    # ---------------------------
    # Helpers pour ADF & séries
    # ---------------------------
    def adf_test(series_np):
        """ADF avec paramètres explicites pour des résultats stables."""
        stat, pval, *_ = adfuller(
            series_np, autolag="AIC", regression="c", maxlag=None
        )
        return stat, pval

    def build_inc_daily(df_):
        """Série journalière : comptage d'incidents par jour, index continu."""
        s = (
            df_["DateOfCall"].dt.floor("D")   # jour
              .value_counts()
              .sort_index()
        )
        full_days = pd.date_range(s.index.min(), s.index.max(), freq="D")
        s = s.reindex(full_days, fill_value=0).astype("float64")
        s.index.name = "ds"
        return s

    def build_inc_monthly(df_):
        """Série mensuelle : comptage d'incidents par mois, index continu."""
        s = (
            df_["DateOfCall"].dt.to_period("M")
              .value_counts()
              .sort_index()
        )
        full_months = pd.period_range(s.index.min(), s.index.max(), freq="M")
        s = s.reindex(full_months, fill_value=0)
        s.index = s.index.to_timestamp()  # DatetimeIndex
        s = s.astype("float64")
        s.index.name = "ds"
        return s

    # ---------------------------
    # Sélecteur de granularité aligné avec ton notebook
    # ---------------------------
    st.subheader("📌 Test de stationnarité (ADF) + ACF/PACF")
    gran = st.radio(
        "Granularité analysée :", 
        ["Journalier (inc_daily)", "Mensuel (inc_monthly)"], 
        horizontal=True,
        help="Choisis la même granularité que dans le notebook pour obtenir le même ADF."
    )

    if gran.startswith("Journalier"):
        serie = build_inc_daily(df)
    else:
        serie = build_inc_monthly(df)

    # ADF aligné notebook
    adf_stat, adf_pvalue = adf_test(serie.values)
    st.markdown(f"**ADF Statistic** : {adf_stat:.4f}")
    st.markdown(f"**p-value** : {adf_pvalue:.4f}")
    if adf_pvalue < 0.05:
        st.success("✅ Stationnaire (p-value < 0.05) — une différenciation supplémentaire n'est pas requise.")
    else:
        st.info("ℹ️ Non-stationnaire (p-value ≥ 0.05) — prévoir **d=1** et **D=1 (m=12)** si mensuel.")

    # ACF / PACF (sur la série choisie)
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    plot_acf(serie, lags=50, ax=axs[0])
    plot_pacf(serie, lags=50, ax=axs[1])
    st.pyplot(fig)

    # ---------------------------
    # Décomposition (visuel)
    # ---------------------------
    st.subheader("📊 Décompositions : Additive vs Multiplicative vs STL")
    safe_image(
        "compraisonstladf.png",
        caption="decomposition_all.jpg : Additive, Multiplicative, STL (2009–2025)",
        use_container_width=True,
    )

    st.markdown("""

### 🧠 Analyse comparative
**Additive**
- Amplitude saisonnière **quasi constante**.
- Lecture claire mais **résidus plus larges** sur événements extrêmes.

**Multiplicative**
- Amplitude saisonnière **proportionnelle** au niveau (pics accentués en période haute).
- Interprétation moins directe ; dépend du niveau général.

**STL (Seasonal-Trend-Loess)**
- **Flexible** : la saisonnalité **varie** dans le temps (covid, canicules).
- **Tendance lissée** et **résidus mieux centrés** → détection d’outliers facilitée.
- **Robuste** aux chocs et aux changements structurels.
""")

    st.markdown("""
### 🔎 Interprétation des anomalies
Les pics majeurs correspondent à :
- 📌 Émeutes 2011
- 📌 Grenfell Tower 2017
- 📌 Attentats de Londres 2017
- 📌 Canicule 2022
- 📌 COVID-19 (2020)

Ces chocs **échappent** à la saisonnalité régulière et justifient une décomposition **STL** pour mieux isoler tendance/saison/résidu.


**👉 Choix retenu pour l’analyse : STL**, car **robuste** et **adaptatif** sur une longue série urbaine.
""")



# =========================================
# 5. Prédictions futures
# =========================================
elif menu == "5. Prédictions futures":
    st.title("🔮 Prévisions futures (Avril 2025 - Décembre 2028)")

    st.markdown("""
Nous confrontons **SARIMA mensuel** et **Prophet journalier (agrégé en mensuel)** :
- Une **modélisation globale** tous incidents confondus.
- Une modélisation **par groupe** (*Fire*, *False Alarm*, *Special Service*).
""")

    # Prophet journalier – jour par jour
    st.subheader("🗓️ Prévisions journalières Prophet (jour par jour)")
    safe_image(
        "prophetjourparjour.png",
        caption="prophet_daily_overall.jpg : Prévision incidents journaliers 2025–2028 avec intervalle",
        use_container_width=True,
    )
    st.markdown("""
    **Observation :**  
    - **Sur le graphe global (2009–2028)** :  
     On distingue surtout la **tendance globale** et la **saisonnalité annuelle** (pics d’été, creux hivernaux).  
    Le rythme hebdomadaire n’est pas lisible à cette échelle, car l’axe du temps est trop compressé.
    """)

    st.markdown("🔍 **Zoom sur les prévisions journalières pour les 6 prochains mois :**")
    safe_image(
        "zoomprophet.png",
        caption="prophet_daily_zoom.jpg : Zoom quotidien du 01/08/2025 au 01/01/2026",
        use_container_width=True,
    )
    st.markdown("""
    **Observation :**  
    -  Le **rythme hebdomadaire** apparaît clairement : baisse des interventions le week-end, hausse en semaine.  
    La saisonnalité annuelle reste perceptible même au jour le jour.  
    L’**incertitude** s’élargit logiquement à mesure que l’on s’éloigne dans le temps, élargissant les intervalles de confiance.
    """)

    # Prévisions mensuelles par groupe
    st.subheader("📈 Prévisions mensuelles par groupe (Avr25–Déc28)")
    safe_image(
        "sarimamensuelle.png",
        caption="monthly_by_group.jpg : SARIMAX vs Prophet pour Special Service, Fire, False Alarm",
        use_container_width=True,
    )
    st.markdown("""
    **Évaluation :**
    - *Special Service* : MAE 697.07 · RMSE 772.76 → tendance haussière récente, prévisions proches entre modèles.  
    - *Fire* : MAE 333.30 · RMSE 336.14 → pics saisonniers bien captés par les deux approches.  
    - *False Alarm* : MAE 906.34 · RMSE 936.37 → forte variabilité, plus difficile à prédire.
    """)

    # Comparaison agrégée
    st.subheader("📊 Comparaison agrégée mensuelle")
    safe_image(
        "comparaisonagreee.png",
        caption="compare_monthly.jpg : SARIMAX vs Prophet agrégé mensuel (2025–2028)",
        use_container_width=True,
    )
    st.markdown("""
    **Évaluation :**
    - MAE : 83.11 | RMSE : 103.67 | MAPE : 1.40%  
    - Les prévisions mensuelles des deux modèles sont **très proches**, écart moyen de ~1,4% seulement.
    """)

    # Erreurs absolues & cumulées
    st.subheader("📉 Erreurs absolues & cumulées")
    safe_image(
        "erreurabsoluemensuelle.png",
        caption="error_absolute.jpg : Erreur absolue mensuelle entre modèles",
        use_container_width=True,
    )
    safe_image(
        "erreurcumulé.png",
        caption="error_cumulative.jpg : Erreur cumulée (Prophet - SARIMAX)",
        use_container_width=True,
    )
    st.markdown("""
    **Observation :**
    - L’erreur absolue reste faible la plupart du temps, avec quelques divergences ponctuelles sur les pics saisonniers.  
    - L’erreur cumulée reste **modérée**, confirmant que les deux modèles convergent globalement.
    """)

    st.markdown("""
    **Synthèse :**
    - Prophet journalier excelle sur les effets calendaires fins et les variations intra-semaine.
    - SARIMA reste robuste pour des prévisions stables à l’échelle mensuelle.
    - La combinaison des deux approches offre une vision à la fois macro (mensuelle) et micro (journalière) pour la planification opérationnelle.
    """)


# =========================================
# 6. Comparaison des modèles
# =========================================
elif menu == "6. Comparaison des modèles":
    st.title("📊 Évaluation comparative SARIMAX vs Prophet")
    st.markdown("""
Nous comparons ici les performances des modèles **SARIMAX mensuel** et **Prophet journalier agrégé mensuellement** sur la période **avril 2025 – décembre 2028**.
Cette évaluation mesure la **cohérence** entre leurs prévisions mensuelles (modèle vs modèle).
""")

    # Tableau global
    df_global = pd.DataFrame({
        'Modèle 1 (Référence)': ['SARIMAX mensuel'],
        'Modèle 2': ['Prophet agrégé mensuel'],
        'MAE': [83.11],
        'RMSE': [103.67],
        'MAPE (%)': [1.40],
    })
    st.subheader("Résultats globaux")
    st.table(df_global)

    st.markdown("""
- La **MAE** (~83 incidents/mois) est **faible** au regard du volume total (~6000/mois).
- La **MAPE** (1.4 %) confirme une **excellente cohérence relative** entre les modèles.
""")

    # Tableau par groupe
    df_group = pd.DataFrame({
        'Groupe': ['Special Service', 'Fire', 'False Alarm'],
        'MAE SARIMAX': [697.07, 333.30, 906.34],
        'RMSE SARIMAX': [772.76, 336.14, 936.37],
        'MAE Prophet': [710.22, 345.11, 920.54],
        'RMSE Prophet': [790.30, 360.45, 950.12],
    })
    st.subheader("Résultats par groupe d’incidents")
    st.table(df_group)

    st.markdown("""
- Les différences de performance entre les modèles sont **faibles** (écarts marginaux).
- *False Alarm* et *Special Service* sont plus **volatils**, expliquant des erreurs plus élevées.
""")

# =========================================
# 7. Conclusion & Perspectives
# =========================================
elif menu == "7. Conclusion & Perspectives":
    st.title("✅ Conclusion & Perspectives")
    st.markdown("""
**Conclusion opérationnelle**
- **SARIMA(1,1,0)×(0,1,1)[12]** : parcimonieux, rapide à entraîner, **excellente tenue** sur l’agrégat mensuel (MAPE ≈ 1.4%).
- **Prophet journalier** : **souple** sur les effets calendaires/hebdomadaires, **réactif** aux pics ; agrégé en mensuel pour la comparaison.
- Les deux approches convergent : **cohérence des tendances** et **écarts maîtrisés** → base fiable pour la **planification**.

**Perspectives**
- **Exogènes** : intégrer météo (température, vent), jours fériés/événements majeurs, mobilité.
- **Granularité** : descendre au **borough/caserne** (modèles hiérarchiques) et **heure** (saisonnalité 24h).
- **SARIMAX / Prophet + Fourier** : enrichir la saisonnalité ; tuning via **AIC/BIC & CV temporelle**.
- **Surveillance** : suivi du **drift** + recalibrage mensuel ; alerte si **MAPE** > seuil.
- **Optimisation** : coupler prévisions à un modèle d’**affectation** (véhicules/équipes) → gains de délai & coûts.
""")
