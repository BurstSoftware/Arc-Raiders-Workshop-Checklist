import streamlit as st
import pandas as pd

st.set_page_config(page_title="ARC Raiders Workshop Requirements", layout="wide")

st.title("🔧 ARC Raiders Workshop Resource Requirements")

# ---- Data ----
data = [
    (80, "Metal Parts", "Gunsmith 1, Refiner 1"),
    (75, "Plastic Parts", "Gear Bench 1, Utility Station 1"),
    (30, "Rubber Parts", "Gunsmith 1"),
    (80, "Fabric", "Gear Bench 1, Medical Lab 1"),
    (50, "Chemicals", "Explosives Station 1"),
    (18, "Arc Alloy", "Explosives Station 1, Medical Lab 1, Utility Station 1"),
    (5, "Arc Powercells", "Refiner 1"),
    (3, "Rusted Tools", "Gunsmith 2"),
    (5, "Mechanical Components", "Gunsmith 2"),
    (8, "Wasp Drivers", "Gunsmith 2"),
    (3, "Rusted Gears", "Gunsmith 3"),
    (5, "Advanced Mechanical Components", "Gunsmith 3"),
    (4, "Sentinel Firing Cores", "Gunsmith 3"),
    (3, "Synthesized Fuel", "Explosives Station 2"),
    (5, "Crude Explosives", "Explosives Station 2"),
    (5, "Pop Triggers", "Explosives Station 2"),
    (3, "Laboratory Reagents", "Explosives Station 3"),
    (5, "Explosive Compounds", "Explosives Station 3"),
    (3, "Rocketeer Drivers", "Explosives Station 3"),
    (3, "Power Cables", "Gear Bench 2"),
    (10, "Electrical Components", "Gear Bench 2, Utility Station 2"),
    (5, "Hornet Drivers", "Gear Bench 2"),
    (3, "Industrial Batteries", "Gear Bench 3"),
    (10, "Advanced Electrical Components", "Gear Bench 3, Utility Station 3"),
    (6, "Bastion Cells", "Gear Bench 3"),
    (2, "Cracked Bioscanners", "Medical Lab 2"),
    (5, "Durable Cloth", "Medical Lab 2"),
    (8, "Tick Pods", "Medical Lab 2"),
    (3, "Rusted Shut Medical Kits", "Medical Lab 3"),
    (8, "Antiseptic", "Medical Lab 3"),
    (5, "Surveyor Vaults", "Medical Lab 3"),
    (2, "Damaged Heat Sinks", "Utility Station 2"),
    (6, "Snitch Scanners", "Utility Station 2"),
    (3, "Fried Motherboards", "Utility Station 3"),
    (4, "Leaper Pulse Units", "Utility Station 3"),
    (3, "Toasters", "Refiner 2"),
    (5, "Arc Motion Cores", "Refiner 2"),
    (8, "Fireball Burners", "Refiner 2"),
    (3, "Motors", "Refiner 3"),
    (10, "Arc Circutry", "Refiner 3"),
    (6, "Bombardier Cells", "Refiner 3"),
    (1, "Dog Collar", "Scrappy 2"),
    (3, "Lemons", "Scrappy 3"),
    (15, "Apricots", "Scrappy 3, Scrappy 5"),
    (6, "Prickly Pears", "Scrappy 4"),
    (6, "Olives", "Scrappy 4"),
    (1, "Cat Bed", "Scrappy 4"),
    (12, "Mushrooms", "Scrappy 5"),
    (3, "Very Comfortable Pillows", "Scrappy 5"),
]

df = pd.DataFrame(data, columns=["Amount", "Material", "Upgrades"])

# Expand upgrades
df_expanded = df.assign(Upgrade=df["Upgrades"].str.split(", ")).explode("Upgrade")

# Create workstation category column
df_expanded["Workstation"] = df_expanded["Upgrade"].str.extract(r"(^[A-Za-z ]+)")

# ---- Sidebar Filters ----
st.sidebar.header("Filters")

# Workstation Filter
workstations = sorted(df_expanded["Workstation"].unique())
selected_workstations = st.sidebar.multiselect(
    "Filter by Workstation",
    workstations,
)

# Upgrade Filter
upgrades = sorted(df_expanded["Upgrade"].unique())
selected_upgrades = st.sidebar.multiselect(
    "Filter by Upgrade Level",
    upgrades,
)

# Material Search
search_material = st.sidebar.text_input("Search Material")

# ---- Filtering Logic ----
filtered_df = df_expanded.copy()

if selected_workstations:
    filtered_df = filtered_df[filtered_df["Workstation"].isin(selected_workstations)]

if selected_upgrades:
    filtered_df = filtered_df[filtered_df["Upgrade"].isin(selected_upgrades)]

if search_material:
    filtered_df = filtered_df[
        filtered_df["Material"].str.contains(search_material, case=False)
    ]

# ---- Create clickable links for materials ----
def make_clickable(material):
    base_url = "https://www.google.com/search?q=ARC+Raiders+"
    return f'<a href="{base_url}{material.replace(" ", "+")}" target="_blank">{material}</a>'

filtered_df["Material"] = filtered_df["Material"].apply(make_clickable)

# ---- Display ----
st.subheader("📋 Filtered Requirements")

st.markdown(
    filtered_df[["Upgrade", "Material", "Amount"]]
    .to_html(escape=False, index=False),
    unsafe_allow_html=True,
)

st.markdown("---")
st.caption("Built with Streamlit for ARC Raiders Workshop Planning")
