import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Enterprise MCP AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise MCP AI Assistant")
st.markdown("Ask questions, search the web, send emails, access Google Sheets, Drive, Docs, and Calendar using n8n MCP.")

N8N_WEBHOOK_URL = "https://n8n.srv1542745.hstgr.cloud/webhook/8f34b1ef-3ceb-4045-8e5e-b4e2ea746914/chat"

question = st.text_area(
    "Enter your request",
    height=120,
    placeholder="Example:\n- What is the French Open 2026 schedule?\n- Send an email to john@example.com\n- Create a calendar meeting tomorrow at 3 PM"
)

if st.button("Ask AI"):
    
    if not question.strip():
        st.warning("Please enter a question.")
    
    else:
        
        with st.spinner("Processing request..."):
            
            payload = {
                "chatInput": question
            }

            headers = {
                "Content-Type": "application/json"
            }

            try:
                
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    headers=headers,
                    timeout=180
                )

                if response.status_code == 200:
                    
                    try:
                        data = response.json()

                        st.success("Response generated successfully!")

                        if isinstance(data, dict):

                            if "output" in data:
                                st.markdown("## 🤖 AI Response")
                                st.write(data["output"])

                            elif "response" in data:
                                st.markdown("## 🤖 AI Response")
                                st.write(data["response"])

                            else:
                                st.markdown("## 🤖 AI Response")
                                st.json(data)

                        else:
                            st.markdown("## 🤖 AI Response")
                            st.write(data)

                    except Exception:
                        
                        st.markdown("## 🤖 AI Response")
                        st.write(response.text)

                else:
                    
                    st.error(f"Error {response.status_code}")
                    st.code(response.text)

            except Exception as e:
                
                st.error("Failed to connect to n8n workflow")
                st.exception(e)