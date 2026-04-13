-- Создание таблицы категорий
CREATE TABLE IF NOT EXISTS категория (
    id SERIAL PRIMARY KEY,
    название TEXT NOT NULL,
    родитель_id INTEGER REFERENCES категория(id)
);

-- Создание таблицы марок
CREATE TABLE IF NOT EXISTS марка (
    id_марка SERIAL PRIMARY KEY,
    марка TEXT NOT NULL
);

-- Создание таблицы продуктов
CREATE TABLE IF NOT EXISTS продукт (
    id_продукт SERIAL PRIMARY KEY,
    название TEXT NOT NULL,
    цена NUMERIC(10,2),
    ед_измерения TEXT,
    состояние TEXT,
    id_марка INTEGER REFERENCES марка(id_марка),
    id_категория INTEGER REFERENCES категория(id)
);
