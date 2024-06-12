import psycopg2
from faker import Faker
import random

# Підключення до бази даних
def create_connection():
    return psycopg2.connect(
        database="postgres",
        user="postgres",
        password="567234",  # Ваш пароль
        host="localhost",
        port="5438"  # Ваш порт
    )

# Функція для створення таблиць
def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""


        CREATE TABLE IF NOT EXISTS groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            group_id INTEGER REFERENCES groups(id)
        );

        CREATE TABLE IF NOT EXISTS teachers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS subjects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(180) NOT NULL,
            teacher_id INTEGER REFERENCES teachers(id)
        );

        CREATE TABLE IF NOT EXISTS grades (
            id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(id),
            subject_id INTEGER REFERENCES subjects(id),
            grade INTEGER CHECK (grade >= 0 AND grade <= 100),
            grade_date DATE NOT NULL
        );
        """)
        conn.commit()

# Функція для наповнення бази даних
def populate_db(conn):
    fake = Faker()
    with conn.cursor() as cur:
        # Додавання груп
        for _ in range(3):
            cur.execute("INSERT INTO groups (name) VALUES (%s)", (fake.word(),))

        # Додавання викладачів
        for _ in range(5):
            cur.execute("INSERT INTO teachers (name) VALUES (%s)", (fake.name(),))

        # Додавання предметів
        cur.execute("SELECT id FROM teachers")
        teacher_ids = [row[0] for row in cur.fetchall()]
        for _ in range(8):
            cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s)",
                        (fake.word(), random.choice(teacher_ids)))

        # Додавання студентів
        cur.execute("SELECT id FROM groups")
        group_ids = [row[0] for row in cur.fetchall()]
        for _ in range(50):
            cur.execute("INSERT INTO students (name, email, group_id) VALUES (%s, %s, %s)",
                        (fake.name(), fake.email(), random.choice(group_ids)))

        # Додавання оцінок
        cur.execute("SELECT id FROM students")
        student_ids = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT id FROM subjects")
        subject_ids = [row[0] for row in cur.fetchall()]
        for student_id in student_ids:
            for subject_id in subject_ids:
                cur.execute("INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)",
                            (student_id, subject_id, random.randint(0, 100), fake.date()))

        conn.commit()

# Основна програма
def main():
    conn = create_connection()
    create_tables(conn)
    populate_db(conn)
    conn.close()

if __name__ == "__main__":
    main()

