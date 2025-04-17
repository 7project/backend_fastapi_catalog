

### START PROJECT BACKEND FASTAPI CATALOG  

![alt text](Catalog_FastAPI.jpg) 

1. uv init
2. update gitignore file
3. git init and first commit
4. rename branch master to main for github
5. Создание репозитория и монтирования его на github
6. Добавление зависимостей в pyproject.toml и синхронизация пакетов
7. Добавление папок\файлов для архитектуры DDD проекта
8. Настройка Alembic
9. Подключение к базе данных
10. Создание первого миграционного скрипта
11. Добавление миграций в проект
12. Настройка FastAPI окружения
13. Создание моделей и репозиториев
14. Создание слоев приложения
15. Создание схемы базы данных
16. Создание сущности продукта
17. Создание сущности свойства продукта
18. Создание сервиса продукта
19. Старт проекта
20. Создание скрипта для подключения к базе данных и создания миграционного скрипта
21. Оформление

### Одна команда для запуска
#### Подготовка

Перед запуском склонировать репозиторий:

```bash
git clone https://github.com/7project/backend_fastapi_catalog.git
```

Создать файл .env в корне проекта:

```bash
DB_HOST=...
DB_PORT=...
DB_USER=...
DB_PASSWORD=...
DB_NAME=...

DATABASE_URL=postgresql+asyncpg://...
```

Запуск:

```bash
docker-compose up --build
```
