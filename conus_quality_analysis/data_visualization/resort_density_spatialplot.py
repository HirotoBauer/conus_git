import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load data
data = pd.read_csv(
    "C:/Users/noodl/Desktop/conus_git/conus_quality_analysis/resort_analysis/resort_density_monthly.csv"
)

data["region"] = data["north_south"] + "_" + data["east_west"]

date_cols = [col for col in data.columns if "-" in col and col.count("-") == 1]

date_map = pd.DataFrame(
    {"col": date_cols, "dt": pd.to_datetime(date_cols, format="%Y-%m")}
)

map_2015 = date_map[date_map["dt"].dt.year == 2015]

diffs = {}
for _, row in map_2015.iterrows():
    month = row["dt"].month
    col2015 = row["col"]

    # find the matching 1985 column name
    match = date_map[
        (date_map["dt"].dt.year == 1985) & (date_map["dt"].dt.month == month)
    ]["col"]

    col1985 = match.iloc[0]
    # subtract the two Series
    diffs[f"diff_{month}"] = data[col2015] - data[col1985]

diffs_df = pd.DataFrame(diffs)
data = pd.concat([data, diffs_df], axis=1)


# Plotting
# spatial per month
m_dict = {"12": "December", "1": "January", "2": "February", "3": "March"}
diff_cols = [col for col in data.columns if "diff" in col]
transform = ccrs.PlateCarree()
plot_size = (12, 4)
plot_bounds = [-127, -65, 27, 50]  # fit to the continental us

for m in diff_cols:
    fig = plt.figure(figsize=plot_size)
    ax = plt.axes(projection=transform)

    ax.add_feature(cfeature.STATES, edgecolor="darkgrey", linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, edgecolor="black")
    ax.add_feature(cfeature.BORDERS, edgecolor="black")
    ax.set_facecolor("lightgrey")

    location_plot = ax.scatter(
        data["lon"],
        data["lat"],
        transform=transform,
        s=25,
        edgecolor="none",
        c=data[m],
        cmap="seismic",
    )

    cbar = plt.colorbar(location_plot, orientation="vertical", pad=0.01)
    cbar.set_label("Bulk Density Difference (Kg/m^3)")

    ax.set_extent(plot_bounds, crs=transform)
    month_name = m.split("_")[1]
    plt.title(f"Bulk Density Difference 2015 - 1985 for {m_dict[month_name]}")

    plt.show()


# calculate mean density difference per region

regional_means = (
    data.groupby("region")[diff_cols]
    .mean()
    .rename(columns=lambda c: m_dict[c.split("_")[-1]])
)

# bar plot for regional diff per month
small = 18
med = 22
large = 24
for month in regional_means.columns:
    fig, ax = plt.subplots(figsize=(10, 5))
    regional_means[month].plot(kind="bar", ax=ax, color="royalblue")
    ax.set_title(f"Mean Density Difference in {month} (2015 - 1985)", fontsize=large)
    ax.set_ylabel("Δ Density", fontsize=small)
    # ax.set_xlabel("Region", fontsize=small)
    ax.set_xlabel(None)
    ax.tick_params(axis="x", rotation=-45, labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylim(bottom=-150, top=110)
    fig.tight_layout()
    ax.grid()
    plt.show()
