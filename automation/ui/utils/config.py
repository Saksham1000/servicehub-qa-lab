import os
BASE_URL=os.getenv('BASE_URL','http://localhost:5173')
HEADLESS=os.getenv('HEADLESS','true').lower()=='true'
