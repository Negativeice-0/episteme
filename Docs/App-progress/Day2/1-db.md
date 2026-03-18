# db setup is in code so pyhton hadled it

THis downloaded the data -- python scripts/load_datasets.py

(venv) lsetga@lsetga:~/Projects/episteme/backend$ python scripts/load_datasets.py

==================================================

📥 LOADING DATASETS INTO POSTGRESQL

==================================================
📊 Loading Boston Housing dataset...
INFO 2026-03-18 13:44:11,514 _california_housing 349058 140698440843392 Downloading Cal. housing from ```https://ndownloader.figshare.com/files/5976036 to /``` home/lsetga/scikit_learn_data
  Created dataset with 20640 samples
📊 Creating Education vs Income dataset...
  Created dataset with 500 samples
📊 Creating Salary Prediction dataset...
  Created dataset with 800 samples

==================================================

✅ All datasets loaded successfully!
📊 Total datasets: 3

==================================================

Training models lead to some imaginary stats.

python scripts/train_models.py
