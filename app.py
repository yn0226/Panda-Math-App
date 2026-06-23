import streamlit as st
import random
import json
import os
from datetime import datetime

SAVE_FILE = "save_data.json"

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

#コンプリート表示
if "complete_shown" not in st.session_state:
    st.session_state.complete_shown = False

# 獲得した瞬間だけ表示するパンダ
if "new_reward" not in st.session_state:
    st.session_state.new_reward = None

#苦手問題用
if "mistakes" not in st.session_state:
    st.session_state.mistakes = []

#テンキー用
if "message" not in st.session_state:
    st.session_state.message = ""

#パンダランダム取得用
if "owned_rewards" not in st.session_state:
    st.session_state.owned_rewards = []

# シークレットパンダ所持一覧
if "owned_secret_rewards" not in st.session_state:
    st.session_state.owned_secret_rewards = []

#日付保存用
if "saved_at" not in st.session_state:
    st.session_state.saved_at = ""

#モードごとの正答数表示
if "mode_correct_counts" not in st.session_state:
    st.session_state.mode_correct_counts = {
        "きほん": 0,
        "くり上がり・くり下がり": 0,
        "九九": 0,
        "にがて復習": 0
    }

# 保存するデータ-----------
def get_save_data():
    return {
        "total_correct": st.session_state.total_correct,
        "owned_rewards": st.session_state.owned_rewards,
        "owned_secret_rewards": st.session_state.owned_secret_rewards,
        "mistakes": st.session_state.mistakes,
        "saved_at": datetime.now().strftime("%Y/%m/%d %H:%M"),
        "mode_correct_counts": st.session_state.mode_correct_counts
    }

def save_game():
    save_data = get_save_data()

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

    st.session_state.saved_at = save_data["saved_at"]

def load_game():
    if not os.path.exists(SAVE_FILE):
        return False

    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    st.session_state.total_correct = data.get("total_correct", 0)
    st.session_state.owned_rewards = data.get("owned_rewards", [])
    st.session_state.owned_secret_rewards = data.get("owned_secret_rewards", [])
    st.session_state.mistakes = data.get("mistakes", [])
    st.session_state.saved_at = data.get("saved_at", "")
    st.session_state.mode_correct_counts = data.get(
    "mode_correct_counts",
    {
        "きほん": 0,
        "くり上がり・くり下がり": 0,
        "九九": 0,
        "にがて復習": 0
    }
)

    st.session_state.new_reward = None
    st.session_state.show_balloons = False
    st.session_state.message = "つづきから はじめたよ！"
    st.session_state.input_key += 1

    return True

#タイトル
#st.title("🐼 パンダけいさんランド 🐼")
st.image(
    "images/title_banner.png",
    use_container_width=True
)
st.caption("🐼 パンダをあつめながら けいさんれんしゅう！")

st.caption("💾 あそんだきろくは じどうでほぞんされるよ")
if st.session_state.saved_at:
    st.caption(f"さいごのきろく：{st.session_state.saved_at}")

if os.path.exists(SAVE_FILE):
    st.caption("📂 つづきから あそべるよ")

# セーブ・ロードボタン
save_col, load_col = st.columns(2)

with save_col:
    if st.button("💾 きろくを のこす", use_container_width=True):
        save_game()
        st.success("きろくを のこしたよ！")

with load_col:
    if st.button("📂 つづきから あそぶ", use_container_width=True):
        if load_game():
            st.rerun()
        else:
            st.warning("まだ きろくが ないよ！")


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
    },
    "ninja": {
        "name": "忍者パンダ",
        "image": "images/ninja_panda.png"
    },
    "forensics": {
        "name": "鑑識パンダ",
        "image": "images/forensics_panda.png"
    }
}


# 正解数表示
st.subheader(
    f"🐼 パンダポイント：{st.session_state.total_correct}"
)
st.caption("📘 れんしゅうきろく")
st.caption(
    f"きほん：{st.session_state.mode_correct_counts['きほん']}もん / "
    f"くり上がり・くり下がり：{st.session_state.mode_correct_counts['くり上がり・くり下がり']}もん / "
    f"九九：{st.session_state.mode_correct_counts['九九']}もん / "
    f"にがて復習：{st.session_state.mode_correct_counts['にがて復習']}もん"
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
answer_value = st.number_input(
    "こたえをいれてね",
    min_value=0,
    step=1,
    value=None,
    placeholder="こたえ",
    key=f"answer_{st.session_state.input_key}"
)

button_clicked = st.button(
    "こたえる",
    key="btn_answer",
    use_container_width=True
)

feedback_area = st.empty()

if button_clicked:
    if answer_value is None:
        st.session_state.message = "すうじをいれてね！"
        st.rerun()

    answer = int(answer_value)

    if answer == st.session_state.correct_answer:
        st.session_state.total_correct += 1
        st.session_state.mode_correct_counts[mode] += 1

        # にがて復習で正解したら、にがて問題から消す
        if mode == "にがて復習":
            solved_mistake = {
                "question": st.session_state.question,
                "answer": st.session_state.correct_answer
            }

            if solved_mistake in st.session_state.mistakes:
                st.session_state.mistakes.remove(solved_mistake)
            
            # にがて復習クリア時にシークレットパンダをランダム開放
            if len(st.session_state.mistakes) == 0:
                secret_candidates = [
                    key for key in secret_reward_list.keys()
                    if key not in st.session_state.owned_secret_rewards
                ]

                if len(secret_candidates) > 0:
                    secret_key = random.choice(secret_candidates)
                    st.session_state.owned_secret_rewards.append(secret_key)
                    st.session_state.new_reward = secret_key
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
        st.session_state.input_key += 1
        st.session_state.message = "せいかい！🐼"
        st.session_state.question, st.session_state.correct_answer = make_question(mode)
        save_game()
        st.rerun()

    else:
        st.session_state.message = "もういちど！"

        mistake = {
            "question": st.session_state.question,
            "answer": st.session_state.correct_answer
        }

        if mistake not in st.session_state.mistakes:
            st.session_state.mistakes.append(mistake)
        save_game()

if st.session_state.message == "せいかい！🐼":
    feedback_area.success("せいかい！🐼")
    st.session_state.message = ""

elif st.session_state.message == "もういちど！":
    feedback_area.error("もういちど！")

elif st.session_state.message == "すうじをいれてね！":
    feedback_area.warning("すうじをいれてね！")

elif st.session_state.message == "つづきから はじめたよ！":
    feedback_area.success("つづきから はじめたよ！")
    st.session_state.message = ""





#パンダ獲得数表示
owned_count = (
    len(st.session_state.owned_rewards)
    + len(st.session_state.owned_secret_rewards)
)

total_pandas = len(reward_list) + len(secret_reward_list)

#コンプリート確認
is_complete = owned_count == total_pandas
if is_complete and not st.session_state.complete_shown:
    st.balloons()
    st.snow()
    st.session_state.complete_shown = True

st.subheader(
    f"🐼 パンダずかん ({owned_count}/{total_pandas})"
)

if is_complete:
    st.success("🎉 パンダずかん コンプリート！きみはパンダマスター！🐼")

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

secret_cols = st.columns(3)

for i, (key, reward) in enumerate(secret_reward_list.items()):
    col = secret_cols[i]

    with col:
        with st.container(border=True):
            unlocked = key in st.session_state.owned_secret_rewards

            if unlocked:
                st.image(reward["image"], use_container_width=True)
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
    st.session_state.owned_rewards = []
    st.session_state.new_reward = None
    st.session_state.owned_secret_rewards = []
    st.session_state.mistakes = []
    st.session_state.complete_shown = False
    
    save_game()
    st.rerun()