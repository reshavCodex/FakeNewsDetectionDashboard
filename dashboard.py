import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ── Plotly dark theme config ─────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#b8a8d0", size=12),
    title_font=dict(family="Inter, sans-serif", color="#ede9fe", size=15, weight=600) if hasattr(dict, '__init__') else dict(family="Inter, sans-serif", color="#ede9fe", size=15),
    legend=dict(
        bgcolor="rgba(30,10,60,0.55)",
        bordercolor="rgba(168,85,247,0.18)",
        borderwidth=1,
        font=dict(color="#b8a8d0", size=11),
    ),
    xaxis=dict(
        gridcolor="rgba(168,85,247,0.08)",
        tickfont=dict(color="#7c6d98", size=11),
        title_font=dict(color="#7c6d98"),
        linecolor="rgba(168,85,247,0.10)",
    ),
    yaxis=dict(
        gridcolor="rgba(168,85,247,0.08)",
        tickfont=dict(color="#7c6d98", size=11),
        title_font=dict(color="#7c6d98"),
        linecolor="rgba(168,85,247,0.10)",
    ),
    margin=dict(t=50, b=40, l=40, r=20),
)

BLUE_PALETTE = [
    "#a855f7", "#ec4899", "#8b5cf6", "#f472b6",
    "#c084fc", "#e879f9", "#fb7185",
]


def metric_card(value, label, accent_class="metric-card-accent"):
    return f"""
    <div class="metric-card {accent_class}">
        <div class="metric-card-value">{value}</div>
        <div class="metric-card-label">{label}</div>
    </div>
    """


def section_header(eyebrow, title, desc=""):
    desc_html = f'<div class="section-desc">{desc}</div>' if desc else ""
    return f"""
    <div class="section-eyebrow">{eyebrow}</div>
    <div class="section-title">{title}</div>
    {desc_html}
    """


def show_dashboard():

    # ── Load data ────────────────────────────────────────────────────────────
    try:
        df_dataset = pd.read_csv("data/D1.csv")
        df_results = pd.read_csv("data/model_comparison_results.csv")
    except Exception as e:
        st.error(f"Error loading data files: {e}")
        return

    # ── Top bar ──────────────────────────────────────────────────────────────
    col_title, col_home = st.columns([9, 1])

    with col_title:
        st.markdown("""
        <div style="padding: 20px 0 4px;">
            <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;
                         color:#c084fc;letter-spacing:0.14em;text-transform:uppercase;">
                Research Dashboard
            </span>
            <div style="font-size:22px;font-weight:700;color:#f5f0ff;
                        letter-spacing:-0.02em;margin-top:4px;">
                Fake News Detection — ML Comparative Study
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_home:
        st.markdown("<div style='padding-top:28px'>", unsafe_allow_html=True)
        if st.button("← Home", width='stretch'):
            st.session_state.page = "home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(168,85,247,0.18);margin:8px 0 24px'>",
        unsafe_allow_html=True
    )

    # ── Navigation ───────────────────────────────────────────────────────────
    if "section" not in st.session_state:
        st.session_state.section = "Dataset"

    SECTIONS = {
        "Dataset":          "📂  Dataset",
        "Methodology":      "⚙️  Methodology",
        "Model Comparison": "🤖  Models",
        "Results":          "📈  Results",
        "Conclusion":       "🏆  Conclusion",
    }

    nav_cols = st.columns(len(SECTIONS))
    for i, (key, label) in enumerate(SECTIONS.items()):
        with nav_cols[i]:
            if st.button(label, width='stretch', key=f"nav_{key}"):
                st.session_state.section = key

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(168,85,247,0.18);margin:16px 0 36px'>",
        unsafe_allow_html=True
    )

    option = st.session_state.section

    # ════════════════════════════════════════════════════════════════════════
    # DATASET
    # ════════════════════════════════════════════════════════════════════════
    if option == "Dataset":

        st.markdown(section_header(
            "01 — Data",
            "Dataset Overview",
            "Structure and distribution of the fake news corpus used for training and evaluation."
        ), unsafe_allow_html=True)

        fake_count, real_count = 0, 0
        if "class" in df_dataset.columns:
            fake_count = int((df_dataset["class"] == 0).sum())
            real_count = int((df_dataset["class"] == 1).sum())

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Records", f"{len(df_dataset):,}")
        c2.metric("Features", len(df_dataset.columns))
        c3.metric("Fake News", f"{fake_count:,}")
        c4.metric("Real News", f"{real_count:,}")

        # Dataset columns & preview
        col_a, col_b = st.columns([1, 2])

        with col_a:
            st.markdown("""
            <div style="font-size:12px;font-weight:600;color:#8b7aa8;
                        text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">
                Column Schema
            </div>
            """, unsafe_allow_html=True)
            columns_df = pd.DataFrame({"Column": df_dataset.columns,
                                       "Type": [str(t) for t in df_dataset.dtypes]})
            st.dataframe(columns_df, width='stretch', hide_index=True)

        with col_b:
            st.markdown("""
            <div style="font-size:12px;font-weight:600;color:#8b7aa8;
                        text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">
                Sample Records
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_dataset.head(8), width='stretch', hide_index=True)

        # Class distribution
        if "class" in df_dataset.columns:
            st.markdown(
                "<hr style='border:none;border-top:1px solid rgba(168,85,247,0.12);margin:28px 0'>",
                unsafe_allow_html=True
            )
            st.markdown("""
            <div style="font-size:12px;font-weight:600;color:#8b7aa8;
                        text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;">
                Class Distribution
            </div>
            """, unsafe_allow_html=True)

            class_counts = df_dataset["class"].value_counts().reset_index()
            class_counts.columns = ["class", "count"]
            class_counts["label"] = class_counts["class"].map({0: "Fake", 1: "Real"})

            col_pie, col_space = st.columns([1, 1])
            with col_pie:
                fig = px.pie(
                    class_counts,
                    values="count",
                    names="label",
                    color_discrete_sequence=["#a855f7", "#ec4899"],
                    hole=0.55,
                )
                fig.update_traces(
                    textfont=dict(color="#ede9fe", size=12),
                    marker=dict(line=dict(color="rgba(10,4,25,0.8)", width=3)),
                )
                fig.update_layout(
                    **PLOT_LAYOUT,
                    title="Fake vs Real News Distribution"
                )
                st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
                st.plotly_chart(fig, width='stretch')
                st.markdown('</div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # METHODOLOGY
    # ════════════════════════════════════════════════════════════════════════
    elif option == "Methodology":

        st.markdown(section_header(
            "02 — Pipeline",
            "Methodology",
            "End-to-end ML pipeline from raw text to model evaluation."
        ), unsafe_allow_html=True)

        steps = [
            ("Dataset",
             "Raw Input Data",
             "D1.csv — labelled fake/real news articles with text and class columns."),
            ("Preprocessing",
             "Text Preprocessing",
             "Tokenisation, stop-word removal, stemming/lemmatisation, and noise cleaning applied to raw article text."),
            ("Feature Extraction",
             "TF-IDF Feature Extraction",
             "Term Frequency–Inverse Document Frequency vectorisation converts text into numerical feature matrices."),
            ("Feature Selection",
             "Entropy-Based Feature Selection",
             "Information-gain / entropy criterion selects the most discriminative features, reducing noise and dimensionality."),
            ("Reduction",
             "Dimensionality Reduction",
             "Principal Component Analysis (PCA) and Singular Value Decomposition (SVD) compress the feature space while retaining variance."),
            ("Models",
             "Machine Learning Classifiers",
             "Seven models trained and evaluated: Logistic Regression · SVM · Random Forest · MLP · KNN · J48 · PART"),
            ("Evaluation",
             "Performance Evaluation",
             "Each model scored on Accuracy, Precision, Recall, F1 Score, and Cohen Kappa across all feature configurations."),
        ]

        for i, (num, title, desc) in enumerate(steps):
            st.markdown(f"""
            <div class="pipeline-step">
                <div class="pipeline-num">{str(i+1).zfill(2)}</div>
                <div class="pipeline-card">
                    <div class="pipeline-card-title">{title}</div>
                    <div class="pipeline-card-desc">{desc}</div>
                </div>
            </div>
            {"<div class='pipeline-arrow'>↓</div>" if i < len(steps)-1 else ""}
            """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════════════
    # MODEL COMPARISON
    # ════════════════════════════════════════════════════════════════════════
    elif option == "Model Comparison":

        st.markdown(section_header(
            "03 — Comparison",
            "Model Comparison",
            "Filter by feature set to compare classifier performance across all configurations."
        ), unsafe_allow_html=True)

        col_sel, col_info = st.columns([1, 2])

        with col_sel:
            feature_options = ["All"] + sorted(df_results["Feature"].unique().tolist())
            selected_feature = st.selectbox("Feature Set", feature_options)

        filtered_df = df_results.copy()
        if selected_feature != "All":
            filtered_df = filtered_df[filtered_df["Feature"] == selected_feature]

        # Summary stats row
        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(168,85,247,0.12);margin:16px 0 20px'>",
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Configurations", len(filtered_df))
        c2.metric("Models", filtered_df["Model"].nunique() if "Model" in filtered_df.columns else 0)
        c3.metric("Best Accuracy", f"{filtered_df['Accuracy'].max():.4f}" if "Accuracy" in filtered_df.columns else "—")
        c4.metric("Best F1", f"{filtered_df['F1'].max():.4f}" if "F1" in filtered_df.columns else "—")

        st.markdown("""
        <div style="font-size:12px;font-weight:600;color:#8b7aa8;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">
            Results Table
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(filtered_df, width='stretch', hide_index=True)

    # ════════════════════════════════════════════════════════════════════════
    # RESULTS
    # ════════════════════════════════════════════════════════════════════════
    elif option == "Results":

        st.markdown(section_header(
            "04 — Results",
            "Performance Results",
            "Comparative analysis of classifier performance. Select a metric and feature set to explore."
        ), unsafe_allow_html=True)

        best_row = df_results.loc[df_results["Accuracy"].idxmax()]

        # Best model banner
        st.markdown(f"""
        <div class="best-banner">
            <div class="best-banner-icon">🏆</div>
            <div>
                <div class="best-banner-text">Best Performing Model: {best_row['Model']}</div>
                <div class="best-banner-sub">
                    Feature Set: {best_row['Feature']} &nbsp;·&nbsp;
                    Accuracy: {best_row['Accuracy']:.4f} &nbsp;·&nbsp;
                    F1: {best_row['F1']:.4f}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Global best metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Best Accuracy", f"{df_results['Accuracy'].max():.4f}")
        c2.metric("Best Precision", f"{df_results['Precision'].max():.4f}")
        c3.metric("Best Recall", f"{df_results['Recall'].max():.4f}")
        c4.metric("Best F1 Score", f"{df_results['F1'].max():.4f}")

        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(168,85,247,0.12);margin:8px 0 24px'>",
            unsafe_allow_html=True
        )

        # Filters
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            feature_filter = st.selectbox(
                "Feature Set",
                ["All"] + sorted(df_results["Feature"].unique())
            )
        with col_f2:
            metric = st.selectbox(
                "Metric",
                ["Accuracy", "Precision", "Recall", "F1", "Kappa"]
            )

        filtered_results = df_results.copy()
        if feature_filter != "All":
            filtered_results = filtered_results[
                filtered_results["Feature"] == feature_filter
            ]

        # Bar chart
        fig = px.bar(
            filtered_results,
            x="Model",
            y=metric,
            color="Feature",
            barmode="group",
            color_discrete_sequence=BLUE_PALETTE,
            title=f"{metric} by Model & Feature Set",
        )
        fig.update_layout(**PLOT_LAYOUT)
        fig.update_traces(
            marker_line_width=0,
            opacity=0.9,
        )
        st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

        # Radar chart (per-model multi-metric) — show top 5 models
        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(168,85,247,0.12);margin:8px 0 24px'>",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div style="font-size:12px;font-weight:600;color:#8b7aa8;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;">
            Multi-Metric Radar — Top 5 Configurations by Accuracy
        </div>
        """, unsafe_allow_html=True)

        top5 = filtered_results.nlargest(5, "Accuracy")
        radar_metrics = ["Accuracy", "Precision", "Recall", "F1", "Kappa"]
        radar_fig = go.Figure()
        for i, (_, row) in enumerate(top5.iterrows()):
            vals = [row.get(m, 0) for m in radar_metrics]
            vals.append(vals[0])
            radar_fig.add_trace(go.Scatterpolar(
                r=vals,
                theta=radar_metrics + [radar_metrics[0]],
                name=f"{row['Model']} / {row['Feature']}",
                fill="toself",
                opacity=0.55,
                line=dict(color=BLUE_PALETTE[i % len(BLUE_PALETTE)], width=2),
            ))
        radar_fig.update_layout(
            **PLOT_LAYOUT,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor="rgba(168,85,247,0.10)",
                    tickfont=dict(color="#6b5a88", size=9),
                    linecolor="rgba(168,85,247,0.10)",
                ),
                angularaxis=dict(
                    tickfont=dict(color="#b8a8d0", size=11),
                    linecolor="rgba(168,85,247,0.14)",
                    gridcolor="rgba(168,85,247,0.08)",
                ),
            ),
            title="",
        )
        st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
        st.plotly_chart(radar_fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

        # Top 10 table
        st.markdown(f"""
        <div style="font-size:12px;font-weight:600;color:#8b7aa8;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">
            Top 10 by {metric}
        </div>
        """, unsafe_allow_html=True)

        top10 = filtered_results.sort_values(metric, ascending=False).head(10)
        st.dataframe(top10, width='stretch', hide_index=True)

        st.download_button(
            "📥 Download Full Results CSV",
            df_results.to_csv(index=False),
            file_name="model_comparison_results.csv",
            mime="text/csv",
        )

    # ════════════════════════════════════════════════════════════════════════
    # CONCLUSION
    # ════════════════════════════════════════════════════════════════════════
    elif option == "Conclusion":

        st.markdown(section_header(
            "05 — Summary",
            "Conclusion",
            "Key findings and the best-performing configuration identified in this study."
        ), unsafe_allow_html=True)

        best_row = df_results.loc[df_results["Accuracy"].idxmax()]

        # Best model card
        rows_html = "".join([
            f'<div class="conclusion-row"><span class="conclusion-key">Best Model</span>'
            f'<span class="conclusion-val">{best_row["Model"]}</span></div>',
            f'<div class="conclusion-row"><span class="conclusion-key">Feature Set</span>'
            f'<span class="conclusion-val">{best_row["Feature"]}</span></div>',
            f'<div class="conclusion-row"><span class="conclusion-key">Accuracy</span>'
            f'<span class="conclusion-val">{best_row["Accuracy"]:.4f}</span></div>',
            f'<div class="conclusion-row"><span class="conclusion-key">Precision</span>'
            f'<span class="conclusion-val">{best_row["Precision"]:.4f}</span></div>',
            f'<div class="conclusion-row"><span class="conclusion-key">Recall</span>'
            f'<span class="conclusion-val">{best_row["Recall"]:.4f}</span></div>',
            f'<div class="conclusion-row"><span class="conclusion-key">F1 Score</span>'
            f'<span class="conclusion-val">{best_row["F1"]:.4f}</span></div>',
            f'<div class="conclusion-row"><span class="conclusion-key">Cohen Kappa</span>'
            f'<span class="conclusion-val">{best_row["Kappa"]:.4f}</span></div>',
        ])

        st.markdown(f"""
        <div class="conclusion-card">
            <div class="conclusion-card-title">Best Configuration</div>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)

        # Key observations
        col_k1, col_k2 = st.columns(2)

        with col_k1:
            st.markdown(f"""
            <div class="finding-card">
                <div class="finding-card-label">🔍 Key Finding</div>
                <div class="finding-card-text">
                    {best_row['Model']} achieved the highest accuracy
                    ({best_row['Accuracy']:.4f}) when combined with the
                    <strong style="color:#ede9fe">{best_row['Feature']}</strong> feature
                    pipeline, outperforming all other model–feature combinations evaluated
                    in this study.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_k2:
            st.markdown(f"""
            <div class="finding-card">
                <div class="finding-card-label">📌 Feature Engineering Impact</div>
                <div class="finding-card-text">
                    TF-IDF combined with entropy-based feature selection and dimensionality
                    reduction (PCA / SVD) consistently produced the strongest feature
                    representations, demonstrating the value of a structured preprocessing
                    pipeline for NLP classification tasks.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="finding-card" style="margin-top:0">
            <div class="finding-card-label">🚀 Future Scope</div>
            <div class="finding-card-text">
                Future work may explore transformer-based language models (BERT, RoBERTa)
                for richer contextual feature extraction, cross-domain evaluation on diverse
                datasets, real-time inference pipelines, and ensemble methods that combine
                multiple classifiers to further improve detection robustness.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Overall accuracy comparison chart
        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(168,85,247,0.12);margin:24px 0'>",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div style="font-size:12px;font-weight:600;color:#8b7aa8;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;">
            Accuracy Overview — All Configurations
        </div>
        """, unsafe_allow_html=True)

        fig = px.bar(
            df_results.sort_values("Accuracy", ascending=True).tail(20),
            x="Accuracy",
            y="Model",
            color="Feature",
            orientation="h",
            color_discrete_sequence=BLUE_PALETTE,
            title="Top 20 Configurations by Accuracy",
        )
        fig.update_layout(**PLOT_LAYOUT)
        fig.update_traces(marker_line_width=0, opacity=0.9)
        st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)