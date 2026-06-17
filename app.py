import streamlit as st
import random

#初期化---------
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

#テンキー用
if "answer_text" not in st.session_state:
    st.session_state.answer_text = ""
if "message" not in st.session_state:
    st.session_state.message = ""

#パンダランダム取得用
if "owned_rewards" not in st.session_state:
    st.session_state.owned_rewards = []
if "swat_unlocked" not in st.session_state:
    st.session_state.swat_unlocked = False


#タイトル
#st.title("🐼 パンダけいさんランド 🐼")
st.image(
    "images/title_banner.png",
    use_container_width=True
)
st.caption("🐼 パンダをあつめながら けいさんれんしゅう！")

mode = st.selectbox(
    "れんしゅうする計算をえらんでね",
    ["きほん", "くり上がり・くり下がり", "九九", "にがて復習"]
)

#ごほうび一覧
reward_list = {
    "normal": {
        "name": "ノーマルパンダ",
        "image": "images/normal_panda.png"
    },
    "bamboo": {
        "name": "笹パンダ",
        "image": "images/bamboo_panda.png"
    },
    "king": {
        "name": "王様パンダ",
        "image": "images/king_panda.png"
    },
    "space": {
        "name": "宇宙飛行士パンダ",
        "image": "images/space_panda.png"
    },
    "fire": {
        "name": "消防士パンダ",
        "image": "images/firefighter_panda.png"
    },
    "army": {
        "name": "自衛隊パンダ",
        "image": "images/army_panda.png"
    },
    "lesser": {
        "name": "レッサーパンダ",
        "image": "images/red_panda.png"
    },
    "lesser_costume": {
        "name": "レッサーパンダの着ぐるみパンダ",
        "image": "images/red_panda_costume.png"
    },
    "police": {
        "name": "警察パンダ",
        "image": "images/police_panda.png"
    },
    "whitebike": {
        "name": "白バイパンダ",
        "image": "images/whitebike_panda.png"
    },
    "patrolcar": {
        "name": "パトカーパンダ",
        "image": "images/patrolcar_panda.png"
    },
    "coastguard": {
        "name": "海上保安庁パンダ",
        "image": "images/coastguard_panda.png"
    },
    "doctor": {
        "name": "お医者さんパンダ",
        "image": "images/doctor_panda.png"
    },    
    "artist": {
        "name": "画家パンダ",
        "image": "images/artist_panda.png"
    },        
}
#シークレットリスト
secret_reward_list = {
    "swat": {
        "name": "スワットパンダ",
        "image": "images/swat_panda.png"
    }
}


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
            # 繰り上がりなし：答えが9以下
            a = random.randint(1, 8)
            b = random.randint(1, 9 - a)

            question = f"{a} + {b} = ?"
            correct_answer = a + b

        else:
            # 繰り下がりなし：一桁どうしの引き算
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

    elif mode == "にがて復習":
        if len(st.session_state.mistakes) == 0:
            question = "にがて問題はまだないよ！"
            correct_answer = None
        else:
            mistake = random.choice(st.session_state.mistakes)
            question = mistake["question"]
            correct_answer = mistake["answer"]

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
all_rewards = {
    **reward_list,
    **secret_reward_list
}

if st.session_state.new_reward is not None:
    reward = all_rewards[st.session_state.new_reward]
    st.image(reward["image"], width=350)
    st.success(f"🐼 {reward['name']}ゲット！")

#ごほうびパンダをしまう
if st.session_state.new_reward is not None:
    if st.button("パンダをしまう"):
        st.session_state.new_reward = None
        st.rerun()

# 次の目標表示
goals = [5,10,20,30,40,50,60,70,
 80,90,100,120,140,160]

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
answer_text = st.text_input(
    "こたえをいれてね",
    st.session_state.answer_text,
    key=f"answer_{st.session_state.input_key}"
)

#テンキー
def add_number(num):
    st.session_state.answer_text += num
    st.session_state.input_key += 1

def clear_answer():
    st.session_state.answer_text = ""
    st.session_state.input_key += 1

def backspace_answer():
    st.session_state.answer_text = st.session_state.answer_text[:-1]
    st.session_state.input_key += 1


keypad = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["C", "0", "←"],
]

for row_index, row in enumerate(keypad):
    cols = st.columns(3)
    for col_index, label in enumerate(row):
        with cols[col_index]:
            if st.button(label, key=f"btn_{row_index}_{col_index}", use_container_width=True):
                if label == "C":
                    clear_answer()
                elif label == "←":
                    backspace_answer()
                else:
                    add_number(label)
                st.rerun()

button_clicked = st.button(
    "こたえる",
    key="btn_answer",
    use_container_width=True
)

feedback_area = st.empty()

if button_clicked:
    try:
        answer = int(st.session_state.answer_text)
    except ValueError:
        st.session_state.message = "すうじをいれてね！"
        st.rerun()

    if answer == st.session_state.correct_answer:
        st.session_state.total_correct += 1

        # にがて復習で正解したら、にがて問題から消す
        if mode == "にがて復習":
            solved_mistake = {
                "question": st.session_state.question,
                "answer": st.session_state.correct_answer
            }

            if solved_mistake in st.session_state.mistakes:
                st.session_state.mistakes.remove(solved_mistake)
            
            #にがて復習クリア時にSWATパンダ開放
            if len(st.session_state.mistakes) == 0 and not st.session_state.swat_unlocked:
                st.session_state.swat_unlocked = True
                st.session_state.new_reward = "swat"
                st.session_state.show_balloons = True

        # 正解時のごほうび判定
        reward_points = [
            5,10,20,30,40,50,60,70,
            80,90,100,120,140,160
        ]

        if st.session_state.total_correct in reward_points:
            if st.session_state.total_correct == 5:
                reward_key = "normal"
            else:
                candidates = [
                    key for key in reward_list.keys()
                    if key not in st.session_state.owned_rewards
                    and key != "normal"
                ]

                if len(candidates) > 0:
                    reward_key = random.choice(candidates)
                else:
                    reward_key = None

            if reward_key is not None:
                st.session_state.owned_rewards.append(reward_key)
                st.session_state.new_reward = reward_key

            st.session_state.show_balloons = True

        # 正解後の後処理
        st.session_state.answer_text = ""
        st.session_state.input_key += 1
        st.session_state.message = "せいかい！🐼"
        st.session_state.question, st.session_state.correct_answer = make_question(mode)

        st.rerun()

    else:
        st.session_state.message = "もういちど！"

        mistake = {
            "question": st.session_state.question,
            "answer": st.session_state.correct_answer
        }

        if mistake not in st.session_state.mistakes:
            st.session_state.mistakes.append(mistake)

if st.session_state.message == "せいかい！🐼":
    feedback_area.success("せいかい！🐼")
    st.session_state.message = ""

elif st.session_state.message == "もういちど！":
    feedback_area.error("もういちど！")

elif st.session_state.message == "すうじをいれてね！":
    feedback_area.warning("すうじをいれてね！")





#パンダ獲得数表示
owned_count = len(st.session_state.owned_rewards)

if st.session_state.swat_unlocked:
    owned_count += 1

st.subheader(
    f"🐼 パンダずかん ({owned_count}/15)"
)

cols = st.columns(3)

for i, (key, reward) in enumerate(reward_list.items()):
    col = cols[i % 3]

    with col:
        with st.container(border=True):
            unlocked = key in st.session_state.owned_rewards

            if unlocked:
                st.image(reward["image"], use_container_width=True)
                st.write(f"✅ {reward['name']}")
            else:
                st.write("⬜ ？？？？")

# シークレット枠
st.subheader("🔒 シークレットパンダ")

left, center, right = st.columns([1,1,1])

with center:
    with st.container(border=True):

        if st.session_state.swat_unlocked:
            reward = secret_reward_list["swat"]

            st.image(
                reward["image"],
                use_container_width=True
            )
            st.write(f"✅ {reward['name']}")
        else:
            st.write("⬜ ？？？？")


#不正解表示
st.subheader("📚 にがて問題")

if len(st.session_state.mistakes) == 0:
    st.write("まだないよ！")
else:
    for m in st.session_state.mistakes:
        st.write(f"• {m['question']} 正解:{m['answer']}")


#リセットボタン
if st.button("🔄 はじめから"):
    st.session_state.total_correct = 0
    st.session_state.question, st.session_state.correct_answer = make_question(mode)
    st.session_state.input_key += 1
    st.session_state.answer_text = ""
    st.session_state.owned_rewards = []
    st.session_state.new_reward = None
    st.session_state.swat_unlocked = False
    st.session_state.mistakes = []
    st.rerun()