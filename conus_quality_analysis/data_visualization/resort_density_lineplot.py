import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Load data
# bulk snow density
# data = pd.read_csv(
#     "C:/Users/noodl/Desktop/conus_git/conus_quality_analysis/resort_analysis/resort_density_monthly.csv"
# )

# new snow density
data = pd.read_csv(
    "C:/Users/noodl/Desktop/conus_git/conus_quality_analysis/resort_analysis/resort_snow_ratio_monthly.csv"
)

ylim = (0, 17)  # change based on the data being plotted

color_dict = {
    "lightred": "lightcoral",
    "darkyellow": "sienna",
    "lightyellow": "orange",
    "lightblue": "darkturquoise",
}

data["region"] = data["north_south"] + "_" + data["east_west"]
date_cols = [col for col in data.columns if "-" in col and col.count("-") == 1]
date_cols_sorted = sorted(date_cols, key=lambda x: pd.to_datetime(x))

# Compute mean per region per month
region_monthly_means = {}
for region in data["region"].unique():
    rdata = data[data["region"] == region]
    means = rdata[date_cols_sorted].mean(axis=0)
    region_monthly_means[region] = means

means_df = pd.DataFrame(region_monthly_means).T
means_df = means_df.T
means_df.index = pd.to_datetime(means_df.index)
means_df["month"] = means_df.index.month
means_df["water_year"] = means_df.index.year

# Define the season months and their labels
season_months = [12, 1, 2, 3]
month_labels = ["Dec", "Jan", "Feb", "Mar"]
x_positions = list(range(len(season_months)))  # [0,1,2,3]

# Define color scheme
region_colors = {"west": "blue", "rockies": "green", "midwest": "red", "east": "orange"}

# Define line styles
line_styles = {
    1985: "-",  # solid
    2015: "--",  # dotted
}


# Helper function to adjust brightness
def adjust_brightness(color, factor):
    """Lightens or darkens a color by a factor (0.0 to 1.0)."""
    rgb = mcolors.to_rgb(color)
    h, s, v = mcolors.rgb_to_hsv(rgb)
    v = max(0, min(1, v * factor))  # Clamp between 0 and 1
    return mcolors.hsv_to_rgb((h, s, v))


# Create figure
xsmall = 14
small = 18
med = 22
large = 24
fig, ax = plt.subplots(figsize=(12, 7))

for region in data["region"].unique():
    # Determine base color based on region type
    region_type = region.split("_")[-1]  # west, rockies, midwest, east
    base_color = region_colors.get(region_type, "gray")

    # Adjust brightness based on north/south
    if region.startswith("north"):
        color = adjust_brightness(base_color, 0.6)  # Darker
        marker = "o"
    else:
        color = adjust_brightness(base_color, 3)  # Lighter
        marker = "o"

    df_region = means_df[[region, "month", "water_year"]].copy()
    df_region = df_region[df_region["month"].isin(season_months)]

    for wy, group in df_region.groupby("water_year"):
        group = group.set_index("month").reindex(season_months)
        if group[region].isnull().all():
            continue

        # Plot with specified style
        ax.plot(
            x_positions,
            group[region].values,
            color=color,
            linestyle=line_styles[wy],
            marker=marker,  # Add dots
            markersize=5,
            label=f"{region} – WY{wy}",
        )

# Customize plot
ax.set_xticks(x_positions)
ax.set_xticklabels(month_labels, fontsize=xsmall)
ax.tick_params(axis="y", labelsize=xsmall)
ax.set_xlabel("Month", fontsize=small)
ax.set_ylabel("Mean Snow Density [kg/m^3]", fontsize=small)
ax.set_title("Monthly Mean Bulk Snow Density by Region and Water Year", fontsize=med)
ax.set_ylim(ylim)
ax.grid(True, alpha=0.4)

# Improve legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles,
    labels,
    loc="center left",
    bbox_to_anchor=(1, 0.485),
    fontsize=small,
    framealpha=1,
)

plt.tight_layout()
plt.show()

# plotting each region seperatly
for r in data["east_west"].unique():
    d = data.loc[data["east_west"] == r]
    fig, ax = plt.subplots(figsize=(12, 7))
    for region in d["region"].unique():
        # Determine base color based on region type
        region_type = region.split("_")[-1]  # west, rockies, midwest, east
        base_color = region_colors.get(region_type, "gray")

        # Adjust brightness based on north/south
        if region.startswith("north"):
            color = adjust_brightness(base_color, 0.6)  # Darker
            # color = "sienna"
            marker = "o"
        else:
            # color = adjust_brightness(base_color, 20)  # Lighter
            color = color_dict["lightblue"]
            marker = "o"

        df_region = means_df[[region, "month", "water_year"]].copy()
        df_region = df_region[df_region["month"].isin(season_months)]

        for wy, group in df_region.groupby("water_year"):
            group = group.set_index("month").reindex(season_months)
            if group[region].isnull().all():
                continue

            # Plot with specified style
            ax.plot(
                x_positions,
                group[region].values,
                color=color,
                linestyle=line_styles[wy],
                marker=marker,  # Add dots
                markersize=5,
                label=f"{region} – WY{wy}",
            )

    # Customize plot
    ax.set_xticks(x_positions)
    ax.set_xticklabels(month_labels, fontsize=xsmall)
    ax.tick_params(axis="y", labelsize=xsmall)
    ax.set_xlabel("Month", fontsize=small)
    ax.set_ylabel("Mean Snow Density [kg/m^3]", fontsize=small)
    ax.set_title(f"Monthly Mean Snow Density for {r} Region", fontsize=med)
    ax.set_ylim(ylim)
    ax.grid(True, alpha=0.4)

    # Improve legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=small,
        framealpha=1,
    )

    plt.tight_layout()
    plt.show()
