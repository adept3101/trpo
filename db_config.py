import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

conn = psycopg2.connect(
    dbname=dbname, host=host, user=user, password=password, port=port
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Client(
        client_id INT PRIMARY KEY,
        name TEXT,
        lastname TEXT,
        phone TEXT,
        email TEXT,
        registr_data TEXT);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Product(
        product_id INT PRIMARY KEY,
        product_name TEXT,
        description TEXT,
        rate TEXT,
        term TEXT);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Client_product(
        client_id INT,
        product_id INT,
        PRIMARY KEY(client_id, product_id),
        FOREIGN KEY (client_id) REFERENCES Client (client_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product (product_id) ON DELETE CASCADE,
        start_date DATE,
        end_date DATE,
        status TEXT);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employee(
        employee_id INT PRIMARY KEY,
        full_name TEXT,
        position TEXT,
        hire_date DATE);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passport(
        passport_id INT PRIMARY KEY,
        client_id INT,
        series TEXT,
        number TEXT,
        iss_date DATE,
        FOREIGN KEY (client_id) REFERENCES Client (client_id) ON DELETE CASCADE);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Account(
        account_id INT PRIMARY KEY,
        client_id INT,
        numver_acc INT,
        balance INT,
        currency TEXT,
        open_data TEXT,
        FOREIGN KEY (client_id) REFERENCES Client (client_id) ON  DELETE CASCADE);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Application(
        application_id INT PRIMARY KEY,
        client_id INT,
        product_id INT,
        employee_id INT,
        status TEXT,
        application_data TEXT,
        FOREIGN KEY (client_id) REFERENCES Client (client_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product (product_id) ON DELETE CASCADE,
        FOREIGN KEY (employee_id) REFERENCES Employee (employee_id) ON DELETE CASCADE);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS TRANSACTION(
        transaction_id INT PRIMARY KEY,
        account_id INT,
        amount INT,
        transaction_data TEXT,
        type TEXT,
        FOREIGN KEY (account_id) REFERENCES Account (account_id) ON DELETE CASCADE);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Account_product(
        account_id INT,
        product_id INT,
        data_connect TEXT,
        status TEXT,
        PRIMARY KEY (account_id),
        FOREIGN KEY (account_id) REFERENCES Account (account_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product (product_id) ON DELETE CASCADE);
""")

cursor.execute("""
    INSERT INTO Client (client_id, name, lastname, phone, email, registr_data)
    VALUES 
    (1, 'Иван', 'Иванов', '89001234567', 'ivanov@mail.ru', '2024-01-15'),
    (2, 'Петр', 'Петров', '89093602325', 'petrov@mail.ru', '2024-02-20'),
    (3, 'Мария', 'Сидорова', '89161234567', 'sidorova@gmail.com', '2024-03-10'),
    (4, 'Анна', 'Кузнецова', '89037654321', 'kuznetsova@yandex.ru', '2024-04-05'),
    (5, 'Сергей', 'Смирнов', '89059876543', 'smirnov@mail.ru', '2024-05-12');
""")

cursor.execute("""
    INSERT INTO Product (product_id, product_name, description, rate, term)
    VALUES 
    (1, 'Дебетовая карта', 'Основная расчетная карта', '0%', 'Бессрочно'),
    (2, 'Кредитная карта', 'Кредитный лимит до 300000 руб', '15.9%', '3 года'),
    (3, 'Вклад "Накопительный"', 'Накопительный счет с капитализацией', '8.5%', '1 год'),
    (4, 'Ипотека', 'Ипотечное кредитование', '7.9%', '20 лет'),
    (5, 'Потребительский кредит', 'Кредит на любые цели', '12.5%', '5 лет');
""")

cursor.execute("""
    INSERT INTO Employee (employee_id, full_name, position, hire_date)
    VALUES 
    (1, 'Ольга Николаевна Иванова', 'Менеджер', '2020-01-10'),
    (2, 'Алексей Владимирович Петров', 'Старший менеджер', '2018-05-15'),
    (3, 'Екатерина Сергеевна Сидорова', 'Кредитный специалист', '2021-03-20'),
    (4, 'Дмитрий Александрович Козлов', 'Операционист', '2019-11-08'),
    (5, 'Наталья Игоревна Морозова', 'Руководитель отдела', '2017-02-14');
""")

cursor.execute("""
    INSERT INTO Passport (passport_id, client_id, series, number, iss_date)
    VALUES 
    (1, 1, '4510', '123456', '2015-06-15'),
    (2, 2, '4511', '654321', '2016-03-20'),
    (3, 3, '4512', '789012', '2017-01-10'),
    (4, 4, '4513', '345678', '2018-09-05'),
    (5, 5, '4514', '901234', '2019-12-18');
""")

cursor.execute("""
    INSERT INTO Account (account_id, client_id, numver_acc, balance, currency, open_data)
    VALUES 
    (1, 1, 100001, 50000, 'RUB', '2024-01-15'),
    (2, 2, 100002, 125000, 'RUB', '2024-02-20'),
    (3, 3, 100003, 78000, 'RUB', '2024-03-10'),
    (4, 4, 100004, 230000, 'RUB', '2024-04-05'),
    (5, 5, 100005, 45000, 'RUB', '2024-05-12');
""")

cursor.execute("""
    INSERT INTO Application (application_id, client_id, product_id, employee_id, status, application_data)
    VALUES 
    (1, 1, 1, 1, 'Одобрена', '2024-01-16'),
    (2, 2, 2, 2, 'На рассмотрении', '2024-02-21'),
    (3, 3, 3, 3, 'Одобрена', '2024-03-11'),
    (4, 4, 4, 4, 'Отклонена', '2024-04-06'),
    (5, 5, 5, 5, 'Одобрена', '2024-05-13');
""")

cursor.execute("""
    INSERT INTO Client_product (client_id, product_id, start_date, end_date, status)
    VALUES 
    (1, 1, '2024-01-16', '2027-01-16', 'Активен'),
    (2, 2, '2024-02-22', '2027-02-22', 'Активен'),
    (3, 3, '2024-03-12', '2025-03-12', 'Активен'),
    (4, 1, '2024-04-07', '2027-04-07', 'Активен'),
    (5, 5, '2024-05-14', '2029-05-14', 'Активен');
""")

cursor.execute("""
    INSERT INTO TRANSACTION (transaction_id, account_id, amount, transaction_data, type)
    VALUES 
    (1, 1, 5000, '2024-01-17', 'Пополнение'),
    (2, 2, -10000, '2024-02-23', 'Списание'),
    (3, 3, 20000, '2024-03-13', 'Пополнение'),
    (4, 4, -5000, '2024-04-08', 'Списание'),
    (5, 5, 15000, '2024-05-15', 'Пополнение');
""")

cursor.execute("""
    INSERT INTO Account_product (account_id, product_id, data_connect, status)
    VALUES 
    (1, 1, '2024-01-16', 'Активна'),
    (2, 2, '2024-02-22', 'Активна'),
    (3, 3, '2024-03-12', 'Активна'),
    (4, 1, '2024-04-07', 'Активна'),
    (5, 5, '2024-05-14', 'Активна');
""")

conn.commit()


cursor.close()
conn.close()
