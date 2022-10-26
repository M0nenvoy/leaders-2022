"""
Различные константы, требуемые для работы программы,
собранные в одном месте.
"""

import os

# Корень проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Путь к папке ресурсов проекта
RESOURCE_DIR = PROJECT_ROOT + "/resource"

# Информация, необходимая для соединения с базой данных
DATABASE_URL = "postgresql://root:root@192.168.0.104:5432/db"