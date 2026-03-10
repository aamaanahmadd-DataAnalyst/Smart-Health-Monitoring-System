import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

ANALYTICS_CSS = """
<style>
/* ---- KPI Cards ---- */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 1.4rem;
}
.kpi-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 22px 16px;
    text-align: center;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 90px; height: 90px;
    border-radius: 50%;
    opacity: 0.06;
    background: white;
}
.kpi-icon  { font-size: 1.6rem; margin-bottom: 8px; }
.kpi-value { font-size: 2rem; font-weight: 800; line-height: 1; margin-bottom: 4px; }
.kpi-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.6px; color: #95a5a6; }
.kpi-blue  { border-top: 3px solid #2980b9; }
.kpi-blue  .kpi-value { color: #3498db; }
.kpi-red   { border-top: 3px solid #e74c3c; }
.kpi-red   .kpi-value { color: #e74c3c; }
.kpi-green { border-top: 3px solid #2ecc71; }
.kpi-green .kpi-value { color: #2ecc71; }

/* ---- Health Banner ---- */
.health-banner {
    border-radius: 14px;
    padding: 18px 22px;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 0.95rem;
    font-weight: 500;
}
.hb-ok   { background: rgba(46,204,113,0.1);  border: 1px solid rgba(46,204,113,0.3);  color: #2ecc71; }
.hb-warn { background: rgba(231,76,60,0.1);    border: 1px solid rgba(231,76,60,0.3);    color: #e74c3c; }
.hb-icon { font-size: 1.8rem; flex-shrink: 0; }

/* ---- Section Title ---- */
.an-title {
    font-size: 1rem;
    font-weight: 700;
    color: #2980b9;
    margin: 1.4rem 0 0.6rem;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* ---- Prediction Log Table ---- */
.pred-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
    font-size: 0.88rem;
}
.pred-table th {
    background: rgba(41,128,185,0.3);
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.pred-table td {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: #ecf0f1;
}
.pred-table tr:hover td { background: rgba(255,255,255,0.04); }
.sev-low      { color: #2ecc71; font-weight: 600; }
.sev-mild     { color: #f1c40f; font-weight: 600; }
.sev-moderate { color: #e67e22; font-weight: 600; }
.sev-severe   { color: #e74c3c; font-weight: 600; }

/* ---- PDF Card ---- */
.pdf-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 24px 22px 10px 22px;
    margin-top: 1rem;
}
.pdf-header  { font-size: 1.1rem; font-weight: 700; color: #ecf0f1; margin-bottom: 4px; }
.pdf-sub     { font-size: 0.8rem; color: #7f8c8d; margin-bottom: 16px; }
.pdf-divider { height: 1px; background: rgba(255,255,255,0.07); margin-bottom: 4px; }

/* ---- Download Button ---- */
div[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #1a5e35, #27ae60) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.2s !important;
}
div[data-testid="stDownloadButton"] button:hover { opacity: 0.88 !important; }

/* ---- Responsive Mobile ---- */
@media (max-width: 768px) {
    .kpi-grid { grid-template-columns: 1fr !important; gap: 10px; }
    .kpi-card { padding: 16px 12px; }
    .kpi-value { font-size: 1.8rem; }
    .health-banner { flex-direction: column; text-align: center; padding: 14px; }
    .an-title { font-size: 0.92rem; }
    .pred-table th,
    .pred-table td { padding: 8px; font-size: 0.76rem; }
    .pdf-card { padding: 16px 14px 8px; }
    .pdf-header { font-size: 1rem; }
}

/* ---- Responsive Tablet ---- */
@media (min-width: 769px) and (max-width: 1024px) {
    .kpi-value { font-size: 1.6rem; }
    .kpi-grid  { gap: 10px; }
}
</style>
"""


def sev_class(s):
    return {
        "Low": "sev-low", "Mild": "sev-mild",
        "Moderate": "sev-moderate", "Severe": "sev-severe"
    }.get(s, "")


def show_health_analytics(history):

    st.subheader("📊 Health Analytics Dashboard")
    st.markdown(ANALYTICS_CSS, unsafe_allow_html=True)

    # ---- Empty State ----
    if len(history) == 0:
        st.markdown("""
        <div class="health-banner hb-ok">
            <span class="hb-icon">ℹ️</span>
            <span>No predictions made yet. Run a prediction from the sidebar first to see your analytics.</span>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.DataFrame(history)
    total     = len(df)
    high_risk = len(df[df["Severity"].isin(["Severe", "Moderate"])])
    avg_prob  = round(df["Probability"].mean(), 1)

    # ---- KPI Cards ----
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card kpi-blue">
            <div class="kpi-icon">🔬</div>
            <div class="kpi-value">{total}</div>
            <div class="kpi-label">Total Predictions</div>
        </div>
        <div class="kpi-card kpi-red">
            <div class="kpi-icon">🚨</div>
            <div class="kpi-value">{high_risk}</div>
            <div class="kpi-label">High Risk Alerts</div>
        </div>
        <div class="kpi-card kpi-green">
            <div class="kpi-icon">📈</div>
            <div class="kpi-value">{avg_prob}%</div>
            <div class="kpi-label">Avg Risk Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    
    # ---- Overall Health Banner ----
    if high_risk == 0:
        st.markdown("""
        <div class="health-banner hb-ok">
            <span class="hb-icon">✅</span>
            <span>All predictions show Low to Mild risk. Keep maintaining your healthy lifestyle!</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="health-banner hb-warn">
            <span class="hb-icon">⚠️</span>
            <span>{high_risk} high-risk prediction(s) detected. Please consult a healthcare provider for further evaluation.</span>
        </div>
        """, unsafe_allow_html=True)

    # ---- Charts ----
    st.markdown('<div class="an-title">📈 Risk Analysis Charts</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            df, x=df.index, y="Probability",
            color="Severity",
            hover_data=["Type", "Severity"],
            labels={"index": "Prediction #", "Probability": "Risk (%)"},
            color_discrete_map={
                "Low": "#2ecc71", "Mild": "#f1c40f",
                "Moderate": "#e67e22", "Severe": "#e74c3c"
            },
            template="plotly_dark",
            title="Prediction History"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=20, l=10, r=10),
            height=280, showlegend=True,
            legend=dict(font=dict(size=10))
        )
        fig.add_hline(y=60, line_dash="dash", line_color="rgba(231,76,60,0.5)",
                      annotation_text="High Risk", annotation_font_size=10)
        fig.add_hline(y=40, line_dash="dash", line_color="rgba(241,196,15,0.5)",
                      annotation_text="Mild Risk", annotation_font_size=10)
        st.plotly_chart(fig, width="stretch")

    with col2:
        sev_count = df["Severity"].value_counts().reset_index()
        sev_count.columns = ["Severity", "Count"]
        fig2 = px.pie(
            sev_count, names="Severity", values="Count", hole=0.6,
            color="Severity",
            color_discrete_map={
                "Low": "#2ecc71", "Mild": "#f1c40f",
                "Moderate": "#e67e22", "Severe": "#e74c3c"
            },
            title="Severity Distribution"
        )
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=40, b=20, l=10, r=10),
            height=280, legend=dict(font=dict(size=10))
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, width="stretch")

    # ---- Risk Trend Line (only if 2+ predictions) ----
    if len(df) >= 2:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=list(range(1, len(df)+1)),
            y=df["Probability"].tolist(),
            mode='lines+markers',
            line=dict(color='#3498db', width=2),
            marker=dict(
                size=8,
                color=["#2ecc71" if s == "Low" else "#f1c40f" if s == "Mild"
                       else "#e67e22" if s == "Moderate" else "#e74c3c"
                       for s in df["Severity"]],
                line=dict(color='white', width=1)
            ),
            hovertemplate="Prediction %{x}<br>Risk: %{y:.1f}%<extra></extra>"
        ))
        fig3.add_hrect(y0=0,  y1=40,  fillcolor="rgba(46,204,113,0.06)",  line_width=0)
        fig3.add_hrect(y0=40, y1=60,  fillcolor="rgba(241,196,15,0.06)",  line_width=0)
        fig3.add_hrect(y0=60, y1=80,  fillcolor="rgba(230,126,34,0.06)",  line_width=0)
        fig3.add_hrect(y0=80, y1=100, fillcolor="rgba(231,76,60,0.06)",   line_width=0)
        fig3.update_layout(
            template="plotly_dark",
            title="Risk Trend Over Time",
            xaxis_title="Prediction #",
            yaxis_title="Risk (%)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=220,
            margin=dict(t=40, b=20, l=10, r=10)
        )
        st.plotly_chart(fig3, width="stretch")

    # ---- Prediction Log Table ----
    st.markdown('<div class="an-title">📋 Prediction Log</div>', unsafe_allow_html=True)

    rows_html = ""
    for i, row in df.iterrows():
        sc = sev_class(row['Severity'])
        rows_html += f"""<tr>
            <td>{i+1}</td>
            <td>{row['Type']}</td>
            <td>{row['Probability']:.1f}%</td>
            <td class="{sc}">{row['Severity']}</td>
        </tr>"""

    st.markdown(f"""
    <table class="pred-table">
        <thead>
            <tr><th>#</th><th>Type</th><th>Risk Probability</th><th>Severity</th></tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- PDF Section ----
    st.markdown('<div class="an-title">📄 Generate Health Report</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="pdf-card">
        <div class="pdf-header">📄 Generate Health Report</div>
        <div class="pdf-sub">Enter patient details to generate a complete AI health report PDF</div>
        <div class="pdf-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        name = st.text_input("👤 Patient Name", placeholder="Enter full name")
    with col_b:
        age = st.number_input("🎂 Age", 1, 120, 25)
    with col_c:
        gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn, col_empty = st.columns([1, 2])
    with col_btn:
        generate = st.button("🖨️ Generate PDF Report", width="stretch")

    if generate:
        if name.strip() == "":
            st.warning("⚠️ Please enter patient name.")
            st.stop()
        if len(st.session_state.history) == 0:
            st.warning("⚠️ No prediction available. Please run a prediction first.")
            st.stop()

        with st.spinner("⏳ Generating your health report..."):
            os.makedirs("reports", exist_ok=True)
            file_path = f"reports/{name.replace(' ','_')}_health_report.pdf"
            _generate_pdf(file_path, name, age, gender, st.session_state.history)

        st.markdown("""
        <div style="background:rgba(46,204,113,0.1); border:1px solid rgba(46,204,113,0.3);
                    border-radius:12px; padding:14px 18px; color:#2ecc71;
                    font-weight:600; margin:10px 0; display:flex; align-items:center; gap:10px;">
            ✅ &nbsp; Report generated successfully! Click below to download.
        </div>
        """, unsafe_allow_html=True)

        with open(file_path, "rb") as file:
            st.download_button(
                label="⬇️  Download Health Report PDF",
                data=file,
                file_name=f"{name}_health_report.pdf",
                mime="application/pdf"
            )


# ================================================================
# PDF GENERATOR
# ================================================================

def _generate_pdf(file_path, name, age, gender, history):

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    subtitle_style = ParagraphStyle(
        'subtitle',
        fontSize=11,
        fontName='Helvetica',
        alignment=TA_CENTER,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=8
    )

    section_style = ParagraphStyle(
        'section',
        fontSize=13,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#2980b9'),
        spaceBefore=12,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        'normal',
        fontSize=10,
        fontName='Helvetica',
        textColor=colors.HexColor('#2c3e50'),
        leading=14
    )

    disclaimer_style = ParagraphStyle(
        'disclaimer',
        fontSize=8,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor('#7f8c8d'),
        leading=12
    )

    elements = []

    # HEADER
    header = Table(
        [["Smart Health Monitoring System"]],
        colWidths=[480]
    )

    header.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#2980b9')),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),18),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('BOTTOMPADDING',(0,0),(-1,-1),12),
        ('TOPPADDING',(0,0),(-1,-1),12)
    ]))

    elements.append(header)
    elements.append(Spacer(1,10))

    elements.append(
        Paragraph(
            "AI Powered Preventive Health Report",
            subtitle_style
        )
    )

    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2980b9")))

    elements.append(Spacer(1,20))

    # PATIENT INFO

    elements.append(Paragraph("Patient Information", section_style))

    high_risk_count = sum(1 for h in history if h["Severity"] in ["Severe","Moderate"])
    avg_prob = sum(h["Probability"] for h in history) / len(history)

    patient_data = [
        ["Patient Name", name],
        ["Age", str(age)],
        ["Gender", gender],
        ["Report Date", datetime.now().strftime("%d %B %Y %I:%M %p")],
        ["Total Predictions", str(len(history))],
        ["High Risk Alerts", str(high_risk_count)],
        ["Average Risk Score", f"{avg_prob:.1f}%"]
    ]

    patient_table = Table(patient_data, colWidths=[180,300])

    patient_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,-1),colors.HexColor("#eaf4fb")),
        ('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#d5d8dc")),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),
            [colors.white, colors.HexColor("#f8f9fa")])
    ]))

    elements.append(patient_table)

    elements.append(Spacer(1,20))

    # PREDICTION RESULTS

    elements.append(Paragraph("Prediction Results", section_style))

    table_data = [["#", "Prediction Type", "Risk %", "Severity"]]

    for i,h in enumerate(history,1):
        table_data.append([
            str(i),
            h["Type"],
            f"{h['Probability']:.1f}%",
            h["Severity"]
        ])

    result_table = Table(table_data, colWidths=[40,200,120,120])

    result_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#2980b9")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor("#d5d8dc")),
        ('ALIGN',(2,1),(2,-1),'CENTER'),
        ('ALIGN',(3,1),(3,-1),'CENTER')
    ]))

    elements.append(result_table)

    elements.append(Spacer(1,20))

    # PREMIUM RISK BARS

    elements.append(Paragraph("Risk Visualization", section_style))

    for h in history:

        prob = h["Probability"]

        if prob < 40:
            color = colors.HexColor("#2ecc71")
        elif prob < 60:
            color = colors.HexColor("#f1c40f")
        elif prob < 80:
            color = colors.HexColor("#e67e22")
        else:
            color = colors.HexColor("#e74c3c")

        bar_width = prob * 4

        bar = Table([[f"{h['Type']}  —  {prob:.1f}%"]], colWidths=[bar_width])

        bar.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),color),
            ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
            ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),
            ('LEFTPADDING',(0,0),(-1,-1),6),
            ('RIGHTPADDING',(0,0),(-1,-1),6),
            ('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4)
        ]))

        elements.append(bar)
        elements.append(Spacer(1,6))

    elements.append(Spacer(1,20))

    # HEALTH SUMMARY

    elements.append(Paragraph("Health Summary", section_style))

    if high_risk_count > 0:
        text = f"{high_risk_count} high risk predictions detected. Please consult a doctor."
        bg = colors.HexColor("#fdebd0")
    else:
        text = "All predictions indicate low risk. Maintain healthy lifestyle."
        bg = colors.HexColor("#d5f5e3")

    summary = Table([[Paragraph(text, normal_style)]], colWidths=[480])

    summary.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('PADDING',(0,0),(-1,-1),10)
    ]))

    elements.append(summary)

    elements.append(Spacer(1,20))

    elements.append(HRFlowable(width="100%", thickness=1))

    elements.append(Paragraph(
        "Medical Disclaimer: This AI report is for preventive awareness only and not a medical diagnosis.",
        disclaimer_style
    ))

    elements.append(Paragraph(
        "Smart Health Monitoring System | Integral University | B.Tech CSE 2025",
        disclaimer_style
    ))

    doc.build(elements)