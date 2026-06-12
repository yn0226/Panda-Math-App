import streamlit as st
import random

#総正解数
if "total_correct" not in st.session_state:
    st.session_state.total_correct = 0

#入力欄リセット用
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

#バルーン表示用
if "reward_shown" not in st.session_state:
    st.session_state.reward_shown = []
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

# 獲得した瞬間だけ表示するパンダ
if "new_reward" not in st.session_state:
    st.session_state.new_reward = None

#苦手問題用
if "mistakes" not in st.session_state:
    st.session_state.mistakes = []


#タイトル
#st.title("🐼 パンダけいさんランド 🐼")
st.image(
    "images/title_banner.png",
    use_container_width=True
)
st.caption("🐼 パンダをあつめながら けいさんれんしゅう！")

mode = st.selectbox(
    "れんしゅうする計算をえらんでね",
    ["きほん", "くり上がり・くり下がり", "九九"]
)

# 正解数表示
st.subheader(
    f"🐼 パンダポイント：{st.session_state.total_correct}"
)


#バルーン表示リセット
if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False


#問題
def make_question(mode):

    if mode == "きほん":
        op = random.choice(["+", "-"])

        if op == "+":
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            question = f"{a} + {b} = ?"
            correct_answer = a + b

        else:
            a = random.randint(1, 9)
            b = random.randint(1, a)
            question = f"{a} - {b} = ?"
            correct_answer = a - b

    elif mode == "くり上がり・くり下がり":
        op = random.choice(["+", "-"])

        if op == "+":
            # 答えが10以上になる足し算
            a = random.randint(2, 9)
            b = random.randint(10 - a, 9)
            question = f"{a} + {b} = ?"
            correct_answer = a + b

        else:
            # 繰り下がりがある引き算
            b = random.randint(2, 9)
            ones = random.randint(0, b - 1)
            tens = random.randint(1, 2)
            a = tens * 10 + ones

            question = f"{a} - {b} = ?"
            correct_answer = a - b

    else:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        question = f"{a} × {b} = ?"
        correct_answer = a * b

    return question, correct_answer

#問題が勝手に変わらないようにする
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode

if "question" not in st.session_state:
    st.session_state.question, st.session_state.correct_answer = make_question(mode)

if st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    st.session_state.question, st.session_state.correct_answer = make_question(mode)
    st.session_state.message = ""
    st.rerun()

# ごほうび表示
if st.session_state.new_reward == 5:
    st.image("images/panda_05.png", width=350)
    st.success("🐼 ノーマルパンダゲット！")

elif st.session_state.new_reward == 10:
    st.image("images/panda_10.png", width=350)
    st.success("🎋 笹パンダゲット！")

elif st.session_state.new_reward == 20:
    st.image("images/panda_20.png", width=350)
    st.success("👑 王様パンダゲット！")

elif st.session_state.new_reward == 30:
    st.image("images/panda_30.png", width=350)
    st.success("🚀 宇宙飛行士パンダゲット！")

#ごほうびパンダをしまう
if st.session_state.new_reward is not None:
    if st.button("パンダをしまう"):
        st.session_state.new_reward = None
        st.rerun()

# 次の目標表示
goals = [5, 10, 20, 30]

next_goal = None

for goal in goals:
    if st.session_state.total_correct < goal:
        next_goal = goal
        break

if next_goal is not None:
    remaining = next_goal - st.session_state.total_correct
    if st.session_state.total_correct < 5:
        st.write(
            f"あと {remaining} ポイントで最初のパンダ！"
        )
    else:
        st.write(
            f"あと {remaining} ポイントで次のパンダ！"
        )
else:
    st.write("すべてのパンダをゲットしたよ！🐼🎉")

st.divider()


#問題表示
st.header(st.session_state.question)

#st.header(question)


#回答判定
answer = st.number_input(
    "こたえをいれてね",
    step=1,
    key=f"answer_{st.session_state.input_key}"
)

if "message" not in st.session_state:
    st.session_state.message = ""

button_clicked = st.button("こたえる")

feedback_area = st.empty()

if button_clicked:
    if answer == st.session_state.correct_answer:
        st.session_state.total_correct += 1

        #パンダ獲得時だけ表示させる
        if st.session_state.total_correct == 5:
            st.session_state.new_reward = 5
        elif st.session_state.total_correct == 10:
            st.session_state.new_reward = 10
        elif st.session_state.total_correct == 20:
            st.session_state.new_reward = 20
        elif st.session_state.total_correct == 30:
            st.session_state.new_reward = 30

        st.session_state.input_key += 1

        st.session_state.message = "せいかい！🐼"
        st.session_state.question, st.session_state.correct_answer = make_question(mode)

        #正解数＝5/10/20/30でバルーン表示
        if st.session_state.total_correct in [5, 10, 20, 30]:
            st.session_state.show_balloons = True
            st.session_state.reward_shown.append(st.session_state.total_correct)

        st.rerun()
    else:
        st.session_state.message = "もういちど！"

        #不正解保存
        mistake = f"{st.session_state.question} 正解:{st.session_state.correct_answer}"

        if mistake not in st.session_state.mistakes:
            st.session_state.mistakes.append(mistake)

if st.session_state.message == "せいかい！🐼":
    feedback_area.success("せいかい！🐼")
    st.session_state.message = ""
elif st.session_state.message == "もういちど！":
    feedback_area.error("もういちど！")


#残数カウント
remaining = next_goal - st.session_state.total_correct



#パンダ獲得数表示
st.subheader("🐼 パンダずかん")

st.write("✅ ノーマルパンダ" if st.session_state.total_correct >= 5 else "⬜ ノーマルパンダ")
st.write("✅ 笹パンダ" if st.session_state.total_correct >= 10 else "⬜ 笹パンダ")
st.write("✅ 王様パンダ" if st.session_state.total_correct >= 20 else "⬜ 王様パンダ")
st.write("✅ 宇宙飛行士パンダ" if st.session_state.total_correct >= 30 else "⬜ 宇宙飛行士パンダ")

#不正解表示
st.subheader("📚 にがて問題")

if len(st.session_state.mistakes) == 0:
    st.write("まだないよ！")
else:
    for m in st.session_state.mistakes:
        st.write("•", m)


#リセットボタン
if st.button("🔄 はじめから"):
    st.session_state.total_correct = 0
    st.session_state.question, st.session_state.correct_answer = make_question(mode)
    st.session_state.input_key += 1
    st.rerun()