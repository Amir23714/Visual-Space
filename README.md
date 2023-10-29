# Visual Space

**Backend for Visual Space startup.** 
The goal of this project was to write a backend on the FastAPI framework for the Visual Space startup web application

## Installation 
To install and set up the project, follow these steps:

1. Make sure that python is installed on your computer

2. Clone the repository:
```bash
git clone https://github.com/Amir23714/Visual-Space.git
```

3. Navigate to the project directory:
```bash
cd Visual-Space
```

4. Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
5. Create .env file with all neccessary variables.
Here is the exaple with suitable values

```bash
SECRET_KEY = secret_key228
ALGORITHM = HS256
API_LINK = https://api.agify.io?name=meelad

EMAIL_SENDER = VisualSpaceOfficial@yandex.ru
EMAIL_PASSWORD = lyour_password
CODE_EXPIRATION_TIME = 900
```

### Alembic configuration
6. Initialize alembic migrations

```bash
alembic init migrations
```

7. In file alembic.ini update value of variable **sqlalchemy.url** to your url to database
here is the example with sqlite DB configuration:

```bash
sqlalchemy.url = sqlite:///test.db
```

9. In file migrations/env.py update row **target_metadata = None** with:
```bash
from models.models import Base
target_metadata = Base.metadata
```

9. Run
```bash
alembic revision --autogenerate
alembic upgrade head
```

10. Start the server using the following command:
```bash
uvicorn main:app --reload
```

11. Run the celery:
```bash
celery -A Authentification.emailUtils:celery worker --loglevel=INFO
```

12. Run flower (if you want to have GUI for celery):
```bash
celery -A Authentification.emailUtils:celery flower
```

