import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Aravia Grok Diagnostic", page_icon="🔍", layout="wide")
st.title("🔍 Aravia Grok API 診斷工具")
st.caption("用嚟檢查你 API Key 可唔可以用 + 可用模型名")

client = OpenAI(
    api_key=st.secrets["XAI_API_KEY"],
    base_url="https://api.x.ai/v1"
)

st.write("### 1. 檢查 API Key 狀態")
if st.button("🔍 列出所有可用模型"):
    with st.spinner("正在查詢可用模型..."):
        try:
            models = client.models.list()
            st.success("✅ API Key 正常！以下係你可以用嘅模型：")
            for m in models.data:
                st.code(m.id)
        except Exception as e:
            st.error("❌ API 錯誤")
            st.code(str(e))

st.write("### 2. 測試 Kan Explainer")
test_query = st.text_input("輸入測試問題", "Space of Appearance 喺TOD項目點應用？")
if st.button("測試 Explainer"):
    with st.spinner("測試中..."):
        try:
            response = client.chat.completions.create(
                model="grok-3",   # 先試 grok-3
                messages=[{"role": "user", "content": test_query}],
                max_tokens=500
            )
            st.success("成功！")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error("錯誤")
            st.code(str(e))

st.caption("診斷完後請 Copy 返上面顯示嘅可用模型名同錯誤訊息畀我，我會即刻畀你最終正確版本")
