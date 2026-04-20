import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "data.json"

# ---------------- UI ----------------
st.set_page_config(
    page_title="Fitness Tracker Pro",
    page_icon="🏋️‍♂️",
    layout="centered"
)

st.markdown("""
<style>
body {background-color:#0f172a;}
h1,h2,h3 {color:#38bdf8;}

.card {
    background:#1e293b;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
    color:white;
    box-shadow:0 0 10px rgba(56,189,248,0.2);
}

.stButton button {
    background:#38bdf8;
    color:black;
    border-radius:10px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_record(t, v, c, h, w):
    data = load_data()
    data.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": t,
        "value": v,
        "comment": c,
        "height": h,
        "weight": w
    })
    save_data(data)

# ---------------- MENU ----------------
menu = st.sidebar.radio(
    "📌 Меню",
    ["🏠 Дашборд", "➕ Добавить", "🧠 AI Коуч", "🏆 Прогресс", "🥗 Питание"]
)

data = load_data()

# ---------------- DASHBOARD ----------------
if menu == "🏠 Дашборд":
    st.title("🏋️ Fitness Tracker Pro")

    water = sum(i["value"] for i in data if "Вода" in i["type"])
    workouts = len([i for i in data if "Тренировка" in i["type"]])
    weights = [i["value"] for i in data if "Вес" in i["type"]]

    last_weight = weights[-1] if weights else None

    st.markdown(f"""
    <div class="card">
    💧 Вода: <b>{water} мл</b><br>
    🏃‍♂️ Тренировки: <b>{workouts}</b><br>
    ⚖️ Вес: <b>{last_weight if last_weight else "нет данных"}</b>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ADD ----------------
elif menu == "➕ Добавить":
    st.title("➕ Добавить данные")

    t = st.selectbox("Тип", ["Вода 💧", "Тренировка 🏃‍♂️", "Вес ⚖️"])
    v = st.number_input("Значение", min_value=0.0)
    c = st.text_input("Комментарий")

    h = st.number_input("📏 Рост (см)", min_value=0)
    w = st.number_input("⚖️ Вес (кг)", min_value=0.0)

    if st.button("Сохранить"):
        if v <= 0:
            st.error("Введите корректное значение")
        else:
            add_record(t, v, c, h, w)
            st.success("Запись добавлена!")

# ---------------- AI COACH ----------------
elif menu == "🧠 AI Коуч":
    st.title("🧠 Умный AI-коуч")

    height = st.number_input("📏 Рост (см)", min_value=50)
    weight = st.number_input("⚖️ Вес (кг)", min_value=10.0)
    water = st.number_input("💧 Вода (мл)", min_value=0)
    sleep = st.slider("😴 Сон (часы)", 0, 12, 7)
    activity = st.selectbox("🏃‍♂️ Активность", ["Низкая", "Средняя", "Высокая"])
    goal = st.selectbox("🎯 Цель", ["Похудение", "Набор массы", "Поддержание"])

    if st.button("Анализировать"):
        st.markdown("### 📊 Результат")

        bmi = weight / ((height / 100) ** 2) if height > 0 else 0

        st.write(f"📊 BMI: **{bmi:.1f}**")

        # BMI
        if bmi < 18.5:
            st.warning("⚠️ Недостаток массы")
        elif bmi < 25:
            st.success("✅ Норма")
        else:
            st.warning("⚠️ Лишний вес")

        # water
        if water < 1500:
            st.warning("💧 Пей больше воды")

        # sleep
        if sleep < 7:
            st.warning("😴 Нужно больше сна")

        # training advice
        st.markdown("### 🏋️‍♂️ Тренировки")

        if goal == "Похудение":
            st.info("🏃‍♂️ Кардио 4–5 раз + дефицит калорий")
        elif goal == "Набор массы":
            st.info("🏋️‍♂️ Силовые 4–5 раз + белок")
        else:
            st.info("⚖️ Баланс: 3 тренировки в неделю")

# ---------------- PROGRESS ----------------
elif menu == "🏆 Прогресс":
    st.title("🏆 Прогресс")

    workouts = len([i for i in data if "Тренировка" in i["type"]])
    water = sum(i["value"] for i in data if "Вода" in i["type"])

    level = "Новичок"
    if workouts > 10:
        level = "Атлет"
    elif workouts > 5:
        level = "Активный"

    st.markdown(f"""
    <div class="card">
    🏆 Уровень: <b>{level}</b><br>
    🏃‍♂️ Тренировки: <b>{workouts}</b><br>
    💧 Вода: <b>{water} мл</b>
    </div>
    """, unsafe_allow_html=True)

    if workouts < 5:
        st.info("💡 Тренируйся чаще")
    else:
        st.success("🔥 Отличный прогресс!")

# ---------------- NUTRITION ----------------
elif menu == "🥗 Питание":
    st.title("🥗 Питание и рацион")

    goal = st.selectbox("🎯 Цель", ["Похудение", "Набор массы", "Поддержание"])

    if goal == "Похудение":
        st.markdown("""
        <div class="card">
        🔥 1500–1800 ккал<br>
        🍗 Белок: высокий<br>
        🥗 Углеводы: низкие<br>
        🥑 Жиры: умеренно<br><br>
        ❌ Убрать сладкое и фастфуд
        </div>
        """, unsafe_allow_html=True)

    elif goal == "Набор массы":
        st.markdown("""
        <div class="card">
        🔥 2500–3000+ ккал<br>
        🍗 Белок: высокий<br>
        🍚 Углеводы: много (рис, овсянка)<br>
        🥑 Жиры: полезные<br><br>
        💪 Есть 4–5 раз в день
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card">
        🔥 2000–2200 ккал<br>
        ⚖️ Баланс БЖУ<br>
        🥗 Овощи ежедневно<br><br>
        ✔️ Без строгих ограничений
        </div>
        """, unsafe_allow_html=True)