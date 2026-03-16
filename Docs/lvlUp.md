# Gone from streamlit baby ui to react next is below proper directory structure

episteme/
├── .github/
│   ├── workflows/
│   │   ├── backend-ci.yml
│   │   ├── frontend-ci.yml
│   │   └── deploy.yml
│   └── CODEOWNERS
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── predict.py
│   │   │   │   ├── compare.py
│   │   │   │   ├── metrics.py
│   │   │   │   ├── datasets.py
│   │   │   │   └── socratic.py
│   │   │   └── middleware/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── logging.py
│   │   │       └── rate_limit.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── exceptions.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── trainer.py
│   │   │   ├── linear.py
│   │   │   ├── random_forest.py
│   │   │   └── xgboost_model.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── dataset_service.py
│   │   │   ├── prediction_service.py
│   │   │   └── metrics_service.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   ├── validators.py
│   │   │   └── helpers.py
│   │   └── main.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api/
│   │   ├── test_models/
│   │   └── test_services/
│   ├── logs/
│   │   ├── error/
│   │   ├── access/
│   │   └── model/
│   ├── scripts/
│   │   ├── init_db.py
│   │   └── seed_data.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   ├── prod.txt
│   │   └── test.txt
│   ├── .env.example
│   ├── .env.test
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── pyproject.toml
├── frontend/
│   ├── public/
│   │   ├── favicon.
