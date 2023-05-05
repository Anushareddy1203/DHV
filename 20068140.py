# -*- coding: utf-8 -*-
"""
Created on Fri May  5 22:25:59 2023

@author: anush
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Load data
military_df = pd.read_csv("militaryexpenditure.csv", skiprows=4)
gdp_df = pd.read_csv("gdp_percapita.csv", skiprows=4)
mortality_df = pd.read_csv("mortality_under5.csv", skiprows=4)
poverty_df = pd.read_csv("API_SI.POV.DDAY_DS2_en_csv_v2_5358982.csv", skiprows=4)

# Select the top four countries by military expenditure
top_countries = ['United States', 'India', 'China', 'Russian Federation']
df_top = military_df[military_df['Country Name'].isin(top_countries)][['Country Name', '2019']]
world_total = military_df['2019'].sum()
top_total = df_top['2019'].sum()
percentages = df_top['2019'] / top_total * 100

# Extract the GDP per capita data from 2000 to 2020 with 5 years interval
countries = ["India", "China", "United States", "Russian Federation", "Brazil", "United Kingdom"]
years = [str(year) for year in range(2000, 2021, 5)]
gdp_data = gdp_df[gdp_df["Country Name"].isin(countries)][["Country Name"] + years]
gdp_data = gdp_data.set_index("Country Name")

# Select the desired countries and years for mortality rate under 5
years = range(2000, 2021, 5)
subset = mortality_df.loc[mortality_df["Country Name"].isin(countries), ["Country Name"] + [str(year) for year in years]]
subset.set_index("Country Name", inplace=True)
subset = subset.transpose()

# Prepare poverty headcount ratio data for histogram
poverty_df = poverty_df.set_index("Country Name")
dropped_df = poverty_df.loc[:, "2000":"2021"]
filtered_df = dropped_df.dropna(axis=0, how="all")
mean_pov_ratio = filtered_df.mean(skipna=True, numeric_only=True)

# Set up grid layout
fig = plt.figure(figsize=(16, 8), dpi=300)
fig.suptitle('Dashboard Infographics visualisation', fontsize=15, fontweight='bold')

gs = gridspec.GridSpec(nrows=2, ncols=3, figure=fig, wspace=0.3, hspace=0.4)

# Pie chart for military expenditure
ax1 = fig.add_subplot(gs[0, 0])
ax1.pie(percentages, labels=df_top['Country Name'], autopct='%1.1f%%')
ax1.set_title('Military Expenditure of Top Four Countries in 2019')

# Bar chart for GDP per capita
ax2 = fig.add_subplot(gs[0, 1])
gdp_data.plot(kind="bar", rot=0, ax=ax2)
ax2.set_title("GDP per capita (current US$) from 2000 to 2020")
ax2.set_xlabel("Country")
ax2.set_ylabel("GDP per capita (current US$)")
ax2.legend(title="Year")

# Line chart for mortality rate under 5
ax3 = fig.add_subplot(gs[0, 2])
subset.plot(kind="line", ax=ax3)
ax3.set_title("Mortality rate under 5 from 2000 to 2020")
ax3.set_xlabel("Year")
ax3.set_ylabel("Mortality rate under 5 (per 1,000 live births)")
ax3.legend(title="Country",prop={"size":8})

# Histogram for mean poverty headcount ratio
ax4 = fig.add_subplot(gs[1, 0])
ax4.hist(mean_pov_ratio, bins=20, color='blue')
ax4.set_xlabel('Mean Poverty Headcount Ratio')
ax4.set_ylabel('Frequency')
ax4.set_title('Histogram of Mean Poverty Headcount Ratio')

fig.text(0.4, 0.2,' The understanding of how military expenditure, GDP per capita, mortality rate under 5,\n and mean poverty ratio are interlinked and how this affects countries around the world.\n It is clear from the data that those countries with the highest military expenditure are also\n the countries with the highest GDP per capita, the lowest mortality rate under 5, and the\n lowest mean poverty ratio. This indicates that countries with higher military expenditure\n are also those countries with the most resources to invest in their people, providing them \n with better healthcare, education, and economic opportunities.',
         fontsize=12, ha='left', va='bottom')

# Add student name and student ID
plt.figtext(0.5, 0.01, 'Student Name: Anusha Kallahalli Byrareddy\nstudent ID: 20068140', 
            fontsize=12, ha='center')
fig.savefig("20068140.png",dpi=300)
plt.show()