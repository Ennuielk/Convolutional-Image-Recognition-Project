import sqlite3

def create_database():
    """创建数据库和表"""
    conn = sqlite3.connect('fruit.db')
    cursor = conn.cursor()

    # 创建水果表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fruits (
        name TEXT UNIQUE NOT NULL,
        calories REAL,
        carbohydrates REAL,
        protein REAL,
        fat REAL,
        fiber REAL
    )
    ''')

    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_emp_name ON fruits(name)')

    conn.commit()
    conn.close()
    print("数据库和表创建完成")


def insert_fruit_data(fruit_dict):
    """将水果营养字典数据插入数据库"""
    conn = sqlite3.connect('fruit.db')
    cursor = conn.cursor()

    try:
        # 使用executemany批量插入
        data_to_insert = []
        for fruit_name, nutrition in fruit_dict.items():
            data = {
                'name': fruit_name,
                'calories': nutrition['calories'],
                'carbohydrates': nutrition['carbohydrates'],
                'protein': nutrition['protein'],
                'fat': nutrition['fat'],
                'fiber': nutrition['fiber']
            }
            data_to_insert.append(data)

        # 使用ON CONFLICT IGNORE避免重复插入
        cursor.executemany('''
        INSERT INTO fruits (name, calories, carbohydrates, protein, fat, fiber)
        VALUES (:name, :calories, :carbohydrates, :protein, :fat, :fiber)
        ''', data_to_insert)

        conn.commit()
        print(f"成功插入/更新 {cursor.rowcount} 条记录")
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        conn.rollback()
    finally:
        conn.close()

fruit_nutrition = {
    "oil_palm": {"calories": 884, "carbohydrates": 0, "protein": 0, "fat": 100, "fiber": 0},
    "hog_plum": {"calories": 46, "carbohydrates": 11.4, "protein": 0.5, "fat": 0.3, "fiber": 2.4},
    "apricot": {"calories": 48, "carbohydrates": 11, "protein": 1.4, "fat": 0.4, "fiber": 2},
    "sugar_apple": {"calories": 94, "carbohydrates": 23.6, "protein": 2.1, "fat": 0.3, "fiber": 4.4},
    "rambutan": {"calories": 68, "carbohydrates": 16, "protein": 0.9, "fat": 0.2, "fiber": 2.8},
    "yellow_plum": {"calories": 46, "carbohydrates": 11.4, "protein": 0.7, "fat": 0.3, "fiber": 1.4},
    "pineapple": {"calories": 50, "carbohydrates": 13.1, "protein": 0.5, "fat": 0.1, "fiber": 1.4},
    "dewberry": {"calories": 43, "carbohydrates": 9.6, "protein": 1.4, "fat": 0.5, "fiber": 5.3},
    "plumcot": {"calories": 46, "carbohydrates": 11.4, "protein": 0.7, "fat": 0.3, "fiber": 1.4},
    "ambarella": {"calories": 46, "carbohydrates": 11.8, "protein": 0.5, "fat": 0.3, "fiber": 3.6},
    "grenadilla": {"calories": 97, "carbohydrates": 23.4, "protein": 2.2, "fat": 0.7, "fiber": 10.4},
    "elderberry": {"calories": 73, "carbohydrates": 18.4, "protein": 0.7, "fat": 0.5, "fiber": 7},
    "barbadine": {"calories": 97, "carbohydrates": 23.4, "protein": 2.2, "fat": 0.7, "fiber": 10.4},
    "horned_melon": {"calories": 44, "carbohydrates": 8.6, "protein": 1.8, "fat": 1.3, "fiber": 3.7},
    "chico": {"calories": 83, "carbohydrates": 20, "protein": 0.4, "fat": 1.1, "fiber": 5.3},
    "mock_strawberry": {"calories": 32, "carbohydrates": 7.7, "protein": 0.7, "fat": 0.3, "fiber": 2},
    "cashew": {"calories": 553, "carbohydrates": 30.2, "protein": 18.2, "fat": 43.9, "fiber": 3.3},
    "finger_lime": {"calories": 30, "carbohydrates": 7.7, "protein": 0.7, "fat": 0.2, "fiber": 2.8},
    "apple": {"calories": 52, "carbohydrates": 14, "protein": 0.3, "fat": 0.2, "fiber": 2.4},
    "eggplant": {"calories": 25, "carbohydrates": 5.9, "protein": 1, "fat": 0.2, "fiber": 3},
    "pawpaw": {"calories": 80, "carbohydrates": 19, "protein": 1.2, "fat": 1.2, "fiber": 2.6},
    "chokeberry": {"calories": 47, "carbohydrates": 9.6, "protein": 1.4, "fat": 0.5, "fiber": 5.3},
    "jamaica_cherry": {"calories": 56, "carbohydrates": 14, "protein": 0.7, "fat": 0.4, "fiber": 1.8},
    "grapefruit": {"calories": 42, "carbohydrates": 10.7, "protein": 0.8, "fat": 0.1, "fiber": 1.6},
    "santol": {"calories": 43, "carbohydrates": 11.4, "protein": 0.5, "fat": 0.3, "fiber": 3.6},
    "chenet": {"calories": 94, "carbohydrates": 23.6, "protein": 2.1, "fat": 0.3, "fiber": 4.4},
    "salak": {"calories": 82, "carbohydrates": 21.3, "protein": 0.4, "fat": 0.4, "fiber": 3.9},
    "indian_strawberry": {"calories": 32, "carbohydrates": 7.7, "protein": 0.7, "fat": 0.3, "fiber": 2},
    "cherimoya": {"calories": 75, "carbohydrates": 18, "protein": 1.6, "fat": 0.7, "fiber": 3},
    "otaheite_apple": {"calories": 46, "carbohydrates": 11.8, "protein": 0.5, "fat": 0.3, "fiber": 3.6},
    "dragonfruit": {"calories": 60, "carbohydrates": 13, "protein": 1.2, "fat": 0, "fiber": 3},
    "raspberry": {"calories": 52, "carbohydrates": 11.9, "protein": 1.2, "fat": 0.7, "fiber": 6.5},
    "mangosteen": {"calories": 73, "carbohydrates": 17.9, "protein": 0.4, "fat": 0.6, "fiber": 1.8},
    "yali_pear": {"calories": 42, "carbohydrates": 10.7, "protein": 0.4, "fat": 0.1, "fiber": 3.1},
    "taxus_baccata": {"calories": 0, "carbohydrates": 0, "protein": 0, "fat": 0, "fiber": 0},  # 注意：有毒不可食用
    "coconut": {"calories": 354, "carbohydrates": 15.2, "protein": 3.3, "fat": 33.5, "fiber": 9},
    "guava": {"calories": 68, "carbohydrates": 14.3, "protein": 2.6, "fat": 1, "fiber": 5.4},
    "black_mulberry": {"calories": 43, "carbohydrates": 9.8, "protein": 1.4, "fat": 0.4, "fiber": 1.7},
    "durian": {"calories": 147, "carbohydrates": 27.1, "protein": 1.5, "fat": 5.3, "fiber": 3.8},
    "ackee": {"calories": 151, "carbohydrates": 0.8, "protein": 2.9, "fat": 15.2, "fiber": 2.7},
    "olive": {"calories": 115, "carbohydrates": 6, "protein": 0.8, "fat": 10.7, "fiber": 3.2},
    "mandarine": {"calories": 53, "carbohydrates": 13.3, "protein": 0.8, "fat": 0.3, "fiber": 1.8},
    "blackberry": {"calories": 43, "carbohydrates": 9.6, "protein": 1.4, "fat": 0.5, "fiber": 5.3},
    "acerola": {"calories": 32, "carbohydrates": 7.7, "protein": 0.4, "fat": 0.3, "fiber": 1.1},
    "jaboticaba": {"calories": 58, "carbohydrates": 15.3, "protein": 0.6, "fat": 0.2, "fiber": 2.3},
    "fig": {"calories": 74, "carbohydrates": 19.2, "protein": 0.8, "fat": 0.3, "fiber": 2.9},
    "langsat": {"calories": 57, "carbohydrates": 14.3, "protein": 0.9, "fat": 0.1, "fiber": 1.4},
    "redcurrant": {"calories": 56, "carbohydrates": 13.8, "protein": 1.4, "fat": 0.2, "fiber": 4.3},
    "gooseberry": {"calories": 44, "carbohydrates": 10.2, "protein": 0.9, "fat": 0.6, "fiber": 4.3},
    "camu_camu": {"calories": 26, "carbohydrates": 6.3, "protein": 0.4, "fat": 0.2, "fiber": 1.1},
    "barberry": {"calories": 316, "carbohydrates": 63.9, "protein": 3.6, "fat": 3.9, "fiber": 7.4},
    "rose_hip": {"calories": 162, "carbohydrates": 38.2, "protein": 1.6, "fat": 0.3, "fiber": 24.1},
    "jalapeno": {"calories": 29, "carbohydrates": 6.5, "protein": 0.9, "fat": 0.4, "fiber": 2.8},
    "brazil_nut": {"calories": 659, "carbohydrates": 11.7, "protein": 14.3, "fat": 67.1, "fiber": 7.5},
    "damson": {"calories": 46, "carbohydrates": 11.4, "protein": 0.7, "fat": 0.3, "fiber": 1.4},
    "acai": {"calories": 70, "carbohydrates": 4, "protein": 1, "fat": 5, "fiber": 3},
    "prickly_pear": {"calories": 41, "carbohydrates": 9.6, "protein": 0.7, "fat": 0.5, "fiber": 3.6},
    "morinda": {"calories": 43, "carbohydrates": 10.2, "protein": 0.4, "fat": 0.2, "fiber": 1.2},
    "sea_buckthorn": {"calories": 82, "carbohydrates": 12.2, "protein": 1.7, "fat": 2.7, "fiber": 4.7},
    "avocado": {"calories": 160, "carbohydrates": 8.5, "protein": 2, "fat": 14.7, "fiber": 6.7},
    "strawberry_guava": {"calories": 68, "carbohydrates": 14.3, "protein": 2.6, "fat": 1, "fiber": 5.4},
    "jackfruit": {"calories": 95, "carbohydrates": 23.2, "protein": 1.7, "fat": 0.6, "fiber": 1.5},
    "greengage": {"calories": 46, "carbohydrates": 11.4, "protein": 0.7, "fat": 0.3, "fiber": 1.4},
    "cupuacu": {"calories": 72, "carbohydrates": 15.3, "protein": 1.2, "fat": 1.1, "fiber": 3.3},
    "longan": {"calories": 60, "carbohydrates": 15.1, "protein": 1.3, "fat": 0.1, "fiber": 1.1},
    "passion_fruit": {"calories": 97, "carbohydrates": 23.4, "protein": 2.2, "fat": 0.7, "fiber": 10.4},
    "feijoa": {"calories": 55, "carbohydrates": 13, "protein": 0.6, "fat": 0.4, "fiber": 6.4},
    "betel_nut": {"calories": 330, "carbohydrates": 6.1, "protein": 3.9, "fat": 15.4, "fiber": 9.2},
    "kaffir_lime": {"calories": 30, "carbohydrates": 7.7, "protein": 0.7, "fat": 0.2, "fiber": 2.8},
    "sapodilla": {"calories": 83, "carbohydrates": 20, "protein": 0.4, "fat": 1.1, "fiber": 5.3},
    "cempedak": {"calories": 117, "carbohydrates": 28.6, "protein": 2.5, "fat": 0.4, "fiber": 3.5},
    "hawthorn": {"calories": 52, "carbohydrates": 14, "protein": 0.8, "fat": 0.2, "fiber": 3.6},
    "mango": {"calories": 60, "carbohydrates": 15, "protein": 0.8, "fat": 0.4, "fiber": 1.6},
    "malay_apple": {"calories": 46, "carbohydrates": 11.8, "protein": 0.5, "fat": 0.3, "fiber": 3.6},
    "cranberry": {"calories": 46, "carbohydrates": 12.2, "protein": 0.4, "fat": 0.1, "fiber": 4.6},
    "jocote": {"calories": 46, "carbohydrates": 11.8, "protein": 0.5, "fat": 0.3, "fiber": 3.6},
    "cluster_fig": {"calories": 74, "carbohydrates": 19.2, "protein": 0.8, "fat": 0.3, "fiber": 2.9},
    "corn_kernel": {"calories": 86, "carbohydrates": 19, "protein": 3.2, "fat": 1.2, "fiber": 2.7},
    "kumquat": {"calories": 71, "carbohydrates": 15.9, "protein": 1.9, "fat": 0.9, "fiber": 6.5},
    "rose_leaf_bramble": {"calories": 52, "carbohydrates": 11.9, "protein": 1.2, "fat": 0.7, "fiber": 6.5},
    "jujube": {"calories": 79, "carbohydrates": 20.2, "protein": 1.2, "fat": 0.2, "fiber": 0.6},
    "grape": {"calories": 69, "carbohydrates": 18.1, "protein": 0.7, "fat": 0.2, "fiber": 0.9},
    "pea": {"calories": 81, "carbohydrates": 14.5, "protein": 5.4, "fat": 0.4, "fiber": 5.1},
    "papaya": {"calories": 43, "carbohydrates": 11, "protein": 0.5, "fat": 0.4, "fiber": 1.7},
    "bitter_gourd": {"calories": 17, "carbohydrates": 3.7, "protein": 1, "fat": 0.2, "fiber": 2.8},
    "ugli_fruit": {"calories": 45, "carbohydrates": 11.2, "protein": 0.8, "fat": 0.2, "fiber": 1.9},
    "jambul": {"calories": 60, "carbohydrates": 15.6, "protein": 0.7, "fat": 0.2, "fiber": 0.6},
    "mabolo": {"calories": 67, "carbohydrates": 17, "protein": 0.5, "fat": 0.4, "fiber": 2.5},
    "abiu": {"calories": 140, "carbohydrates": 36, "protein": 1.4, "fat": 0.4, "fiber": 0.8},
    "quince": {"calories": 57, "carbohydrates": 15.3, "protein": 0.4, "fat": 0.1, "fiber": 1.9},
    "custard_apple": {"calories": 101, "carbohydrates": 25.2, "protein": 1.7, "fat": 0.6, "fiber": 2.4},
    "medlar": {"calories": 60, "carbohydrates": 16, "protein": 0.4, "fat": 0.2, "fiber": 1.7},
    "mountain_soursop": {"calories": 66, "carbohydrates": 16.8, "protein": 1, "fat": 0.3, "fiber": 3.3},
    "banana": {"calories": 89, "carbohydrates": 22.8, "protein": 1.1, "fat": 0.3, "fiber": 2.6},
    "goumi": {"calories": 52, "carbohydrates": 11.9, "protein": 1.2, "fat": 0.7, "fiber": 6.5},
    "hard_kiwi": {"calories": 61, "carbohydrates": 14.7, "protein": 1.1, "fat": 0.5, "fiber": 3},
    "pomegranate": {"calories": 83, "carbohydrates": 18.7, "protein": 1.7, "fat": 1.2, "fiber": 4},
    "white_currant": {"calories": 56, "carbohydrates": 13.8, "protein": 1.4, "fat": 0.2, "fiber": 4.3},
    "lablab": {"calories": 343, "carbohydrates": 60.7, "protein": 24.6, "fat": 1.7, "fiber": 25.3},
    "emblic": {"calories": 44, "carbohydrates": 10.2, "protein": 0.4, "fat": 0.2, "fiber": 1.2}
}

if __name__ == "__main__":
    # 创建数据库和表
    create_database()

    # 插入水果营养数据
    insert_fruit_data(fruit_nutrition)

    # 验证数据插入
    conn = sqlite3.connect('fruit.db')
    conn.row_factory = sqlite3.Row  # 返回字典形式的结果
    cursor = conn.cursor()

    conn.close()
