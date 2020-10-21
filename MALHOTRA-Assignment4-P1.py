# Part 1 of Assignmnent 4:
# Create Visualization
import pandas as pd
import streamlit as st
import altair as alt
from sklearn import preprocessing
import numpy as np
data = pd.read_csv("green_house.csv")

#top ten countries
countries = ['United States', 'Russia', 'Japan', 'Germany', 'Italy',
				'Canada', 'Australia', 'Turkey', 'United Kingdom', 'France']


# filter out Europe and total as our objective is to compare countries
data = data[data.Country != 'OECD - Total']
data = data[data.Country != 'OECD - Europe']
data = data[data.Country != 'European Union (28 countries)']
# st.write(data.head(10))

#A slider filter for year
select_year = alt.selection_single(
	name='select', fields=['Year'], init={'Year': 2018}, #here use min(Year)
	bind=alt.binding_range(min=1990, max=2018, step=1) #use here min and max
)

# A dropdown filter: filters for x axis and y axis
emission_type = data['Pollutant'].unique()
emission_dropdown = alt.binding_select(options=emission_type)
emission_select = alt.selection_single(
	fields=['Pollutant'], bind=emission_dropdown, name="Emission type", init={'Pollutant': 'Carbon dioxide'}
	)

# total emission area chart
area_chart = alt.Chart(data[data.VAR == 'TOTAL']).mark_area(
	strokeWidth=3,
	opacity=0.7,
	interpolate='monotone'
	).encode(
	alt.X('Year:O', title="Year"),
	alt.Y('Value:Q', title="Emission value (in Tonnes of CO2 equivalent)"),
	alt.Color('Country:N', legend=None),
	alt.Tooltip('Country:N'),
	#alt.Order('Value:Q', sort='descending') #encode value with saturation
	).properties(
		width=800, height=400,
		title="Greenhouse house gas emission over the years"
	).add_selection(
	    emission_select
	).transform_filter(
	    emission_select
)

st.altair_chart(area_chart)
"""
The above stacked area chart is meant to show the overall trend of the 
greenhouse gas emission over the years. Area encoding was chosen because
it is an effective channel to visualize and compare the quantitive fields. The 
area chart is combination of line chart and area, and thus it is also useful 
for seeing trends over time.  
Filter transform (as a drop-down menu) is used to choose the desired 
greenhouse gas, whose variations we want to visualize over time. 
Countries can be identified by the user using a tooltip.
Legend for country is not included, as there are ~30 countries
in the dataset, and that would exceed the reasonable number of colours that
should be used in a visualization as a sole identifier. Also, big legends
are not aesthetic. 

This Visualization not only shows the quantity of a particular (user selected)
greenhouse gas emitted, but also it is effective in inter-country comparisons
and to see the over-all trend. For example, we see that for most gases 
the quantity of emission is has decreased over time, except for HFCs.
We also notice that there are some peaks, for example in 2007 due
to emissions by China. This makes sense, as it is right before the 2008 Financial 
Crises. """

# per capita emission per country
bar_chart = alt.Chart(data[data.Pollutant == 'Greenhouse gases'][data.VAR == 'GHG_CAP']).mark_bar(
	opacity=0.5).transform_filter( 
		'datum.Country != null'
	).encode(
	alt.X('Country:N',
			title='Country',
			sort=alt.EncodingSortField(
			op='max', field='Value', order='descending')),
	alt.Y('Value:Q',
			axis=alt.Axis(tickCount=5, grid=False),
			title='Emission value (in kilograms per capita)'),

	#alt.Color('Country:N'),
	alt.Tooltip('Country:N')
).properties(width=600, height=500,
		title="Total Greenhouse gases emissions per capita"
).add_selection(select_year).transform_filter(select_year)
st.altair_chart(bar_chart)

"""
The next bar chart uses length encoding to encapsulate Total Emission
value per capita, as length encoding is often the most effective
channel to get comprehend quantitive fields. It gives us a good idea of quantity of greenhouse gases emitted by
different countries. Due to unavailabilty of data of 
specific gases, we can only visualise the total greenhouse emission in this chart.
Per-capita chart was choosen over total emission by a country as the latter
can be misleading, as it doesn't encapsulate the size of the country. For example,
USA is the leading overall pollutant, however, Australia is the leading pollutant per capita. 
 Transform filter for year was applied. 
With the help of the slider, we can see the variation in emission of total greenhouse gas emission
over time. Since the values are sorted, we can also see, how rankings change 
over time. """

# heatmap
data = data[data.Country.isin(countries)]

heatmap = alt.Chart(data[data.VAR == 'TOTAL']).mark_rect().encode(
	x=alt.X('Country:N', title="Countries"),
	y=alt.Y('Pollutant:N', title="Greenhouse gases"),
	color=alt.Color('Value:Q',
		scale=alt.Scale(type='log', scheme='plasma', nice=True)
	),
	tooltip='Value:Q',
	).add_selection(select_year).transform_filter(select_year
	).properties(width=600, height=400,
		title="Greenhouse gases emitted by top 10 countries emitting most pollutants"
	).transform_filter(alt.datum.Pollutant != 'Greenhouse gases')

st.altair_chart(heatmap)

"""Next we see specifically, the total emission of each
pollutant by each country using a heatmap. It uses position
encoding to identify a country and pollutant and color to identify 
quantity. To monitor the change over time, it is a very effective 
tool. Thus, again, using filter transformation we use slider
to see change in the heatmap over the years. We use log scale
to clearly see the difference in different tones of colors, which also
"normalises" the quantities of different gases. 
Over all, we see that the heat map becomes less yellow from 1990 to 2018. 
But also, we see that some countries like Russia and Turkey have started to emit more
Nitrogen trifluoride and HFC respectively. """









