import streamlit as st
import plotly.express as px

def show_pincode_map(mandal_df, anomaly_df):
    st.subheader("🗺️ Pincode-wise Enrolment Intensity Map")

    if mandal_df.empty:
        st.warning("No data available for selected filters.")
        return

    # Aggregate data
    map_df = (
        mandal_df.groupby("pincode")["Total_Enrolments"]
        .sum()
        .reset_index()
    )

    # Mark anomaly pincodes
    anomaly_pins = (
        anomaly_df["pincode"].unique().tolist()
        if anomaly_df is not None and not anomaly_df.empty
        else []
    )

    map_df["Status"] = map_df["pincode"].apply(
        lambda x: "Anomaly" if x in anomaly_pins else "Normal"
    )

    # Boxed card layout
    with st.container(border=True):
        fig = px.scatter(
            map_df,
            x="pincode",
            y="Total_Enrolments",
            size="Total_Enrolments",
            color="Status",
            color_discrete_map={
                "Normal": "#2ecc71",
                "Anomaly": "#e74c3c"
            },
            hover_data={
                "pincode": True,
                "Total_Enrolments": True,
                "Status": True
            },
            title="Pincode Enrolment Density (Size = Volume)"
        )

        fig.update_layout(
            xaxis_title="Pincode",
            yaxis_title="Total Enrolments",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)
