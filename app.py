import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from data_utils import generate_synthetic_learning_data, prepare_learning_data, learner_summary, recommend_modules, date_filter

st.set_page_config(page_title="Learning Path Optimization Studio", page_icon="🧭", layout="wide")
st.markdown("""
<style>
.block-container {padding-top:1rem;}
.hero {background:linear-gradient(135deg,#312e81,#7c3aed); color:white; padding:22px; border-radius:20px; margin-bottom:14px;}
.hero * {color:white !important;}
.soft {background:#faf5ff; color:#3b0764; padding:12px; border-radius:12px; border:1px solid #e9d5ff;}
.soft * {color:#3b0764 !important;}
div[data-testid="stMetric"] {background:#faf5ff; border:1px solid #ddd6fe; border-radius:14px; padding:12px;}
div[data-testid="stMetric"] * {color:#2e1065 !important;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🧭 Learning Path Optimization Studio</h1><p>Analyze learner journeys, discover pathway patterns, and recommend next learning actions.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Learning Dataset")
    up=st.file_uploader("Upload learner activity CSV", type=["csv"])
    learners=st.slider("Demo learners", 100, 1200, 450, step=50)
    if up:
        try: df=prepare_learning_data(pd.read_csv(up)); src="Uploaded CSV"
        except Exception as e: st.error(e); df=generate_synthetic_learning_data(learners); src="Synthetic Demo"
    else:
        df=generate_synthetic_learning_data(learners); src="Synthetic Demo"
    st.success(src)
    period=st.selectbox("Activity window", ["All Data","Last 30 Days","Last 90 Days","Last 180 Days"])
    df=date_filter(df, period)
    topic_opts=["All Topics"]+sorted(df["topic"].dropna().unique().tolist())
    topic=st.selectbox("Topic focus", topic_opts)
    if topic!="All Topics": df=df[df["topic"]==topic]
    st.info(f"{len(df):,} learning records")

if df.empty:
    st.warning("No activity records available.")
    st.stop()

ls=learner_summary(df)
c1,c2,c3,c4=st.columns(4)
c1.metric("Learners", f"{ls['learner_id'].nunique():,}")
c2.metric("Avg Score", f"{df['score'].mean():.1f}")
c3.metric("Completion Rate", f"{df['completed'].mean()*100:.1f}%")
c4.metric("Avg Engagement", f"{ls['engagement_score'].mean():.1f}")

tab1,tab2,tab3,tab4=st.tabs(["Path Map","Learner Segments","Recommendation Studio","Intervention Notes"])
with tab1:
    st.subheader("Learning Path Map")
    prog=df.groupby("module").agg(records=("learner_id","count"), avg_score=("score","mean"), completion=("completed","mean")).reset_index()
    fig=px.bar(prog, x="module", y="records", color="completion", title="Module Participation and Completion Strength")
    st.plotly_chart(fig, use_container_width=True)
    fig=px.scatter(prog, x="avg_score", y="completion", size="records", hover_name="module", title="Module Difficulty / Completion View")
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.subheader("Learner Segments")
    if len(ls)>=3:
        X=ls[["modules_seen","avg_score","completion_rate","total_time"]].fillna(0)
        Xs=StandardScaler().fit_transform(X)
        k=min(4, len(ls))
        ls["segment"]=KMeans(n_clusters=k, random_state=3, n_init=10).fit_predict(Xs)
        fig=px.scatter(ls, x="avg_score", y="engagement_score", color="segment", size="modules_seen", hover_name="learner_id", title="Learner Engagement Segments")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(ls.sort_values("engagement_score").head(20), use_container_width=True, hide_index=True)
    else:
        st.info("Need at least 3 learners for segmentation.")
with tab3:
    st.subheader("Recommendation Studio")
    learner=st.selectbox("Select learner", ["Portfolio-level recommendation"]+sorted(ls["learner_id"].tolist()))
    lid=None if learner=="Portfolio-level recommendation" else learner
    recs=recommend_modules(df, lid)
    st.markdown('<div class="soft">Recommended next modules are based on completed modules and current pathway position.</div>', unsafe_allow_html=True)
    for i,r in enumerate(recs,1): st.write(f"**{i}. {r}**")
    if lid:
        st.dataframe(df[df["learner_id"]==lid].sort_values("activity_date"), use_container_width=True, hide_index=True)
with tab4:
    st.subheader("Intervention Notes")
    low=ls[ls["engagement_score"]<45]
    st.write(f"**{len(low)} learners** show low engagement signals in the selected view.")
    st.write("- Offer guided revision for modules with low completion.")
    st.write("- Recommend smaller next steps for Starter-stage learners.")
    st.write("- Use peer/project tasks for Builder-stage learners.")
    st.write("- Prioritize learners with low score and high attempts.")
    st.dataframe(df.head(80), use_container_width=True, hide_index=True)
