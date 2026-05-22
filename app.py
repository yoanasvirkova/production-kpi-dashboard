import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Production KPI Dashboard",
    layout="wide"
)

st.title("Production KPI Dashboard")
st.write("A dashboard for monitoring manufacturing KPIs using Python, pandas, matplotlib, and Streamlit.")

# Load data
df = pd.read_csv("production_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Create KPI columns
df["good_units"] = df["units_produced"] - df["defective_units"]
df["defect_rate"] = (df["defective_units"] / df["units_produced"]) * 100
df["efficiency"] = (df["units_produced"] / df["target_units"]) * 100

# Sidebar filters
st.sidebar.header("Filters")

selected_machine = st.sidebar.multiselect(
    "Select machine",
    options=df["machine"].unique(),
    default=df["machine"].unique()
)

selected_shift = st.sidebar.multiselect(
    "Select shift",
    options=df["shift"].unique(),
    default=df["shift"].unique()
)

start_date = st.sidebar.date_input(
    "Start date",
    df["date"].min()
)

end_date = st.sidebar.date_input(
    "End date",
    df["date"].max()
)

filtered_df = df[
    (df["machine"].isin(selected_machine)) &
    (df["shift"].isin(selected_shift)) &
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.error("No data available for the selected filters.")
    st.stop()

# KPI calculations
total_units = filtered_df["units_produced"].sum()
total_defects = filtered_df["defective_units"].sum()
avg_defect_rate = filtered_df["defect_rate"].mean()
avg_efficiency = filtered_df["efficiency"].mean()
total_downtime = filtered_df["downtime_minutes"].sum()
good_units = filtered_df["good_units"].sum()

# KPI cards
st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Units", int(total_units))
col2.metric("Good Units", int(good_units))
col3.metric("Defective Units", int(total_defects))
col4.metric("Avg Defect Rate", f"{avg_defect_rate:.2f}%")
col5.metric("Avg Efficiency", f"{avg_efficiency:.2f}%")
col6.metric("Total Downtime", f"{int(total_downtime)} min")

# Warnings
if avg_defect_rate > 4:
    st.warning("Defect rate is higher than recommended. Process improvement may be needed.")

if avg_efficiency < 95:
    st.warning("Average efficiency is below target.")

if total_downtime > 300:
    st.warning("Total downtime is high. Machine availability should be reviewed.")

# Data table
st.subheader("Production Data")
st.dataframe(filtered_df)

# Production trend chart
st.subheader("Units Produced Over Time")

daily_production = filtered_df.groupby("date")["units_produced"].sum()

fig, ax = plt.subplots()
ax.plot(daily_production.index, daily_production.values, marker="o")
ax.set_xlabel("Date")
ax.set_ylabel("Units Produced")
ax.set_title("Daily Production Trend")
plt.xticks(rotation=45)
st.pyplot(fig)

# Defect rate chart
st.subheader("Average Defect Rate by Machine")

machine_defects = filtered_df.groupby("machine")["defect_rate"].mean()

fig2, ax2 = plt.subplots()
ax2.bar(machine_defects.index, machine_defects.values)
ax2.set_xlabel("Machine")
ax2.set_ylabel("Average Defect Rate (%)")
ax2.set_title("Defect Rate by Machine")
st.pyplot(fig2)

# Downtime chart
st.subheader("Total Downtime by Machine")

machine_downtime = filtered_df.groupby("machine")["downtime_minutes"].sum()

fig3, ax3 = plt.subplots()
ax3.bar(machine_downtime.index, machine_downtime.values)
ax3.set_xlabel("Machine")
ax3.set_ylabel("Downtime Minutes")
ax3.set_title("Downtime by Machine")
st.pyplot(fig3)

# Efficiency chart
st.subheader("Average Efficiency by Machine")

machine_efficiency = filtered_df.groupby("machine")["efficiency"].mean()

fig4, ax4 = plt.subplots()
ax4.bar(machine_efficiency.index, machine_efficiency.values)
ax4.set_xlabel("Machine")
ax4.set_ylabel("Efficiency (%)")
ax4.set_title("Efficiency by Machine")
st.pyplot(fig4)

# Insights
st.subheader("Insights")

worst_defect_day = filtered_df.loc[filtered_df["defect_rate"].idxmax()]
best_efficiency_day = filtered_df.loc[filtered_df["efficiency"].idxmax()]
highest_downtime_day = filtered_df.loc[filtered_df["downtime_minutes"].idxmax()]

st.write(
    f"The highest defect rate was on {worst_defect_day['date'].date()} "
    f"for {worst_defect_day['machine']} during the {worst_defect_day['shift']} shift."
)

st.write(
    f"The best efficiency was on {best_efficiency_day['date'].date()} "
    f"for {best_efficiency_day['machine']} during the {best_efficiency_day['shift']} shift."
)

st.write(
    f"The highest downtime was on {highest_downtime_day['date'].date()} "
    f"for {highest_downtime_day['machine']} during the {highest_downtime_day['shift']} shift."
)

# Conclusion
st.subheader("Conclusion")

st.write("""
This dashboard helps production teams monitor important manufacturing KPIs such as output,
defect rate, efficiency, and downtime.

It can support faster decision-making and help identify areas for process improvement.
""")