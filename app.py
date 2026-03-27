import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# ================= PAGE CONFIG =================
st.set_page_config(page_title="World Dashboard", layout="wide")

# ================= SIDEBAR =================
st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Clustering Analysis"])

# ================= LOAD DATA =================
df = pd.read_excel("World_development_mesurement.xlsx")
df.columns = df.columns.str.strip()

# ================= CLEAN =================
def clean_numeric(col):
    return pd.to_numeric(
        df[col].astype(str).str.replace('[\$,]', '', regex=True),
        errors='coerce'
    )

for col in ["GDP", "Population Total", "CO2 Emissions"]:
    if col in df.columns:
        df[col] = clean_numeric(col)

# ================= INTERNET FIX =================
internet_col = None
for col in df.columns:
    if "internet" in col.lower():
        internet_col = col
        break

if internet_col:
    df[internet_col] = df[internet_col].astype(str).str.replace('%', '', regex=True)
    df[internet_col] = pd.to_numeric(df[internet_col], errors='coerce')
    df[internet_col] = df[internet_col].apply(
        lambda x: x * 100 if pd.notna(x) and x <= 1 else x
    )

# ================= DASHBOARD =================
if page == "Dashboard":

    st.markdown("<h1 style='text-align:center;'>🌍 World Development Dashboard</h1>", unsafe_allow_html=True)

    st.sidebar.subheader("🔍 Filters")
    country1 = st.sidebar.selectbox("Select Country", df["Country"].unique())
    country2 = st.sidebar.selectbox("Compare With", df["Country"].unique())

    df1 = df[df["Country"] == country1]
    df2 = df[df["Country"] == country2]

    # KPI
    col1, col2, col3 = st.columns(3)

    col1.metric("GDP", f"{df1['GDP'].values[0]/1_000_000:.2f} M")
    col2.metric("Population", f"{df1['Population Total'].values[0]/1_000_000:.2f} M")

    internet_val = df1[internet_col].values[0] if internet_col else 0
    col3.metric("Internet Usage (%)", f"{internet_val:.2f}%")

    # MAP
    st.subheader("🌍 Global Map")

    metric = st.selectbox("Select Metric", ["GDP", "Population Total", "CO2 Emissions"])

    fig_map = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color=metric,
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig_map, use_container_width=True)

    # COMPARISON
    st.subheader("📊 Country Comparison")

    fig = px.bar(
        x=[country1, country2],
        y=[df1[metric].values[0], df2[metric].values[0]],
        title=f"{metric} Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    # SCATTER
    st.subheader("📈 Scatter Analysis")

    x_axis = st.selectbox("X-axis", df.columns)
    y_axis = st.selectbox("Y-axis", df.columns)

    fig_scatter = px.scatter(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig_scatter, use_container_width=True)

# ================= CLUSTERING =================
elif page == "Clustering Analysis":

    st.markdown("<h1 style='text-align:center;'>🧠 Clustering Analysis</h1>", unsafe_allow_html=True)

    st.subheader("Select Features for Clustering")

    features = st.multiselect(
        "Choose Features",
        ["GDP", "Population Total", "CO2 Emissions"],
        default=["GDP", "Population Total"]
    )

    k = st.slider("Select Number of Clusters", 2, 6, 3)

    if len(features) >= 2:

        cluster_df = df[["Country"] + features].dropna()

        X = cluster_df[features]

        model = KMeans(n_clusters=k, random_state=42)
        cluster_df["Cluster"] = model.fit_predict(X)

        st.subheader("📊 Cluster Visualization")

        fig = px.scatter(
            cluster_df,
            x=features[0],
            y=features[1],
            color=cluster_df["Cluster"].astype(str),
            hover_name="Country",
            title="Country Clustering"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📄 Cluster Data")
        st.dataframe(cluster_df)

    else:
        st.warning("Please select at least 2 features")

# ================= FOOTER =================
st.markdown("---")
st.markdown("<center>🚀 Ultimate Dashboard | Streamlit + Plotly</center>", unsafe_allow_html=True)