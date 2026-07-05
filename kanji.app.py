import streamlit as st
import random

# data.py から KANJI_LIST を読み込む
try:
    from data import KANJI_LIST
except ImportError:
    st.error("data.py が見つかりません。同じフォルダに作成してください。")
    st.stop()

# --- 1. 各種状態の初期化 ---
if 'all_kanji_data' not in st.session_state:
    st.session_state.all_kanji_data = KANJI_LIST
if 'wrong_list' not in st.session_state:
    st.session_state.wrong_list = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'mode' not in st.session_state:
    st.session_state.mode = None

# --- クイズエンジンの定義 ---
def quiz_engine(data_list):
    if st.session_state.current_question >= len(data_list):
        st.write(f"テスト終了！スコア: {st.session_state.score} / {len(data_list)}")
        if st.button("もう一度やる"):
            st.session_state.mode = None
            st.rerun()
        return

    q = data_list[st.session_state.current_question]
    st.write(f"### 第 {st.session_state.current_question + 1} 問")
    st.write(f"## {q['kanji']}")

    # 選択肢を作成（正解1つ＋ダミー3つ）
    options = [q['read']]
    while len(options) < 4:
        dummy = random.choice(data_list)['read']
        if dummy not in options:
            options.append(dummy)
    random.shuffle(options)

    # ボタンのIDが重複しないようにユニークなキーを生成
    for opt in options:
        # keyに現在何問目かを含めることで重複を回避
        if st.button(opt, key=f"btn_{st.session_state.current_question}_{opt}"):
            if opt == q['read']:
                st.success("正解！")
                st.session_state.score += 1
            else:
                st.error(f"残念！正解は {q['read']} でした")
                st.session_state.wrong_list.append(q)
            
            st.session_state.current_question += 1
            st.rerun()

# --- サイドバーメニュー ---
with st.sidebar:
    st.title("🍀 メニュー")
    menu = st.radio("メニューを選んでね", ["🏠 ホーム", "✍️ テスト開始", "🔥 復習モード"])
    st.write("---")
    st.write(f"現在の苦手漢字: {len(st.session_state.wrong_list)} 個")

# --- メイン画面 ---
if menu == "🏠 ホーム":
    st.title("🏠 漢字クイズアプリへようこそ")
    st.write("左のメニューからテストを開始してください。")

elif menu == "✍️ テスト開始":
    st.title("✍️ 実力テスト")
    # テスト開始時のみ、問題をシャッフルして「10問だけ」抽出する
    if st.session_state.mode != "test":
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.mode = "test"
        # 全データからランダムに10個選ぶ
        all_data = st.session_state.all_kanji_data
        num_questions = min(10, len(all_data))
        st.session_state.test_data = random.sample(all_data, num_questions)

    quiz_engine(st.session_state.test_data)

elif menu == "🔥 復習モード":
    st.title("🔥 苦手克服")
    if not st.session_state.wrong_list:
        st.success("完璧！苦手な漢字はありません。")
    else:
        if st.session_state.mode != "review":
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.mode = "review"
            st.session_state.review_data = st.session_state.wrong_list[:]
        
        quiz_engine(st.session_state.review_data)
