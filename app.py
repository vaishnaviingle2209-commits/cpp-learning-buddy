import streamlit as st
import time

st.set_page_config(page_title="C++ Learning Buddy", page_icon="🤖", layout="wide")

# ----------------- SESSION STATE SETUP -----------------
if "chats" not in st.session_state:
    st.session_state.chats = {
        "Chat 1": {
            "title": "New C++ Chat",
            "messages": []
        }
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "suggested_prompt" not in st.session_state:
    st.session_state.suggested_prompt = None


# ----------------- SIDEBAR (CHATGPT STYLE) -----------------
with st.sidebar:
    st.title("💬 Chat History")

    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_id = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[new_id] = {
            "title": f"New C++ Chat {len(st.session_state.chats) + 1}",
            "messages": []
        }
        st.session_state.current_chat = new_id
        st.session_state.suggested_prompt = None
        st.rerun()

    st.markdown("---")

    # Tutor Mode / System Persona
    tutor_mode = st.selectbox(
        "🎯 Tutor Persona:",
        [
            "💡 Friendly Mentor (ELI5 & Examples)",
            "⚡ DSA & Interview Prep Coach",
            "🔍 Code Reviewer & Bug Hunter",
            "⚙️ Systems & Memory Specialist"
        ]
    )

    st.markdown("---")

    # Past conversations with Delete (🗑️) button
    for chat_id, data in list(st.session_state.chats.items()):
        col_chat, col_del = st.columns([4, 1])
        btn_type = "primary" if chat_id == st.session_state.current_chat else "secondary"
        
        with col_chat:
            if st.button(data["title"], key=f"select_{chat_id}", type=btn_type, use_container_width=True):
                st.session_state.current_chat = chat_id
                st.session_state.suggested_prompt = None
                st.rerun()
        with col_del:
            # Delete button (only allow deletion if more than 1 chat exists)
            if len(st.session_state.chats) > 1:
                if st.button("✕", key=f"del_{chat_id}", help="Delete chat"):
                    del st.session_state.chats[chat_id]
                    # Fallback to the first available chat
                    st.session_state.current_chat = list(st.session_state.chats.keys())[0]
                    st.rerun()

    st.markdown("---")

    # Export Chat to Markdown
    active_msgs = st.session_state.chats[st.session_state.current_chat]["messages"]
    if active_msgs:
        export_text = f"# C++ Learning Buddy Notes - {st.session_state.chats[st.session_state.current_chat]['title']}\n\n"
        for m in active_msgs:
            export_text += f"### {m['role'].capitalize()}\n{m['content']}\n\n"
        st.download_button(
            "💾 Export Current Chat",
            data=export_text,
            file_name="cpp_study_notes.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Clear All Chats
    if st.button("🗑️ Clear All Chats", use_container_width=True):
        st.session_state.chats = {
            "Chat 1": {"title": "New C++ Chat", "messages": []}
        }
        st.session_state.current_chat = "Chat 1"
        st.session_state.suggested_prompt = None
        st.rerun()


# ----------------- MAIN INTERFACE -----------------
active_chat = st.session_state.chats[st.session_state.current_chat]

st.header("🤖 C++ Learning Buddy")
st.caption(f"Tutor Mode: **{tutor_mode}**")

# Response generator simulator
def stream_response(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03)

def generate_cpp_answer(question: str, mode: str) -> str:
    """Generates structured C++ explanations matching the question."""
    q_lower = question.lower()
    if "paradigm" in q_lower:
        return (
            "### C++ Programming Paradigms\n"
            "C++ is a **multi-paradigm language**, meaning it supports multiple programming styles:\n\n"
            "1. **Procedural Programming**: Code organized into procedures/functions (`int main()`, loops, statements).\n"
            "2. **Object-Oriented Programming (OOP)**: Encapsulation, inheritance, polymorphism using `class` and `struct`.\n"
            "3. **Generic Programming**: Code independent of data types using **Templates** and the **STL** (`std::vector<T>`).\n"
            "4. **Functional Features (Modern C++)**: Lambdas, `constexpr`, and pure functions.\n\n"
            "```cpp\n"
            "#include <iostream>\n"
            "#include <vector>\n"
            "#include <algorithm>\n\n"
            "// OOP Paradigm\n"
            "class Greeter {\n"
            "public:\n"
            "    void sayHello() const {\n"
            "        std::cout << \"Hello from OOP!\\n\";\n"
            "    }\n"
            "};\n\n"
            "int main() {\n"
            "    Greeter g;\n"
            "    g.sayHello();\n"
            "    return 0;\n"
            "}\n"
            "```"
        )
    elif "pointer" in q_lower:
        return (
            "### Pointers in C++\n"
            "A **pointer** is a variable that stores the memory address of another variable.\n\n"
            "```cpp\n"
            "#include <iostream>\n\n"
            "int main() {\n"
            "    int score = 100;\n"
            "    int* ptr = &score; // '&' gets memory address\n\n"
            "    std::cout << \"Value: \" << *ptr << \"\\n\"; // '*' dereferences pointer\n"
            "    std::cout << \"Address: \" << ptr << \"\\n\";\n"
            "    return 0;\n"
            "}\n"
            "```\n"
            "💡 *Tip: Prefer smart pointers (`std::unique_ptr`) over raw pointers in modern C++.*"
        )
    else:
        return (
            f"Here is a comprehensive breakdown for **{question}**:\n\n"
            "```cpp\n"
            "#include <iostream>\n\n"
            "int main() {\n"
            "    // Implementation\n"
            "    std::cout << \"C++ Learning Buddy\" << std::endl;\n"
            "    return 0;\n"
            "}\n"
            "```\n"
            f"- **Persona focus ({mode})**: Ensure RAII principles and safe pointer practices."
        )

# ----------------- EMPTY STATE SUGGESTIONS -----------------
# Only show prompt buttons when there are NO messages in this conversation
if len(active_chat["messages"]) == 0:
    st.info("💡 Start a conversation or select a topic below:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📌 Explain Pointers in C++", use_container_width=True):
            st.session_state.suggested_prompt = "Explain pointers in C++ with memory details."
            st.rerun()
    with col2:
        if st.button("🏗️ Object-Oriented Principles", use_container_width=True):
            st.session_state.suggested_prompt = "What are the OOP paradigms in C++ with code?"
            st.rerun()
    with col3:
        if st.button("⚡ Memory Leaks & RAII", use_container_width=True):
            st.session_state.suggested_prompt = "What is a memory leak in C++ and how does RAII solve it?"
            st.rerun()


# ----------------- DISPLAY CHAT MESSAGES -----------------
for i, msg in enumerate(active_chat["messages"]):
    avatar_icon = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])
        
        # ChatGPT-style interactive feedback actions under assistant messages
        if msg["role"] == "assistant":
            sub_col1, sub_col2, sub_col3 = st.columns([1, 1, 10])
            with sub_col1:
                st.button("👍", key=f"up_{i}", help="Good response")
            with sub_col2:
                st.button("👎", key=f"down_{i}", help="Needs improvement")


# ----------------- INPUT PROCESSING -----------------
user_input = st.chat_input("Ask any C++ question, paste compiler error, or request code...")

# Pick up either typed input or clicked suggested button
prompt = user_input or st.session_state.suggested_prompt

if prompt:
    # Reset clicked pill state so it doesn't trigger repeatedly
    st.session_state.suggested_prompt = None

    # Update chat title automatically from first question
    if len(active_chat["messages"]) == 0:
        short_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
        active_chat["title"] = short_title

    # 1. Append and render user message
    active_chat["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 2. Stream assistant response
    with st.chat_message("assistant", avatar="🤖"):
        raw_text = generate_cpp_answer(prompt, tutor_mode)
        streamed_response = st.write_stream(stream_response(raw_text))

    # 3. Store response in session state
    active_chat["messages"].append({"role": "assistant", "content": streamed_response})
    st.rerun()