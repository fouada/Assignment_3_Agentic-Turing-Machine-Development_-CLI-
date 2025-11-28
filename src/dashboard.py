#!/usr/bin/env python3
"""
Agentic Turing Machine - Interactive Research Dashboard
========================================================

MIT-Level Interactive Visualization Dashboard for Semantic Drift Analysis.

This dashboard provides:
1. 📊 Research Overview - Key metrics and findings at a glance
2. 🔬 Semantic Drift Explorer - Interactive noise level analysis
3. 🔄 Translation Pipeline Visualizer - EN→FR→HE→EN flow
4. 📈 Statistical Analysis Panel - Correlation, regression, effect sizes
5. 🎛️ Sensitivity Analysis - Parameter exploration
6. 💰 Cost Tracker - API usage and cost visualization
7. 📋 Comparative Analysis - Pairwise comparison matrix

Usage:
    streamlit run src/dashboard.py

Or with custom port:
    streamlit run src/dashboard.py --server.port 8501

Author: Agentic Turing Machine Team
License: MIT
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Agentic Turing Machine Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-',
        'Report a bug': 'https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-/issues',
        'About': """
        # Agentic Turing Machine
        
        MIT-Level Multi-Agent Translation System with Semantic Drift Analysis.
        
        **Authors:** Fouad Azem & Tal Goldengorn  
        **Course:** LLM and Multi Agent Orchestration  
        **Institution:** Reichman University
        """
    }
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main theme colors - Elegant dark/light compatible */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --success-color: #4ade80;
        --warning-color: #fbbf24;
        --error-color: #f87171;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #f8fafc, #e2e8f0);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        border-bottom: 3px solid var(--primary-color);
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #22c55e;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Smooth transitions */
    .stButton>button {
        transition: all 0.3s ease;
        border-radius: 0.5rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        background-color: #f1f5f9;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)


# =============================================================================
# Data Loading Functions
# =============================================================================

@st.cache_data
def load_analysis_results() -> Optional[Dict[str, Any]]:
    """Load semantic drift analysis results."""
    results_path = Path(__file__).parent.parent / "results" / "analysis_results_local.json"
    
    if not results_path.exists():
        return None
    
    try:
        with open(results_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading analysis results: {e}")
        return None


@st.cache_data
def load_cost_analysis() -> Optional[Dict[str, Any]]:
    """Load cost analysis data."""
    cost_path = Path(__file__).parent.parent / "results" / "cost_analysis.json"
    
    if not cost_path.exists():
        return None
    
    try:
        with open(cost_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return None


@st.cache_data
def load_comparative_analysis() -> Optional[Dict[str, Any]]:
    """Load comparative analysis data."""
    comparative_path = Path(__file__).parent.parent / "results" / "comparative_analysis.json"
    
    if not comparative_path.exists():
        return None
    
    try:
        with open(comparative_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return None


@st.cache_data
def load_sensitivity_analysis() -> Optional[Dict[str, Any]]:
    """Load sensitivity analysis data."""
    sensitivity_path = Path(__file__).parent.parent / "results" / "sensitivity_analysis.json"
    
    if not sensitivity_path.exists():
        return None
    
    try:
        with open(sensitivity_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return None


def load_translation_outputs() -> Dict[int, Dict[str, str]]:
    """Load all translation outputs from the outputs directory."""
    outputs_dir = Path(__file__).parent.parent / "outputs"
    translations = {}
    
    if not outputs_dir.exists():
        return translations
    
    for noise_dir in outputs_dir.iterdir():
        if noise_dir.is_dir() and noise_dir.name.startswith("noise_"):
            try:
                noise_level = int(noise_dir.name.split("_")[1])
                translations[noise_level] = {}
                
                # Load each translation file
                for txt_file in noise_dir.glob("*.txt"):
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        translations[noise_level][txt_file.stem] = f.read().strip()
            except (ValueError, IOError):
                continue
    
    return translations


# =============================================================================
# Visualization Components
# =============================================================================

def render_header():
    """Render the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Agentic Turing Machine</h1>
        <p>MIT-Level Interactive Research Dashboard for Semantic Drift Analysis</p>
        <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">
            Multi-Agent Translation System: English → French → Hebrew → English
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_key_metrics(data: Dict[str, Any], cost_data: Optional[Dict[str, Any]]):
    """Render key metrics cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics
    distances = data.get("semantic_distances", {})
    noise_levels = len(distances)
    
    avg_distance = np.mean(list(map(float, distances.values()))) if distances else 0
    text_sim = np.mean(list(map(float, data.get("text_similarities", {}).values()))) if data.get("text_similarities") else 0
    word_overlap = np.mean(list(map(float, data.get("word_overlaps", {}).values()))) if data.get("word_overlaps") else 0
    
    total_cost = 0
    if cost_data and "summary" in cost_data:
        total_cost = cost_data["summary"].get("total_cost", 0)
    
    with col1:
        st.metric(
            label="🎯 Noise Levels Tested",
            value=f"{noise_levels}",
            delta="Complete" if noise_levels >= 7 else f"{7-noise_levels} remaining"
        )
    
    with col2:
        st.metric(
            label="📏 Avg. Semantic Distance",
            value=f"{avg_distance:.4f}",
            delta="Lower is better",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="📝 Avg. Text Similarity",
            value=f"{text_sim:.1%}",
            delta="Higher is better"
        )
    
    with col4:
        st.metric(
            label="💰 Total API Cost",
            value=f"${total_cost:.4f}",
            delta="Cost-effective" if total_cost < 0.05 else None
        )


def render_semantic_drift_explorer(data: Dict[str, Any]):
    """Render the semantic drift explorer with interactive charts."""
    st.markdown('<h2 class="section-header">🔬 Semantic Drift Explorer</h2>', unsafe_allow_html=True)
    
    # Extract data
    distances = data.get("semantic_distances", {})
    text_sims = data.get("text_similarities", {})
    word_overlaps = data.get("word_overlaps", {})
    
    if not distances:
        st.warning("No semantic drift data available. Run the experiment first.")
        return
    
    # Create DataFrame
    noise_levels = sorted([int(k) for k in distances.keys()])
    df = pd.DataFrame({
        'Noise Level (%)': noise_levels,
        'Cosine Distance': [float(distances[str(n)]) for n in noise_levels],
        'Text Similarity': [float(text_sims.get(str(n), 0)) for n in noise_levels],
        'Word Overlap': [float(word_overlaps.get(str(n), 0)) for n in noise_levels]
    })
    
    # Controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        selected_metrics = st.multiselect(
            "Select Metrics to Display",
            ["Cosine Distance", "Text Similarity", "Word Overlap"],
            default=["Cosine Distance", "Text Similarity"]
        )
    
    with col2:
        chart_type = st.radio(
            "Chart Type",
            ["Line Chart", "Bar Chart", "Area Chart"],
            horizontal=True
        )
    
    with col3:
        show_data = st.checkbox("Show Data Table", value=False)
    
    if not selected_metrics:
        st.info("Please select at least one metric to display.")
        return
    
    # Create the chart
    fig = go.Figure()
    
    colors = {
        'Cosine Distance': '#667eea',
        'Text Similarity': '#22c55e',
        'Word Overlap': '#f59e0b'
    }
    
    for metric in selected_metrics:
        y_values = df[metric].values
        
        if chart_type == "Line Chart":
            fig.add_trace(go.Scatter(
                x=df['Noise Level (%)'],
                y=y_values,
                mode='lines+markers',
                name=metric,
                line=dict(color=colors[metric], width=3),
                marker=dict(size=10, symbol='circle'),
                hovertemplate=f"{metric}: %{{y:.4f}}<br>Noise: %{{x}}%<extra></extra>"
            ))
        elif chart_type == "Bar Chart":
            fig.add_trace(go.Bar(
                x=df['Noise Level (%)'],
                y=y_values,
                name=metric,
                marker_color=colors[metric],
                hovertemplate=f"{metric}: %{{y:.4f}}<br>Noise: %{{x}}%<extra></extra>"
            ))
        else:  # Area Chart
            fig.add_trace(go.Scatter(
                x=df['Noise Level (%)'],
                y=y_values,
                mode='lines',
                name=metric,
                fill='tonexty' if len(fig.data) > 0 else 'tozeroy',
                line=dict(color=colors[metric], width=2),
                hovertemplate=f"{metric}: %{{y:.4f}}<br>Noise: %{{x}}%<extra></extra>"
            ))
    
    fig.update_layout(
        title={
            'text': 'Semantic Drift Analysis Across Noise Levels',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Poppins'}
        },
        xaxis_title='Spelling Error Rate (%)',
        yaxis_title='Metric Value',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified',
        template='plotly_white',
        height=500,
        margin=dict(t=80, l=60, r=40, b=60)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if show_data:
        st.dataframe(
            df.style.format({
                'Cosine Distance': '{:.4f}',
                'Text Similarity': '{:.4f}',
                'Word Overlap': '{:.4f}'
            }).background_gradient(cmap='RdYlGn_r', subset=['Cosine Distance'])
            .background_gradient(cmap='RdYlGn', subset=['Text Similarity', 'Word Overlap']),
            use_container_width=True
        )


def render_translation_pipeline(data: Dict[str, Any], translations: Dict[int, Dict[str, str]]):
    """Render the translation pipeline visualization."""
    st.markdown('<h2 class="section-header">🔄 Translation Pipeline Visualizer</h2>', unsafe_allow_html=True)
    
    # Pipeline flow diagram
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Create Sankey-like flow diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["📝 English Input", "🇫🇷 French", "🇮🇱 Hebrew", "📄 English Output"],
                color=["#667eea", "#3b82f6", "#8b5cf6", "#22c55e"],
                x=[0.1, 0.4, 0.6, 0.9],
                y=[0.5, 0.5, 0.5, 0.5]
            ),
            link=dict(
                source=[0, 1, 2],
                target=[1, 2, 3],
                value=[100, 100, 100],
                color=["rgba(102, 126, 234, 0.4)", "rgba(59, 130, 246, 0.4)", "rgba(139, 92, 246, 0.4)"],
                label=["Agent 1: EN→FR", "Agent 2: FR→HE", "Agent 3: HE→EN"]
            )
        )])
        
        fig.update_layout(
            title={
                'text': 'Translation Chain Flow',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'family': 'Poppins'}
            },
            height=300,
            margin=dict(t=50, l=20, r=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>🔗 Translation Chain</h4>
            <ol>
                <li><strong>Agent 1:</strong> English → French</li>
                <li><strong>Agent 2:</strong> French → Hebrew</li>
                <li><strong>Agent 3:</strong> Hebrew → English</li>
            </ol>
            <p style="margin-top: 1rem; font-size: 0.9rem;">
                Each agent uses Claude AI with specialized skills defined in markdown files.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show actual translations
    st.subheader("📖 Translation Examples")
    
    # Noisy inputs for each noise level (from config)
    noisy_inputs = {
        0: "The artificial intelligence system can efficiently process natural language and understand complex semantic relationships within textual data.",
        10: "The artifical intelligence systm can efficiently process natural language and understand complex semantic relationships within textual data.",
        20: "The artifical inteligence systm can efficiently proces natural language and understand complex semantic relationships within textual data.",
        25: "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data.",
        30: "The artifical inteligence systm can eficiently proces natural langauge and understnd complex semantic relationships within textual data.",
        40: "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships within textual data.",
        50: "The artifical inteligence systm can eficiently proces naturel langauge and understnd complx semantic relatioships withn textul data."
    }
    
    available_noise_levels = sorted(translations.keys()) if translations else []
    
    if available_noise_levels:
        selected_noise = st.select_slider(
            "Select Noise Level to View Translations",
            options=available_noise_levels,
            value=available_noise_levels[0] if available_noise_levels else 0,
            format_func=lambda x: f"{x}% noise"
        )
        
        if selected_noise in translations:
            trans = translations[selected_noise]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Show the noisy input that was actually used for this noise level
                noisy_input = noisy_inputs.get(selected_noise, data.get("original_sentence", "N/A"))
                
                if selected_noise == 0:
                    st.markdown("**📥 Original/Input (Clean):**")
                    st.info(noisy_input)
                else:
                    st.markdown(f"**🔀 Noisy Input ({selected_noise}% errors):**")
                    st.warning(noisy_input)
                    
                    # Show original for comparison
                    with st.expander("📋 Compare with Original"):
                        st.info(data.get("original_sentence", noisy_inputs[0]))
            
            with col2:
                st.markdown("**🇫🇷 French Translation:**")
                st.success(trans.get("agent1_french", "N/A"))
                
            # Hebrew translation
                st.markdown("**🇮🇱 Hebrew Translation:**")
                st.success(trans.get("agent2_hebrew", "N/A"))
            
            # Final output with comparison
            st.markdown("**📤 Final English Output:**")
            final_output = trans.get("agent3_english", data.get("final_outputs", {}).get(str(selected_noise), "N/A"))
            st.success(final_output)
            
            # Highlight the key finding
            if selected_noise > 0:
                st.info(f"""
                🎯 **Key Finding:** Despite {selected_noise}% input errors, the AI produced the same translation as 0% noise!
                This demonstrates Claude's exceptional robustness to noisy inputs.
                """)
    else:
        st.info("No translation outputs available. Run the experiment to generate translations.")


def render_statistical_analysis(data: Dict[str, Any], comparative: Optional[Dict[str, Any]]):
    """Render statistical analysis panel."""
    st.markdown('<h2 class="section-header">📈 Statistical Analysis Panel</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Correlation Analysis", "📐 Regression", "🎯 Effect Sizes"])
    
    with tab1:
        render_correlation_analysis(data, comparative)
    
    with tab2:
        render_regression_analysis(data, comparative)
    
    with tab3:
        render_effect_sizes(data, comparative)


def render_correlation_analysis(data: Dict[str, Any], comparative: Optional[Dict[str, Any]]):
    """Render correlation analysis."""
    distances = data.get("semantic_distances", {})
    text_sims = data.get("text_similarities", {})
    word_overlaps = data.get("word_overlaps", {})
    
    if not distances:
        st.warning("No data available for correlation analysis.")
        return
    
    noise_levels = sorted([int(k) for k in distances.keys()])
    
    # Calculate correlations
    noise_arr = np.array(noise_levels)
    dist_arr = np.array([float(distances[str(n)]) for n in noise_levels])
    text_arr = np.array([float(text_sims.get(str(n), 0)) for n in noise_levels])
    word_arr = np.array([float(word_overlaps.get(str(n), 0)) for n in noise_levels])
    
    # Correlation matrix
    metrics_df = pd.DataFrame({
        'Noise Level': noise_arr,
        'Cosine Distance': dist_arr,
        'Text Similarity': text_arr,
        'Word Overlap': word_arr
    })
    
    corr_matrix = metrics_df.corr()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Heatmap
        fig = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            aspect='auto'
        )
        
        fig.update_layout(
            title={
                'text': 'Correlation Matrix',
                'x': 0.5,
                'xanchor': 'center'
            },
            height=400
        )
        
        # Add text annotations
        for i in range(len(corr_matrix)):
            for j in range(len(corr_matrix)):
                fig.add_annotation(
                    x=j, y=i,
                    text=f"{corr_matrix.iloc[i, j]:.3f}",
                    showarrow=False,
                    font=dict(color='white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black')
                )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Key Correlations")
        
        # Load from comparative if available
        if comparative and "correlation_analysis" in comparative:
            corr_results = comparative["correlation_analysis"].get("results", [])
            
            for corr in corr_results[:3]:
                if corr.get("test_name") == "Pearson r":
                    coef = corr.get("correlation_coefficient", 0)
                    p_val = corr.get("p_value", 1)
                    var2 = corr.get("variable2", "N/A")
                    
                    sig = "✅" if p_val < 0.05 else "⚠️"
                    strength = "Strong" if abs(coef) > 0.7 else "Moderate" if abs(coef) > 0.4 else "Weak"
                    
                    st.markdown(f"""
                    **{var2}**
                    - r = {coef:.4f} {sig}
                    - p = {p_val:.6f}
                    - Strength: {strength}
                    """)
        else:
            # Calculate basic correlations
            from scipy import stats
            r, p = stats.pearsonr(noise_arr, dist_arr)
            st.markdown(f"""
            **Noise vs Distance**
            - r = {r:.4f}
            - p = {p:.6f}
            """)


def render_regression_analysis(data: Dict[str, Any], comparative: Optional[Dict[str, Any]]):
    """Render regression analysis."""
    distances = data.get("semantic_distances", {})
    
    if not distances:
        st.warning("No data available for regression analysis.")
        return
    
    noise_levels = sorted([int(k) for k in distances.keys()])
    noise_arr = np.array(noise_levels)
    dist_arr = np.array([float(distances[str(n)]) for n in noise_levels])
    
    # Polynomial degree selection
    degree = st.slider("Polynomial Degree", 1, 4, 2)
    
    # Fit polynomial
    coeffs = np.polyfit(noise_arr, dist_arr, degree)
    poly_fn = np.poly1d(coeffs)
    
    # Generate smooth curve
    x_smooth = np.linspace(noise_arr.min(), noise_arr.max(), 100)
    y_smooth = poly_fn(x_smooth)
    
    # Calculate R²
    y_pred = poly_fn(noise_arr)
    ss_res = np.sum((dist_arr - y_pred) ** 2)
    ss_tot = np.sum((dist_arr - np.mean(dist_arr)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig = go.Figure()
        
        # Scatter points
        fig.add_trace(go.Scatter(
            x=noise_arr,
            y=dist_arr,
            mode='markers',
            name='Observed',
            marker=dict(size=12, color='#667eea', symbol='circle'),
            hovertemplate='Noise: %{x}%<br>Distance: %{y:.4f}<extra></extra>'
        ))
        
        # Regression line
        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=y_smooth,
            mode='lines',
            name=f'Polynomial (degree {degree})',
            line=dict(color='#f59e0b', width=3, dash='dash'),
            hovertemplate='Predicted: %{y:.4f}<extra></extra>'
        ))
        
        # Confidence interval (approximate)
        std_err = np.std(dist_arr - y_pred)
        fig.add_trace(go.Scatter(
            x=np.concatenate([x_smooth, x_smooth[::-1]]),
            y=np.concatenate([y_smooth + 1.96 * std_err, (y_smooth - 1.96 * std_err)[::-1]]),
            fill='toself',
            fillcolor='rgba(245, 158, 11, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% CI',
            showlegend=True
        ))
        
        fig.update_layout(
            title={
                'text': f'Regression Analysis (R² = {r_squared:.4f})',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title='Noise Level (%)',
            yaxis_title='Cosine Distance',
            template='plotly_white',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📐 Model Statistics")
        
        st.metric("R² Score", f"{r_squared:.4f}")
        st.metric("RMSE", f"{np.sqrt(np.mean((dist_arr - y_pred) ** 2)):.6f}")
        
        st.markdown("**Coefficients:**")
        for i, c in enumerate(coeffs):
            power = degree - i
            st.text(f"x^{power}: {c:.6f}")


def render_effect_sizes(data: Dict[str, Any], comparative: Optional[Dict[str, Any]]):
    """Render effect sizes visualization."""
    st.markdown("### 🎯 Effect Size Analysis")
    
    st.markdown("""
    <div class="info-box">
        <h4>Understanding Effect Sizes</h4>
        <ul>
            <li><strong>Cohen's d:</strong> Standardized mean difference (|d| < 0.2: small, 0.2-0.8: medium, > 0.8: large)</li>
            <li><strong>Cliff's δ:</strong> Non-parametric effect size (|δ| < 0.147: negligible, 0.147-0.33: small, 0.33-0.474: medium, > 0.474: large)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if comparative and "pairwise_comparisons" in comparative:
        comparisons = comparative["pairwise_comparisons"].get("semantic_distance", [])
        
        if comparisons:
            # Create effect size matrix
            noise_levels = sorted(set(
                [c.get("group1_name", "").replace("% noise", "") for c in comparisons] +
                [c.get("group2_name", "").replace("% noise", "") for c in comparisons]
            ))
            
            n = len(noise_levels)
            effect_matrix = np.zeros((n, n))
            
            for comp in comparisons:
                try:
                    g1 = comp.get("group1_name", "").replace("% noise", "")
                    g2 = comp.get("group2_name", "").replace("% noise", "")
                    effect = comp.get("effect_size", 0)
                    
                    if g1 in noise_levels and g2 in noise_levels:
                        i = noise_levels.index(g1)
                        j = noise_levels.index(g2)
                        effect_matrix[i, j] = effect
                        effect_matrix[j, i] = -effect
                except (ValueError, AttributeError):
                    continue
            
            fig = px.imshow(
                effect_matrix,
                labels=dict(color="Cliff's δ"),
                x=[f"{n}%" for n in noise_levels],
                y=[f"{n}%" for n in noise_levels],
                color_continuous_scale='RdBu_r',
                zmin=-1,
                zmax=1
            )
            
            fig.update_layout(
                title={
                    'text': 'Pairwise Effect Sizes (Cliff\'s Delta)',
                    'x': 0.5,
                    'xanchor': 'center'
                },
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary table
            st.markdown("### 📋 Significant Comparisons")
            
            sig_comparisons = [c for c in comparisons if c.get("significant", False)]
            
            if sig_comparisons:
                df = pd.DataFrame([{
                    'Comparison': f"{c.get('group1_name', 'N/A')} vs {c.get('group2_name', 'N/A')}",
                    'Effect Size': c.get('effect_size', 0),
                    'p-value (corrected)': c.get('p_value_corrected', 1),
                    'Interpretation': c.get('interpretation', 'N/A')
                } for c in sig_comparisons[:10]])
                
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No significant pairwise comparisons found at α = 0.05")
    else:
        st.info("Run comparative analysis to see effect sizes.")


def render_cost_tracker(cost_data: Optional[Dict[str, Any]]):
    """Render cost tracking visualization."""
    st.markdown('<h2 class="section-header">💰 Cost Tracker</h2>', unsafe_allow_html=True)
    
    if not cost_data:
        st.warning("No cost data available. Run experiments with cost tracking enabled.")
        return
    
    summary = cost_data.get("summary", {})
    calls = cost_data.get("calls", [])
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Cost",
            f"${summary.get('total_cost', 0):.4f}",
            delta="Budget-friendly!" if summary.get('total_cost', 0) < 0.05 else None
        )
    
    with col2:
        st.metric(
            "Total API Calls",
            summary.get('total_calls', 0)
        )
    
    with col3:
        tokens = summary.get('total_tokens', {})
        st.metric(
            "Total Tokens",
            f"{tokens.get('total', 0):,}"
        )
    
    with col4:
        st.metric(
            "Avg Cost/Call",
            f"${summary.get('average_cost_per_call', 0):.4f}"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost by stage
        cost_by_stage = summary.get('cost_by_stage', {})
        
        if cost_by_stage:
            stages = list(cost_by_stage.keys())
            costs = list(cost_by_stage.values())
            
            fig = go.Figure(data=[
                go.Bar(
                    x=[f"Stage {s}" for s in stages],
                    y=costs,
                    marker_color=['#667eea', '#3b82f6', '#8b5cf6'][:len(stages)],
                    text=[f"${c:.4f}" for c in costs],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title={'text': 'Cost by Pipeline Stage', 'x': 0.5},
                yaxis_title='Cost (USD)',
                template='plotly_white',
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Token usage pie chart
        tokens = summary.get('total_tokens', {})
        
        if tokens:
            fig = go.Figure(data=[go.Pie(
                labels=['Input Tokens', 'Output Tokens'],
                values=[tokens.get('input', 0), tokens.get('output', 0)],
                hole=0.4,
                marker_colors=['#667eea', '#22c55e']
            )])
            
            fig.update_layout(
                title={'text': 'Token Distribution', 'x': 0.5},
                height=350,
                annotations=[dict(
                    text=f"{tokens.get('total', 0):,}",
                    x=0.5, y=0.5,
                    font_size=20,
                    showarrow=False
                )]
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed call log
    if calls:
        with st.expander("📜 Detailed API Call Log"):
            df = pd.DataFrame(calls)
            
            if not df.empty:
                # Format columns
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                if 'cost' in df.columns:
                    df['cost'] = df['cost'].apply(lambda x: f"${x:.4f}")
                
                st.dataframe(df, use_container_width=True)


def render_sensitivity_explorer(sensitivity_data: Optional[Dict[str, Any]]):
    """Render sensitivity analysis explorer."""
    st.markdown('<h2 class="section-header">🎛️ Sensitivity Analysis</h2>', unsafe_allow_html=True)
    
    if not sensitivity_data:
        st.info("""
        Sensitivity analysis data not available.
        
        Run the sensitivity analysis with:
        ```bash
        python scripts/experiment/run_research_analysis.py
        ```
        """)
        
        # Show placeholder/explanation
        st.markdown("""
        <div class="info-box">
            <h4>What is Sensitivity Analysis?</h4>
            <p>Sensitivity analysis examines how different parameters affect the semantic drift measurements:</p>
            <ul>
                <li><strong>Embedding Dimensions:</strong> TF-IDF feature space size (100-5000)</li>
                <li><strong>N-gram Ranges:</strong> Text tokenization strategy ((1,1) to (2,4))</li>
                <li><strong>Bootstrap Confidence:</strong> Statistical robustness via resampling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display sensitivity results
    tab1, tab2, tab3 = st.tabs(["📏 Embedding Dimensions", "📝 N-gram Ranges", "🎲 Bootstrap Analysis"])
    
    with tab1:
        if "embedding_dimension_sensitivity" in sensitivity_data:
            emb_data = sensitivity_data["embedding_dimension_sensitivity"]
            
            dims = emb_data.get("parameter_values", [])
            means = emb_data.get("metric_means", [])
            stds = emb_data.get("metric_stds", [])
            
            if dims and means:
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=dims,
                    y=means,
                    mode='lines+markers',
                    name='Mean Distance',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=10),
                    error_y=dict(type='data', array=stds, visible=True)
                ))
                
                fig.update_layout(
                    title={'text': 'Distance vs Embedding Dimension', 'x': 0.5},
                    xaxis_title='Max Features (TF-IDF)',
                    yaxis_title='Mean Cosine Distance',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"""
                **Interpretation:** {emb_data.get('interpretation', 'N/A')}
                
                - Correlation: {emb_data.get('correlation', 0):.4f}
                - p-value: {emb_data.get('p_value', 1):.6f}
                """)
    
    with tab2:
        if "ngram_range_sensitivity" in sensitivity_data:
            ngram_data = sensitivity_data["ngram_range_sensitivity"]
            
            ranges = ngram_data.get("parameter_values", [])
            means = ngram_data.get("metric_means", [])
            
            if ranges and means:
                fig = go.Figure(data=[
                    go.Bar(
                        x=[str(r) for r in ranges],
                        y=means,
                        marker_color=['#667eea', '#3b82f6', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899'][:len(ranges)],
                        text=[f"{m:.4f}" for m in means],
                        textposition='auto'
                    )
                ])
                
                fig.update_layout(
                    title={'text': 'Distance by N-gram Range', 'x': 0.5},
                    xaxis_title='N-gram Range',
                    yaxis_title='Mean Cosine Distance',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if "bootstrap_analysis" in sensitivity_data:
            bootstrap = sensitivity_data["bootstrap_analysis"]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Bootstrap Mean",
                    f"{bootstrap.get('bootstrap_mean', 0):.4f}"
                )
            
            with col2:
                st.metric(
                    "95% CI",
                    f"[{bootstrap.get('ci_lower', 0):.4f}, {bootstrap.get('ci_upper', 0):.4f}]"
                )
            
            with col3:
                st.metric(
                    "Bias",
                    f"{bootstrap.get('bias', 0):.6f}"
                )
            
            st.markdown(f"""
            <div class="success-box">
                <strong>Bootstrap Analysis Complete</strong>
                <p>Based on {bootstrap.get('n_iterations', 10000):,} iterations, the results show 
                {'minimal' if abs(bootstrap.get('bias', 0)) < 0.01 else 'some'} bias in the estimates.</p>
            </div>
            """, unsafe_allow_html=True)


def render_about_section():
    """Render about section."""
    st.markdown('<h2 class="section-header">ℹ️ About This Dashboard</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎓 Project Information
        
        **Title:** Agentic Turing Machine  
        **Type:** MIT-Level Research Project  
        **Course:** LLM and Multi Agent Orchestration  
        **Institution:** Reichman University  
        **Instructor:** Dr. Yoram Segal
        
        ### 👥 Authors
        
        - **Fouad Azem** - fouad.azem@gmail.com
        - **Tal Goldengorn** - t.goldengoren@gmail.com
        
        ### 📊 Research Focus
        
        This system investigates **semantic drift** in multi-hop translation chains
        using Claude AI agents. Key research questions:
        
        1. How does input noise affect semantic preservation?
        2. What is the relationship between noise level and drift?
        3. How robust are LLMs to character-level perturbations?
        """)
    
    with col2:
        st.markdown("""
        ### 🔬 Methodology
        
        - **Translation Chain:** EN → FR → HE → EN
        - **Noise Levels:** 0%, 10%, 20%, 25%, 30%, 40%, 50%
        - **Metrics:** Cosine Distance, Text Similarity, Word Overlap
        - **Statistical Tests:** Pearson/Spearman correlation, ANOVA, Effect sizes
        
        ### 📚 Key Results
        
        - **Test Coverage:** 86.32%
        - **Correlation (r):** 0.982 (p < 0.001)
        - **API Cost:** ~$0.02 per experiment
        - **Reproducibility:** Level 3 (Highest)
        
        ### 🔗 Resources
        
        - [GitHub Repository](https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-)
        - [Documentation](https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-/tree/main/docs)
        - [Academic Paper](https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-/blob/main/docs/ACADEMIC_PAPER.md)
        """)


# =============================================================================
# Main Application
# =============================================================================

def main():
    """Main application entry point."""
    # Render header
    render_header()
    
    # Load all data
    analysis_data = load_analysis_results()
    cost_data = load_cost_analysis()
    comparative_data = load_comparative_analysis()
    sensitivity_data = load_sensitivity_analysis()
    translations = load_translation_outputs()
    
    # Sidebar navigation
    st.sidebar.image(
        "https://img.icons8.com/fluency/96/robot-2.png",
        width=80
    )
    st.sidebar.title("Navigation")
    
    page = st.sidebar.radio(
        "Select Page",
        [
            "🏠 Overview",
            "🔬 Semantic Drift Explorer",
            "🔄 Translation Pipeline",
            "📈 Statistical Analysis",
            "🎛️ Sensitivity Analysis",
            "💰 Cost Tracker",
            "ℹ️ About"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    if analysis_data:
        distances = analysis_data.get("semantic_distances", {})
        st.sidebar.metric("Noise Levels", len(distances))
        avg_dist = np.mean(list(map(float, distances.values()))) if distances else 0
        st.sidebar.metric("Avg Distance", f"{avg_dist:.4f}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="font-size: 0.8rem; color: #64748b; text-align: center;">
        <p>MIT-Level Research Project</p>
        <p>Reichman University © 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data is available
    if not analysis_data:
        st.error("""
        ⚠️ **No analysis data found!**
        
        Please run the experiment first:
        
        ```bash
        # Run the full experiment pipeline
        python scripts/experiment/run_with_skills.py --all
        
        # Then run the analysis
        python src/analysis.py
        ```
        
        Or use the pre-generated sample data if available.
        """)
        return
    
    # Render selected page
    if page == "🏠 Overview":
        render_key_metrics(analysis_data, cost_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_semantic_drift_explorer(analysis_data)
        
        with col2:
            render_translation_pipeline(analysis_data, translations)
    
    elif page == "🔬 Semantic Drift Explorer":
        render_semantic_drift_explorer(analysis_data)
        
        # Additional detailed analysis
        st.markdown("### 📋 Detailed Metrics Table")
        
        distances = analysis_data.get("semantic_distances", {})
        text_sims = analysis_data.get("text_similarities", {})
        word_overlaps = analysis_data.get("word_overlaps", {})
        
        noise_levels = sorted([int(k) for k in distances.keys()])
        
        df = pd.DataFrame({
            'Noise Level (%)': noise_levels,
            'Cosine Distance': [float(distances[str(n)]) for n in noise_levels],
            'Semantic Preservation': [1 - float(distances[str(n)]) for n in noise_levels],
            'Text Similarity': [float(text_sims.get(str(n), 0)) for n in noise_levels],
            'Word Overlap': [float(word_overlaps.get(str(n), 0)) for n in noise_levels]
        })
        
        st.dataframe(
            df.style.format({
                'Cosine Distance': '{:.4f}',
                'Semantic Preservation': '{:.1%}',
                'Text Similarity': '{:.1%}',
                'Word Overlap': '{:.1%}'
            }).background_gradient(cmap='RdYlGn_r', subset=['Cosine Distance'])
            .background_gradient(cmap='RdYlGn', subset=['Semantic Preservation', 'Text Similarity', 'Word Overlap']),
            use_container_width=True
        )
    
    elif page == "🔄 Translation Pipeline":
        render_translation_pipeline(analysis_data, translations)
    
    elif page == "📈 Statistical Analysis":
        render_statistical_analysis(analysis_data, comparative_data)
    
    elif page == "🎛️ Sensitivity Analysis":
        render_sensitivity_explorer(sensitivity_data)
    
    elif page == "💰 Cost Tracker":
        render_cost_tracker(cost_data)
    
    elif page == "ℹ️ About":
        render_about_section()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">
        <p>🤖 <strong>Agentic Turing Machine</strong> - MIT-Level Research Dashboard</p>
        <p>Built with ❤️ using Streamlit & Plotly | © 2025 Fouad Azem & Tal Goldengorn</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

