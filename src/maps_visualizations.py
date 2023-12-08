import pandas as pd
import plotly.express as px
import plotly
import json
df = pd.read_csv("../data/merged_dataset.csv", index_col=0)
df.head()
# sort by physicians_per_1000_people in descending order
df.sort_values(by="physicians_per_1000_people", ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)
df.head()
df.to_csv("../data/merged_sorted_dataset.csv")
min = df.head(1)["physicians_per_1000_people"].values[0]
min
max = df.tail(1)["physicians_per_1000_people"].values[0]
max
df["reverse_physicians_per_1000_people"] = 1 / df["physicians_per_1000_people"]
#df["reverse_physicians_per_1000_people"] = df["physicians_per_1000_people"].apply(lambda x: max - x + min)
df.head()
df.tail()
with open("../postleitzahlen.geojson") as response:
    zipcode_json = json.load(response)
# zipcode_json['features'][0]['properties']
choropleth_fig = px.choropleth_mapbox(
    df,
    color="population_density",
    geojson=zipcode_json,
    locations='zipcode',
    featureidkey='properties.postcode',
    center={"lat": 48.142137, "lon": 11.557905},
    mapbox_style='open-street-map',
    zoom=10.5,
    opacity=0.5,
     hover_data={
                "zipcode":':.0f',
                "population_density":':.0f',
                "population":':.0f',
     },
    labels={
        "zipcode":"Zipcode",
        "population":"Population",
        "population_density":"Population Density",
    },
    title='<b>Population map of Munich based on Zipcodes</b>',
    color_continuous_scale='Cividis'    
)
choropleth_fig.update_layout(
    margin={'r':20,'t':40,'l':20,'b':20},
    font_color='black',
    height=900,
    width=1300,
    autosize=True,
    hovermode='closest',
    hoverlabel={"bgcolor":"white",
                "font_color":"black", 
                "font_size":12,
                "font_family":"Sans"},
     title={
        "font_size":20,
        "xanchor":"center", "x":0.38,
        "yanchor":"bottom", "y":0.96
        }

)
choropleth_fig.show()

scatter_mapbox_fig = px.scatter_mapbox(
                    df,
                    lat='lat',
                    lon='lon',
                    color='reverse_physicians_per_1000_people',
                    size='reverse_physicians_per_1000_people',
                    size_max=30,
                    # hover_name='zipcode',
                    hover_data={
                                "zipcode":':.0f',    
                                "physicians_per_1000_people":':.2f',
                                "population_density":':.0f',
                                'lat':False, 'lon':False, 'reverse_physicians_per_1000_people':False},
                    zoom=10.5,
                    title="<b>'Requirement for physicians per 1000 people across Munich'</b>",
                    color_discrete_sequence=px.colors.qualitative.Plotly,
                    labels={
                            "zipcode":"Zip Code",
                            "physicians_per_1000_people": "Physicians Density",
                            "population_density":"Population Density",
                            "reverse_physicians_per_1000_people": "1 / physicians per 1000 people",
                    #         "physicians_count": "Physicians"
                            }
                       )

scatter_mapbox_fig.update_layout(
                margin={'r':20,'t':40,'l':20,'b':20},
                    title={"font_size":20,
                           "xanchor":"center", "x":0.38,
                           "yanchor":"bottom", "y":0.95},
                    title_font=dict(size=24, color='Black', family='Arial, sans-serif'),
                    height=900,
                    width=1300,
                    autosize=True,
                    hovermode='closest',
                    hoverlabel={"bgcolor":"white",
                              "font_color":"black", 
                              "font_size":12,
                             "font_family":"Sans"},
                    mapbox=dict(
                        style='open-street-map'
                    )
)

scatter_mapbox_fig.show()


scatter_data = scatter_mapbox_fig.data[0]

choropleth_fig.add_trace(scatter_data)
choropleth_fig.update_layout(
    title_text="Requirement for physicians per 1000 people across Munich laid over population map",
)
choropleth_fig.show()
df.plot.scatter(x="population_density", y="physicians_density");
df.loc[:10].plot.bar(x="zipcode", y="physicians_per_1000_people");
df.loc[:10].plot.bar(x="zipcode", y="population_density");
df.loc[:10].plot.bar(x="zipcode", y="physicians_density");