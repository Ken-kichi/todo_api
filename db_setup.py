from connect_db import ConnectDB


def create_tables(conn):
    cursor = conn.cursor()

    # テーブル削除（存在する場合）
    cursor.execute("DROP TABLE IF EXISTS tasks;")
    cursor.execute("DROP TABLE IF EXISTS users;")
    print("Finished dropping tables (if existed)")

    # タイムゾーンの設定
    cursor.execute("SET timezone TO 'Asia/Tokyo';")

    # ユーザーテーブル作成
    cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            is_manager BOOLEAN DEFAULT FALSE,
            disabled BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # タスクテーブル作成（users.id を参照する外部キー付き）
    cursor.execute("""
        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 仮のユーザーを追加（task挿入用）
    cursor.execute("""
        INSERT INTO users (username, full_name, email, hashed_password,is_manager)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """, ("testuser", "test user", "test@example.com", "hashedpassword123", True))

    user_id = cursor.fetchone()[0]

    # タスクデータを挿入
    sample_tasks = [
        ("ABCD", "食事に行く", False),
        ("EFGH", "料理を作る", False),
        ("IJKL", "買い物をする", False),
    ]

    for title, desc, completed in sample_tasks:
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, completed)
            VALUES (%s, %s, %s, %s);
        """, (user_id, title, desc, completed))

    conn.commit()
    cursor.close()
    conn.close()


def main():
    try:
        connect_db = ConnectDB()
        conn = connect_db.get_connection()
        create_tables(conn)
        print("created database")
    except Exception as e:
        print(f"Error:{e}")


if __name__ == "__main__":
    main()
