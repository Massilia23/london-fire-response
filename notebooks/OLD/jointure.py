
# In[9]:
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_extract, min as spark_min, max as spark_max
import os

# 1. Initialisation Spark
try:
    spark.stop()
except:
    pass

spark = SparkSession.builder \
    .appName("Jointure Incidents & Mobilisations") \
    .master("local[*]") \
    .getOrCreate()

print("SparkSession initialisée.")

# 2. Chemins des fichiers
incident_path = "data/raw/Cleaned_data/InUSE/cleaned_data_incidents.csv"
mobilisation_path = "data/raw/Cleaned_data/InUSE/cleaned_data_mobilisations.csv"

# 3. Vérification des chemins
assert os.path.exists(incident_path), f"❌ Fichier introuvable : {incident_path}"
assert os.path.exists(mobilisation_path), f"❌ Fichier introuvable : {mobilisation_path}"

# 4. Chargement des données
df_incidents = spark.read.option("header", True).option("inferSchema", True).csv(incident_path)
df_mobilisations = spark.read.option("header", True).option("inferSchema", True).csv(mobilisation_path)
print("Données chargées avec succès.")

# 5. Aperçu
print("Incidents :")
df_incidents.show(3, truncate=False)
print("Mobilisations :")
df_mobilisations.show(3, truncate=False)

# 6. Période de données
print("Période des incidents :")
df_incidents.select(spark_min("CalYear"), spark_max("CalYear")).show()
print("Période des mobilisations :")
df_mobilisations.select(spark_min("CalYear"), spark_max("CalYear")).show()

# 7. Nettoyage des identifiants incidents
def clean_incident_number(col_):
    return when(col_.contains('.'), regexp_extract(col_, r"^([^\.]+)", 1)) \
    .when(col_.contains('-'), regexp_extract(col_, r"^([^-]+)", 1)) \
    .otherwise(col_)

df_incidents_clean = df_incidents.withColumn("incident_id_cleaned", clean_incident_number(col("IncidentNumber")))
df_mobilisations_clean = df_mobilisations.withColumn("incident_id_cleaned", clean_incident_number(col("IncidentNumber")))

# 8. Dédupliquer les incidents (1 ligne par incident)
df_incidents_unique = df_incidents_clean.dropDuplicates(["incident_id_cleaned"])
print(f"🔢 Incidents uniques : {df_incidents_unique.count():,}")

# 9. Jointure
df_joined = df_mobilisations_clean.join(df_incidents_unique, on="incident_id_cleaned", how="inner")

# 10. Statistiques
nb_incidents = df_incidents.count()
nb_mobilisations = df_mobilisations.count()
nb_jointure = df_joined.count()
nb_incidents_uniques = df_incidents_unique.count()

print(f"Incidents (original) : {nb_incidents:,}")
print(f"Incidents uniques : {nb_incidents_uniques:,}")
print(f"Mobilisations : {nb_mobilisations:,}")
print(f"Lignes jointes : {nb_jointure:,}")
print(f"Taux de jointure : {nb_jointure / nb_mobilisations:.2%}")

# 11. Mobilisations sans correspondance
df_unmatched = df_mobilisations_clean.join(df_incidents_unique, on="incident_id_cleaned", how="left_anti")
print(f"Mobilisations non jointes : {df_unmatched.count():,}")

# 12. Aperçu final
print("Aperçu jointure :")
df_joined.show(5, truncate=False)

# 13. Fin de session
spark.stop()
print("SparkSession terminée.")
