# run_pyspark.ps1

# ➤ Définir Java 11 localement (sans modifier Windows)
$env:JAVA_HOME="C:\Users\9609241C\AppData\Local\Programs\Eclipse Adoptium\jdk-17.0.15.6-hotspot"
$env:PATH="$env:JAVA_HOME\bin;$env:PATH"

# ➤ Lancer ton script Python PySpark
python .\notebooks\Ingestion\jointure.py
