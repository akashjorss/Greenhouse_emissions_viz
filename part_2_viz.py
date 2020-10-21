"""Part 2"""
import pandas as pd
import streamlit as st
import altair as alt
data = pd.read_csv("green_house.csv")


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


#data = data[data.Country.isin(countries[:10])]
data = data[data.VAR == 'TOTAL']
data = data[data.Country != 'OECD - Total']
data = data[data.Country != 'OECD - Europe']
data = data[data.Country != 'European Union (28 countries)']
#st.write(data.head(10))

#Make a bar chart with log scale, showing different emissions
bar_chart = alt.Chart(data[data.Pollutant=='Greenhouse gases']).mark_bar(
	opacity=0.5).transform_filter( #[data.Country.isin(countries)]
		'datum.Country != null'
	).encode(
	alt.X('Country:N',
			title='Country'),
	alt.Y('Value:Q',
			scale=alt.Scale(type='log', domain=[1, 10000000]),
			axis=alt.Axis(tickCount=5, grid=False),
			title='Emission Value (in Tonnes of CO2 equivalent)'),
	alt.Tooltip('Country:N')
).properties(width=600, height=500,
		title="Greenhouse gases emissions by Top 10 countries"
).add_selection(select_year).transform_filter(select_year
).transform_window(
    rank='rank(Value)',
    sort=[alt.SortField('Value', order='descending')]
).transform_filter(
    (alt.datum.rank < 11)
)

st.altair_chart(bar_chart)

"""
We use bar-chart for plotting emission by top countries. 
Transformat window and and transform filter was chosen to 
to select these 10 countries automatically and they changed over time. 
The slider filters the year. From the first sight, it looks like
there is not much difference in the emissions of top 10 countries, 
and that it doesn't change over time.

This chart is misleading because

1. It is ambiguous. y axis is total emission of green house gases. 
It is the sum of green house gases emitted by each country
in that year. Different gases are harmful in different quantities.
There is no normalization between gases. 

2. The y axis is on the log scale. So it appears that different
countries emit almost the same amount of greenhouse gases. Thus
ignoring the fact that United States emit 10 times more than
United Kingdom. To suppress the difference in emissions:

	i. The y axis scale starts from 1 and the 

	ii. bars are not sorted 

	iii. Countries are not color coded

3. Also, the emissions are not normalized by per capita, which
completely ignores the size of the country. 

4. The title subtley suggests that being top 10 is positive
"""

# Compare the gas emissions

area_chart = alt.Chart(data).mark_area(opacity=0.5,
	interpolate='monotone').encode(
    alt.X("Year:O"),
    alt.Y("sum(Value):Q", stack=None,
    	title='Yearly emission (in Tonnes of CO2 equivalent)'),
    alt.Color("Pollutant:N"),
    alt.Tooltip("Pollutant:N")
).transform_filter(
	alt.datum.Pollutant != 'Greenhouse gases'
).properties(height = 400, width=800,
	title="Major pollutants causing greenhouse effect")

st.altair_chart(area_chart)


"""
We use transparent area charts to visualise the emission
of different gases over time. Since altair doesn't have support
for pie chart yet, area charts are the next best thing to compare
quantities in a time series setting. At first sight, due to large quantity of CO2
being released, the viewer thinks that CO2 is the most significant
pollutant, and compared to it rest of the pollutants are insignificant. 
The above chart is misleading:

1. The title introduces the bias. It would indicate that more major the pollutant is, 
the more area it will have on chart

2. Plots the literal number of gas emissions, without taking
into account the effects of different gases in different
quantities. For example, Hydrofluorocarbons deplete ozone layer
and is effective in even small quantities, and CO2 can be tolerated
in much larger quantities relative to HFC. But this chart 
draws the attention of the viewer to CO2, more than the other gases
which are potentially much more harmful. 
"""
