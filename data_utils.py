import pandas as pd
import numpy as np

MODULES = ["Orientation","Python Basics","Data Cleaning","EDA","Statistics","ML Foundations","Model Evaluation","Dashboarding","Capstone"]
TOPICS = ["Foundations","Programming","Analytics","Statistics","Machine Learning","Visualization","Project Work"]

def generate_synthetic_learning_data(n_learners=450, seed=7):
    rng = np.random.default_rng(seed)
    rows=[]
    end = pd.Timestamp.today().normalize()
    for lid in range(1, n_learners+1):
        ability = rng.normal(0,1)
        start = end - pd.Timedelta(days=int(rng.integers(20,220)))
        last_module = int(np.clip(rng.normal(5+ability,2), 1, len(MODULES)))
        for m_idx, mod in enumerate(MODULES[:last_module], 1):
            attempts = int(np.clip(rng.poisson(1.2-ability*.15)+1,1,5))
            difficulty = ["Beginner","Intermediate","Advanced"][min(2, max(0, (m_idx-1)//3))]
            score = np.clip(rng.normal(68+ability*9-m_idx*1.2, 12), 20, 100)
            completed = int(score >= rng.normal(55,7))
            date = start + pd.Timedelta(days=int(m_idx*rng.integers(4,14)))
            rows.append([f"L{lid:04d}", date, mod, TOPICS[min(len(TOPICS)-1,m_idx-1)], difficulty, round(score,1), int(rng.gamma(2,22)), completed, attempts])
    return pd.DataFrame(rows, columns=["learner_id","activity_date","module","topic","difficulty","score","time_spent_min","completed","attempts"])

def prepare_learning_data(df):
    df=df.copy()
    cols={c.lower().strip().replace(" ","_"):c for c in df.columns}
    def pick(names):
        for n in names:
            if n in cols: return cols[n]
        return None
    n=len(df); out=pd.DataFrame()
    out["learner_id"]=df[pick(["learner_id","student_id","user_id","id"])].astype(str) if pick(["learner_id","student_id","user_id","id"]) else [f"L{i:04d}" for i in range(n)]
    out["activity_date"]=pd.to_datetime(df[pick(["activity_date","date","timestamp","created_date"])], errors="coerce") if pick(["activity_date","date","timestamp","created_date"]) else pd.Timestamp.today()
    out["module"]=df[pick(["module","lesson","course_module","content"])].astype(str) if pick(["module","lesson","course_module","content"]) else np.random.choice(MODULES,n)
    out["topic"]=df[pick(["topic","subject","category"])].astype(str) if pick(["topic","subject","category"]) else "General"
    out["difficulty"]=df[pick(["difficulty","level"])].astype(str) if pick(["difficulty","level"]) else "Intermediate"
    out["score"]=pd.to_numeric(df[pick(["score","marks","grade","percentage"])], errors="coerce") if pick(["score","marks","grade","percentage"]) else np.random.normal(70,12,n)
    out["time_spent_min"]=pd.to_numeric(df[pick(["time_spent_min","duration_min","minutes"])], errors="coerce") if pick(["time_spent_min","duration_min","minutes"]) else np.random.gamma(2,25,n)
    out["completed"]=pd.to_numeric(df[pick(["completed","is_completed","completion"])], errors="coerce") if pick(["completed","is_completed","completion"]) else (out["score"]>=55).astype(int)
    out["attempts"]=pd.to_numeric(df[pick(["attempts","attempt_count","tries"])], errors="coerce") if pick(["attempts","attempt_count","tries"]) else 1
    out["activity_date"]=out["activity_date"].fillna(pd.Timestamp.today())
    out["score"]=out["score"].fillna(out["score"].median()).clip(0,100)
    out["completed"]=out["completed"].fillna(0).astype(int)
    out["attempts"]=out["attempts"].fillna(1).clip(1,10)
    return out

def learner_summary(df):
    g=df.groupby("learner_id").agg(
        modules_seen=("module","nunique"),
        avg_score=("score","mean"),
        total_time=("time_spent_min","sum"),
        completion_rate=("completed","mean"),
        attempts=("attempts","sum"),
        last_activity=("activity_date","max")
    ).reset_index()
    g["engagement_score"]=(g["modules_seen"].rank(pct=True)*30 + g["completion_rate"]*35 + (g["avg_score"]/100)*25 + (1-g["attempts"].rank(pct=True))*10).round(1)
    g["path_stage"]=pd.cut(g["modules_seen"], bins=[0,2,5,99], labels=["Starter","Builder","Capstone-ready"])
    return g

def recommend_modules(df, learner_id=None):
    if learner_id and learner_id in set(df["learner_id"]):
        done=set(df[df["learner_id"]==learner_id]["module"])
    else:
        done=set()
    rec=[m for m in MODULES if m not in done]
    return rec[:3] if rec else ["Capstone Practice","Portfolio Review","Peer Teaching"]

def date_filter(df, mode):
    if mode=="All Data": return df
    days={"Last 30 Days":30,"Last 90 Days":90,"Last 180 Days":180}[mode]
    return df[df["activity_date"] >= df["activity_date"].max()-pd.Timedelta(days=days)]
