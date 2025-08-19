"""
Contract Analysis Multi-Agent System - Streamlit Web Interface
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from contract_analysis_system import (
    ContractAnalysisSystem,
    extract_text_from_pdf,
    analyze_contract,
    save_analysis_results,
    ContractAnalysisResult
)

# Page configuration
st.set_page_config(
    page_title="Contract Analysis System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .success-badge {
        background: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    
    .error-badge {
        background: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    
    .warning-badge {
        background: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

def initialize_system():
    """Initialize the contract analysis system"""
    try:
        with st.spinner("🚀 Initializing Multi-Agent System..."):
            system = ContractAnalysisSystem()
            st.session_state.system = system
            st.success("✅ All agents initialized successfully!")
            return True
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {e}")
        st.error("Please check your API keys and dependencies")
        return False

def display_header():
    """Display the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Contract Analysis Multi-Agent System</h1>
        <p>AI-Powered Contract Review with Structure • Legal • Negotiation • Management Analysis</p>
    </div>
    """, unsafe_allow_html=True)

def display_system_status():
    """Display system status in sidebar"""
    st.sidebar.markdown("### 🔧 System Status")
    
    if st.session_state.system is None:
        st.sidebar.error("🔴 System Not Initialized")
        if st.sidebar.button("Initialize System", type="primary"):
            initialize_system()
    else:
        st.sidebar.success("🟢 System Ready")
        
        # Agent status
        st.sidebar.markdown("**Agent Status:**")
        agents = ["Structure", "Legal", "Negotiation", "Manager"]
        for agent in agents:
            st.sidebar.markdown(f"✅ {agent} Agent")
        
        # Analysis history
        if st.session_state.analysis_history:
            st.sidebar.markdown(f"**📊 Analyses Completed:** {len(st.session_state.analysis_history)}")

def extract_pdf_text(uploaded_file):
    """Extract text from uploaded PDF file"""
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Extract text
        text = extract_text_from_pdf(temp_path)
        
        # Clean up
        Path(temp_path).unlink(missing_ok=True)
        
        return text
    except Exception as e:
        st.error(f"Error extracting PDF text: {e}")
        return None

def create_analysis_metrics(result: ContractAnalysisResult):
    """Create metrics display for analysis results"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📄 Contract Length",
            value=f"{result.contract_info['length']:,} chars"
        )
    
    with col2:
        total_agents = len(result.agent_responses)
        success_agents = sum(1 for resp in result.agent_responses if "error" not in resp.findings)
        st.metric(
            label="🤖 Agent Success",
            value=f"{success_agents}/{total_agents}"
        )
    
    with col3:
        # Calculate average confidence
        confidences = [resp.confidence_score for resp in result.agent_responses]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        st.metric(
            label="🎯 Avg Confidence",
            value=f"{avg_confidence:.1%}"
        )
    
    with col4:
        # Overall risk assessment
        risk_levels = [resp.risk_level for resp in result.agent_responses if resp.risk_level != "PENDING"]
        if risk_levels:
            high_risk = sum(1 for r in risk_levels if r == "HIGH")
            overall_risk = "HIGH" if high_risk > 0 else "MEDIUM" if "MEDIUM" in risk_levels else "LOW"
        else:
            overall_risk = "UNKNOWN"
        
        risk_color = "red" if overall_risk == "HIGH" else "orange" if overall_risk == "MEDIUM" else "normal"
        st.metric(
            label="⚠️ Risk Level",
            value=overall_risk,
            delta_color=risk_color
        )

def display_agent_responses(result: ContractAnalysisResult):
    """Display individual agent responses with improved formatting"""
    st.markdown("### 🤖 Individual Agent Analysis")
    
    for i, response in enumerate(result.agent_responses):
        with st.expander(f"{response.agent_name} - {response.analysis_type.replace('_', ' ').title()}", expanded=i==0):
            
            # Agent metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**⏰ Timestamp:** {response.timestamp}")
            with col2:
                risk_color = "🔴" if response.risk_level == "HIGH" else "🟡" if response.risk_level == "MEDIUM" else "🟢"
                st.markdown(f"**⚠️ Risk Level:** {risk_color} {response.risk_level}")
            with col3:
                st.markdown(f"**🎯 Confidence:** {response.confidence_score:.1%}")
            
            # Analysis content
            st.markdown("**🔍 Analysis Findings:**")
            if "error" not in response.findings:
                findings_text = response.findings.get('raw_response', 'No detailed findings available')
                st.markdown(f"```\n{findings_text}\n```")
            else:
                st.error(f"❌ Error: {response.findings['error']}")
            
            # Recommendations
            if response.recommendations:
                st.markdown("**💡 Recommendations:**")
                for rec in response.recommendations:
                    st.markdown(f"• {rec}")

def create_risk_visualization(result: ContractAnalysisResult):
    """Create risk assessment visualization"""
    # Prepare data for visualization
    agents = []
    risk_scores = []
    confidences = []
    
    risk_mapping = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "PENDING": 0, "UNKNOWN": 0}
    
    for response in result.agent_responses:
        agents.append(response.agent_name.replace("Agent", ""))
        risk_scores.append(risk_mapping.get(response.risk_level, 0))
        confidences.append(response.confidence_score * 100)
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=risk_scores,
        theta=agents,
        fill='toself',
        name='Risk Level',
        line_color='red'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[c/33.33 for c in confidences],  # Normalize to 0-3 scale
        theta=agents,
        fill='toself',
        name='Confidence',
        line_color='blue',
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3],
                ticktext=["None", "Low", "Medium", "High"],
                tickvals=[0, 1, 2, 3]
            )),
        showlegend=True,
        title="Risk Assessment & Confidence by Agent"
    )
    
    return fig

def main_analysis_interface():
    """Main interface for contract analysis"""
    
    if st.session_state.system is None:
        st.warning("⚠️ Please initialize the system first using the sidebar.")
        return

    # Initialize session state variables if they don't exist
    if "contract_text" not in st.session_state:
        st.session_state.contract_text = None
    if "contract_name" not in st.session_state:
        st.session_state.contract_name = None

    st.markdown("### 📁 PDF Contract Upload")
        
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload your contract PDF file for analysis"
    )
        
    if uploaded_file is not None:
        st.info(f"📄 File: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
        
        if st.button("📖 Extract Text from PDF", type="primary"):
            with st.spinner("Extracting text from PDF..."):
                text = extract_pdf_text(uploaded_file)
                if text:
                    st.session_state.contract_text = text
                    st.session_state.contract_name = f"PDF Contract - {Path(uploaded_file.name).stem}"
                    st.success(f"✅ Extracted {len(text):,} characters")
                    st.text_area(
                        "📄 Extracted Text Preview:",
                        text[:500] + "...",
                        height=200
                    )
                else:
                    st.error("❌ Failed to extract text from PDF")

    # Analysis execution
    if st.session_state.contract_text and st.session_state.contract_name:
        st.markdown("---")
    
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📄 Ready to analyze:** {st.session_state.contract_name}")
            st.markdown(f"**📊 Text length:** {len(st.session_state.contract_text):,} characters")
    
        with col2:
            if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
                with st.spinner("🔍 Analyzing contract with all agents..."):
                    result = analyze_contract(
                        st.session_state.system, 
                        st.session_state.contract_text, 
                        st.session_state.contract_name
                    )
                    # Save results in session state
                    st.session_state.current_analysis = result
                    if "analysis_history" not in st.session_state:
                        st.session_state.analysis_history = []
                    st.session_state.analysis_history.append(result)
                
                st.success("✅ Analysis completed!")


def display_analysis_results():
    """Display detailed analysis results"""
    if st.session_state.current_analysis is None:
        return
    
    result = st.session_state.current_analysis
    
    st.markdown("## 🎯 Analysis Results")
    
    # Metrics overview
    create_analysis_metrics(result)
    
    st.markdown("---")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🤖 Agent Details", "📈 Visualizations", "💾 Export"])
    
    with tab1:
        st.markdown("### 📋 Executive Summary")
        
        # Manager consolidation
        if "error" not in result.consolidated_findings:
            st.markdown("#### 👨‍💼 Management Synthesis")
            synthesis = result.consolidated_findings.get("manager_synthesis", "No synthesis available")
            st.markdown(f"```\n{synthesis}\n```")
        else:
            st.error(f"❌ Consolidation Error: {result.consolidated_findings['error']}")
        
        # Traceability map
        st.markdown("#### 🔗 Agent Traceability")
        trace_df = pd.DataFrame([
            {
                "Role": role.replace('_', ' ').title(),
                "Agent": agent_name,
                "Status": "✅ Completed" if not any("FAILED" in agent_name for _ in [agent_name]) else "❌ Failed"
            }
            for role, agent_name in result.traceability_map.items()
        ])
        st.dataframe(trace_df, use_container_width=True)
    
    with tab2:
        display_agent_responses(result)
    
    with tab3:
        st.markdown("### 📈 Risk Assessment Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk radar chart
            fig = create_risk_visualization(result)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Confidence scores bar chart
            agents = [resp.agent_name.replace("Agent", "") for resp in result.agent_responses]
            confidences = [resp.confidence_score * 100 for resp in result.agent_responses]
            
            fig_bar = px.bar(
                x=agents,
                y=confidences,
                title="Agent Confidence Scores",
                labels={"x": "Agent", "y": "Confidence (%)"}
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab4:
        st.markdown("### 💾 Export Analysis Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save to File", type="primary"):
                filepath = save_analysis_results(result)
                if filepath:
                    st.success(f"✅ Results saved to: {filepath}")
                else:
                    st.error("❌ Failed to save results")
        
        with col2:
            # Download as JSON
            result_json = json.dumps(result.__dict__, default=str, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=result_json,
                file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
def analysis_history_page():
    """Display analysis history"""
    st.markdown("## 📊 Analysis History")
    
    if not st.session_state.analysis_history:
        st.info("📭 No analysis history available. Complete some contract analyses to see them here.")
        return
    
    # History overview
    st.markdown(f"**Total Analyses:** {len(st.session_state.analysis_history)}")
    
    # Create history table
    history_data = []
    for i, result in enumerate(st.session_state.analysis_history):
        timestamp = datetime.fromisoformat(result.analysis_timestamp)
        agent_count = len(result.agent_responses)
        success_count = sum(1 for resp in result.agent_responses if "error" not in resp.findings)
        
        history_data.append({
            "Index": i + 1,
            "Contract Name": result.contract_info['name'],
            "Date": timestamp.strftime("%Y-%m-%d %H:%M"),
            "Length (chars)": f"{result.contract_info['length']:,}",
            "Agents Success": f"{success_count}/{agent_count}",
            "Status": "✅ Complete" if success_count == agent_count else "⚠️ Partial"
        })
    
    history_df = pd.DataFrame(history_data)
    
    # Display with selection
    selected_indices = st.dataframe(
        history_df,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    # Show details for selected analysis
    if selected_indices and selected_indices.selection.rows:
        selected_idx = selected_indices.selection.rows[0]
        selected_result = st.session_state.analysis_history[selected_idx]
        
        st.markdown("---")
        st.markdown("### 📋 Selected Analysis Details")
        
        # Set as current analysis for detailed view
        if st.button("📖 View Full Analysis", type="primary"):
            st.session_state.current_analysis = selected_result
            st.rerun()

def main():
    """Main Streamlit application"""
    
    # Display header
    display_header()
    
    # Sidebar
    display_system_status()
    
    # Navigation
    st.sidebar.markdown("---")
    page = st.sidebar.selectbox(
        "📋 Navigation",
        ["🏠 Contract Analysis", "📊 Analysis History", "ℹ️ About"]
    )
    
    # Main content based on navigation
    if page == "🏠 Contract Analysis":
        main_analysis_interface()
        
        # Display results if available
        if st.session_state.current_analysis:
            st.markdown("---")
            display_analysis_results()
    
    elif page == "📊 Analysis History":
        analysis_history_page()
    
    elif page == "ℹ️ About":
        st.markdown("## ℹ️ About Contract Analysis System")
        
        st.markdown("""
        ### 🎯 Features
        
        - **Multi-Agent Analysis**: Specialized AI agents for different aspects of contract review
        - **Comprehensive Coverage**: Structure, Legal, Negotiation, and Management perspectives
        - **Full Traceability**: Track which agent contributed to each recommendation
        - **Risk Assessment**: Automated risk level evaluation with confidence scores
        - **Multiple Input Methods**: PDF upload, sample contracts, or custom text
        - **Visual Analytics**: Interactive charts and metrics
        - **Export Capabilities**: Save results in multiple formats
        
        ### 🤖 AI Agents
        
        1. **Structure Agent**: Analyzes contract organization and completeness
        2. **Legal Agent**: Reviews legal compliance and enforceability
        3. **Negotiation Agent**: Identifies optimization opportunities
        4. **Manager Agent**: Consolidates findings and prioritizes actions
        
        ### 🔧 Technical Stack
        
        - **Frontend**: Streamlit with interactive visualizations
        - **Backend**: Multi-agent AI system with full traceability
        - **File Processing**: PDF text extraction capabilities
        - **Data Visualization**: Plotly charts and metrics
        """)

if __name__ == "__main__":
    main()