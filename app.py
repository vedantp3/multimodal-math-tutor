"""Multimodal Math Mentor — Streamlit Application"""
import time
import json
import streamlit as st

from config import OCR_CONFIDENCE_THRESHOLD, ASR_CONFIDENCE_THRESHOLD
from input_handlers.image_handler import ImageHandler
from input_handlers.audio_handler import AudioHandler
from input_handlers.text_handler import TextHandler
from agents.parser_agent import ParserAgent
from agents.router_agent import RouterAgent
from agents.solver_agent import SolverAgent
from agents.verifier_agent import VerifierAgent
from agents.explainer_agent import ExplainerAgent
from rag.retriever import RAGRetriever
from memory.memory_store import MemoryStore

# ─── Page Config ───
st.set_page_config(
    page_title="Multimodal math mentor",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2rem; }
    .main-header p  { color: rgba(255,255,255,0.85); margin: 0.3rem 0 0; }
    .confidence-high   { background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600; }
    .confidence-medium { background: #f59e0b; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600; }
    .confidence-low    { background: #ef4444; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600; }
    .agent-trace-item {
        border-left: 3px solid #667eea;
        padding: 8px 12px;
        margin: 6px 0;
        background: rgba(102,126,234,0.05);
        border-radius: 0 8px 8px 0;
    }
    .hitl-banner {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .memory-card {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f8fafc;
    }
    .stButton > button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ─── Initialize Services (cached) ───
@st.cache_resource
def get_retriever():
    return RAGRetriever()

@st.cache_resource
def get_memory():
    return MemoryStore()

@st.cache_resource
def get_agents():
    return {
        "parser": ParserAgent(),
        "router": RouterAgent(),
        "solver": SolverAgent(),
        "verifier": VerifierAgent(),
        "explainer": ExplainerAgent(),
    }

@st.cache_resource
def get_input_handlers():
    return {
        "image": ImageHandler(),
        "audio": AudioHandler(),
        "text": TextHandler(),
    }


def main():
    # ─── Header ───
    st.markdown("""
    <div class="main-header">
        <h1>🧮 Math Mentor</h1>
        <p>JEE math tutor — Upload a photo, speak, or type your problem</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "agent_trace" not in st.session_state:
        st.session_state.agent_trace = []
    if "current_entry_id" not in st.session_state:
        st.session_state.current_entry_id = None
    if "solution_data" not in st.session_state:
        st.session_state.solution_data = None
    if "show_feedback_form" not in st.session_state:
        st.session_state.show_feedback_form = False
    
    # Load services
    retriever = get_retriever()
    memory = get_memory()
    agents = get_agents()
    handlers = get_input_handlers()
    
    # ─── Sidebar ───
    with st.sidebar:
        st.header("⚙️ Input Mode")
        input_mode = st.radio(
            "Choose input method:",
            ["📝 Text", "📷 Image", "🎤 Audio"],
            index=0,
            help="Select how you want to input your math problem"
        )
        
        st.divider()
        
        # Memory Statistics
        st.header("🧠 Memory Stats")
        stats = memory.get_stats()
        col1, col2 = st.columns(2)
        col1.metric("Problems Solved", stats["total_problems"])
        col2.metric("Accuracy", 
                     f"{stats['correct']}/{stats['correct'] + stats['incorrect']}" 
                     if (stats['correct'] + stats['incorrect']) > 0 else "N/A")
        
        if stats["topics"]:
            st.caption("**Topics solved:**")
            for topic, count in stats["topics"].items():
                st.caption(f"  • {topic}: {count}")
        
        st.divider()
        
    
    # ─── Main Input Section ───
    extracted_text = ""
    confidence = 10
    input_type = "text"
    hitl_triggered = False
    extraction_notes = ""
    
    if "📝 Text" in input_mode:
        input_type = "text"
        extracted_text = st.text_area(
            "✏️ Type your math problem:",
            height=120,
            placeholder="e.g., Find the roots of x² - 5x + 6 = 0"
        )
        confidence = 10
    
    elif "📷 Image" in input_mode:
        input_type = "image"
        uploaded_file = st.file_uploader(
            "📷 Upload a math problem image",
            type=["png", "jpg", "jpeg"],
            help="Upload a photo or screenshot of a math problem"
        )
        
        if uploaded_file:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            with col2:
                with st.spinner("🔍 Extracting text from image..."):
                    image_bytes = uploaded_file.read()
                    mime_type = f"image/{uploaded_file.type.split('/')[-1]}" if '/' in uploaded_file.type else "image/png"
                    ocr_result = handlers["image"].extract_text(image_bytes, mime_type)
                
                extracted_text = ocr_result.get("text", "")
                confidence = ocr_result.get("confidence", 5)
                extraction_notes = ocr_result.get("extraction_notes", "")
                
                # Show confidence
                conf_class = "high" if confidence >= 7 else ("medium" if confidence >= 4 else "low")
                st.markdown(f'OCR Confidence: <span class="confidence-{conf_class}">{confidence}/10</span>', unsafe_allow_html=True)
                
                if extraction_notes:
                    st.caption(f"📝 Notes: {extraction_notes}")
                
                # HITL trigger for low confidence
                if confidence < OCR_CONFIDENCE_THRESHOLD:
                    hitl_triggered = True
                    st.markdown("""
                    <div class="hitl-banner">
                        ⚠️ <strong>Human Review Needed</strong> — OCR confidence is low. Please review and edit the extracted text below.
                    </div>
                    """, unsafe_allow_html=True)
            
            # Editable extraction
            extracted_text = st.text_area(
                "✏️ Verify and edit extracted text:",
                value=extracted_text,
                height=120
            )
    
    elif "🎤 Audio" in input_mode:
        input_type = "audio"
        
        audio_tab1, audio_tab2 = st.tabs(["📁 Upload Audio", "🎙️ Record Audio"])
        
        with audio_tab1:
            audio_file = st.file_uploader(
                "Upload an audio file",
                type=["mp3", "wav", "m4a"],
                help="Upload a recording of your math question"
            )
        
        with audio_tab2:
            audio_recording = st.audio_input("🎙️ Record your math question")
        
        audio_data = None
        audio_mime = "audio/wav"
        
        if audio_file:
            audio_data = audio_file.read()
            ext = audio_file.name.split(".")[-1].lower()
            mime_map = {"mp3": "audio/mpeg", "wav": "audio/wav", "m4a": "audio/mp4"}
            audio_mime = mime_map.get(ext, "audio/wav")
            st.audio(audio_data, format=audio_mime)
        elif audio_recording:
            audio_data = audio_recording.read()
            audio_mime = "audio/wav"
            st.audio(audio_data, format="audio/wav")
        
        if audio_data:
            with st.spinner("🎧 Transcribing audio..."):
                asr_result = handlers["audio"].transcribe(audio_data, audio_mime)
            
            extracted_text = asr_result.get("text", "")
            confidence = asr_result.get("confidence", 5)
            extraction_notes = asr_result.get("transcription_notes", "")
            
            conf_class = "high" if confidence >= 7 else ("medium" if confidence >= 4 else "low")
            st.markdown(f'ASR Confidence: <span class="confidence-{conf_class}">{confidence}/10</span>', unsafe_allow_html=True)
            
            if extraction_notes:
                st.caption(f"📝 Notes: {extraction_notes}")
            
            if confidence < ASR_CONFIDENCE_THRESHOLD:
                hitl_triggered = True
                st.markdown("""
                <div class="hitl-banner">
                    ⚠️ <strong>Human Review Needed</strong> — Transcription confidence is low. Please review and edit below.
                </div>
                """, unsafe_allow_html=True)
            
            extracted_text = st.text_area(
                "✏️ Verify and edit transcription:",
                value=extracted_text,
                height=120
            )
    
    # ─── Solve Button ───
    col_solve, col_recheck = st.columns([1, 1])
    
    with col_solve:
        solve_button = st.button("🚀 Solve Problem", type="primary", use_container_width=True,
                                  disabled=not extracted_text.strip())
    
    with col_recheck:
        recheck_button = st.button("🔄 Re-check Solution", use_container_width=True,
                                    disabled=st.session_state.solution_data is None)
    
    # ─── Solving Pipeline ───
    if (solve_button or recheck_button) and extracted_text.strip():
        st.session_state.agent_trace = []
        st.session_state.solution_data = None
        
        with st.status("🧠 AI Agents working...", expanded=True) as status:
            
            # ── Step 1: Parser Agent ──
            st.write("🔍 **Parser Agent** — Analyzing problem structure...")
            t0 = time.time()
            parsed = agents["parser"].parse(extracted_text)
            t_parse = time.time() - t0
            st.session_state.agent_trace.append({
                "agent": "Parser Agent",
                "status": "✅ Complete",
                "time": f"{t_parse:.1f}s",
                "output": f"Topic: {parsed.get('topic', 'unknown')} | Vars: {parsed.get('variables', [])} | Needs clarification: {parsed.get('needs_clarification', False)}"
            })
            
            # HITL: Parser detected ambiguity
            if parsed.get("needs_clarification"):
                st.warning(f"⚠️ **Clarification needed**: {parsed.get('clarification_reason', 'Problem is ambiguous')}")
                st.info("Please edit the problem text above and try again.")
                hitl_triggered = True
            
            # ── Step 2: Router Agent ──
            st.write("🗺️ **Router Agent** — Classifying and routing...")
            t0 = time.time()
            route_info = agents["router"].route(parsed)
            t_route = time.time() - t0
            st.session_state.agent_trace.append({
                "agent": "Router Agent",
                "status": "✅ Complete",
                "time": f"{t_route:.1f}s",
                "output": f"Topic: {route_info.get('topic')} | Subtopic: {route_info.get('subtopic')} | Difficulty: {route_info.get('difficulty')} | Tools: {route_info.get('tools_needed', [])}"
            })
            
            # ── Step 3: RAG Retrieval ──
            st.write("📚 **RAG Pipeline** — Retrieving relevant knowledge...")
            t0 = time.time()
            rag_results = retriever.retrieve(
                f"{parsed.get('topic', '')} {parsed.get('problem_text', extracted_text)}"
            )
            t_rag = time.time() - t0
            
            rag_context = "\n\n".join([
                f"**[{r['metadata'].get('source_name', r['metadata'].get('source', 'Unknown'))}]**\n{r['content']}"
                for r in rag_results
            ])
            
            st.session_state.agent_trace.append({
                "agent": "RAG Retrieval",
                "status": "✅ Complete",
                "time": f"{t_rag:.1f}s",
                "output": f"Retrieved {len(rag_results)} chunks from knowledge base"
            })
            
            # ── Step 4: Memory Lookup ──
            st.write("🧠 **Memory** — Checking for similar problems...")
            t0 = time.time()
            memory_context = memory.get_memory_context(
                parsed.get("problem_text", extracted_text)
            )
            similar_problems = memory.find_similar(
                parsed.get("problem_text", extracted_text)
            )
            t_mem = time.time() - t0
            
            st.session_state.agent_trace.append({
                "agent": "Memory Lookup",
                "status": "✅ Complete",
                "time": f"{t_mem:.1f}s",
                "output": f"Found {len(similar_problems)} similar previously-solved problems"
            })
            
            # ── Step 5: Solver Agent ──
            st.write("🧮 **Solver Agent** — Computing solution...")
            t0 = time.time()
            solver_result = agents["solver"].solve(
                parsed, route_info, rag_context, memory_context
            )
            t_solve = time.time() - t0
            
            python_note = ""
            if solver_result.get("python_verification"):
                pv = solver_result["python_verification"]
                python_note = f" | Python verification: {'✅ ' + pv['output'][:50] if pv['success'] else '❌ ' + pv.get('error', '')[:50]}"
            
            st.session_state.agent_trace.append({
                "agent": "Solver Agent",
                "status": "✅ Complete",
                "time": f"{t_solve:.1f}s",
                "output": f"Solution generated ({len(solver_result.get('solution', ''))} chars){python_note}"
            })
            
            # ── Step 6: Verifier Agent ──
            st.write("✅ **Verifier Agent** — Checking correctness...")
            t0 = time.time()
            verification = agents["verifier"].verify(
                parsed, solver_result["solution"], solver_result.get("python_verification")
            )
            t_verify = time.time() - t0
            
            st.session_state.agent_trace.append({
                "agent": "Verifier Agent",
                "status": "✅ Complete",
                "time": f"{t_verify:.1f}s",
                "output": f"Correct: {verification.get('is_correct')} | Confidence: {verification.get('confidence', 0)}% | Issues: {len(verification.get('issues', []))}"
            })
            
            # HITL: Verifier low confidence
            if verification.get("needs_hitl"):
                hitl_triggered = True
            
            # ── Step 7: Explainer Agent ──
            st.write("📖 **Explainer Agent** — Creating student-friendly explanation...")
            t0 = time.time()
            explanation = agents["explainer"].explain(
                parsed, solver_result["solution"], verification, route_info
            )
            t_explain = time.time() - t0
            
            st.session_state.agent_trace.append({
                "agent": "Explainer Agent",
                "status": "✅ Complete",
                "time": f"{t_explain:.1f}s",
                "output": f"Explanation generated ({len(explanation)} chars)"
            })
            
            # ── Store in memory ──
            entry_id = memory.store({
                "input_type": input_type,
                "original_input": extracted_text,
                "parsed_question": parsed,
                "retrieved_context": rag_context[:1000],
                "route_info": route_info,
                "solution": solver_result["solution"],
                "verification": verification,
                "explanation": explanation,
            })
            st.session_state.current_entry_id = entry_id
            
            # Store solution data
            st.session_state.solution_data = {
                "parsed": parsed,
                "route_info": route_info,
                "rag_results": rag_results,
                "rag_context": rag_context,
                "similar_problems": similar_problems,
                "solver_result": solver_result,
                "verification": verification,
                "explanation": explanation,
                "hitl_triggered": hitl_triggered,
            }
            
            total_time = t_parse + t_route + t_rag + t_mem + t_solve + t_verify + t_explain
            status.update(label=f"✅ Complete — {total_time:.1f}s total", state="complete")
    
    # ─── Display Results ───
    if st.session_state.solution_data:
        data = st.session_state.solution_data
        
        # HITL Banner for Verifier
        if data.get("hitl_triggered") and data["verification"].get("needs_hitl"):
            st.markdown("""
            <div class="hitl-banner">
                ⚠️ <strong>Human Review Recommended</strong> — The verifier is not fully confident in this solution. 
                Please review the answer and provide feedback below.
            </div>
            """, unsafe_allow_html=True)
            
            if data["verification"].get("issues"):
                st.warning("**Verifier concerns:**\n" + "\n".join(f"- {issue}" for issue in data["verification"]["issues"]))
        
        # Layout: Two columns
        left_col, right_col = st.columns([3, 2])
        
        with left_col:
            # Solution & Explanation
            st.subheader("📝 Solution")
            st.markdown(data["solver_result"]["solution"])
            
            # Python verification result
            pv = data["solver_result"].get("python_verification")
            if pv:
                with st.expander("🐍 Python Verification", expanded=False):
                    if pv["success"]:
                        st.success(f"✅ Python output: {pv['output']}")
                    else:
                        st.error(f"❌ Python error: {pv.get('error', 'Unknown error')}")
            
            st.divider()
            
            st.subheader("📖 Step-by-Step Explanation")
            st.markdown(data["explanation"])
        
        with right_col:
            # Confidence Indicator
            st.subheader("📊 Confidence")
            conf = data["verification"].get("confidence", 0)
            if conf >= 80:
                conf_color = "🟢"
                conf_label = "High"
            elif conf >= 50:
                conf_color = "🟡"
                conf_label = "Medium"
            else:
                conf_color = "🔴"
                conf_label = "Low"
            
            st.metric(
                label=f"{conf_color} Verification Confidence",
                value=f"{conf}%",
                delta=conf_label
            )
            st.progress(conf / 100)
            
            is_correct = data["verification"].get("is_correct", False)
            st.markdown(f"**Correctness:** {'✅ Verified correct' if is_correct else '⚠️ Needs review'}")
            
            if data["verification"].get("edge_cases_checked"):
                st.caption("**Edge cases checked:** " + ", ".join(data["verification"]["edge_cases_checked"][:3]))
            
            st.divider()
            
            # Agent Trace Panel
            with st.expander("🔍 Agent Trace", expanded=False):
                for trace in st.session_state.agent_trace:
                    st.markdown(f"""
                    <div class="agent-trace-item">
                        <strong>{trace['agent']}</strong> {trace['status']} <small>({trace['time']})</small><br>
                        <small>{trace['output']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Retrieved Context (RAG)
            with st.expander("📚 Retrieved Knowledge (RAG)", expanded=False):
                for i, r in enumerate(data["rag_results"], 1):
                    source = r["metadata"].get("source_name", r["metadata"].get("source", "Unknown"))
                    score = r.get("score", 0)
                    st.markdown(f"**Source {i}:** {source} (relevance: {score:.2f})")
                    st.caption(r["content"][:300] + ("..." if len(r["content"]) > 300 else ""))
                    st.divider()
            
            # Similar Problems from Memory
            if data["similar_problems"]:
                with st.expander("🧠 Similar Previously-Solved Problems", expanded=False):
                    for sp in data["similar_problems"]:
                        st.markdown(f"""
                        <div class="memory-card">
                            <strong>Similarity: {sp['similarity_score']:.1%}</strong><br>
                            <em>{sp.get('parsed_question', {}).get('problem_text', sp.get('original_input', 'N/A'))[:200]}</em>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        fb = sp.get("feedback")
                        if fb and isinstance(fb, dict):
                            st.caption(f"Previous feedback: {fb.get('status', 'none')}")
            
            # Parsed Problem Info
            with st.expander("🏷️ Parsed Problem Info", expanded=False):
                st.json(data["parsed"])
        
        st.divider()
        
        # ─── Feedback Section ───
        st.subheader("💬 Feedback")
        st.caption("Help Math Mentor learn! Your feedback improves future solutions.")
        
        fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 2])
        
        with fb_col1:
            if st.button("✅ Correct", use_container_width=True, type="primary"):
                if st.session_state.current_entry_id:
                    memory.update_feedback(st.session_state.current_entry_id, "correct")
                    memory._load()  # Reload
                    st.success("Thanks! Feedback recorded. ✅")
        
        with fb_col2:
            if st.button("❌ Incorrect", use_container_width=True):
                st.session_state.show_feedback_form = True
        
        with fb_col3:
            if st.session_state.get("show_feedback_form"):
                feedback_comment = st.text_input(
                    "What was wrong? (optional)",
                    placeholder="e.g., The sign was flipped in step 3"
                )
                if st.button("Submit Feedback"):
                    if st.session_state.current_entry_id:
                        memory.update_feedback(
                            st.session_state.current_entry_id, 
                            "incorrect",
                            feedback_comment
                        )
                        memory._load()  # Reload
                        st.session_state.show_feedback_form = False
                        st.warning("Feedback recorded. We'll learn from this! 📝")


if __name__ == "__main__":
    main()
