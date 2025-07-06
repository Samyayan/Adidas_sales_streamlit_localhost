import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")
st.title(":bar_chart: Adidas Sales")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
#File upload
try:
    fl=st.sidebar.file_uploader(":file_folder: Upload file", type=['xlsx'])

    if fl is not None:
        df=pd.read_excel(fl)
        st.markdown("## :round_pushpin: Whole Data Statistics")
        st.write(df.describe())
    
#Creating side bar and filter
    st.sidebar.header("Choose your filters")
#Region
    region=st.sidebar.multiselect("Pick the region", df["Region"].unique())
    if not region:
        df2=df.copy()
    else: 
        df2=df[df["Region"].isin(region)]
#State
    state=st.sidebar.multiselect("Pick the state", df2["State"].unique())
    if not state:
        df3=df2.copy()
    else:
        df3=df2[df2["State"].isin(state)]
#City
    city=st.sidebar.multiselect("Pick city", df3["City"].unique())

#Creating filters
    if not region and not state and not city:
        filtered_df=df
    elif not state and not city:
        filtered_df=df[df["Region"].isin(region)] 
    elif not region and not city:
        filtered_df=df[df["State"].isin(state)]
    elif region and state:
        filtered_df=df3[df["Region"].isin(region) & df3["State"].isin(state)]
    elif state and city:
        filtered_df=df3[df["State"].isin(state) & df3["City"].isin(city)]
    elif region and city:
        filtered_df=df3[df["Region"].isin(region) & df3["City"].isin(city)]
    elif city:
        filtered_df=df3[df3["City"].isin(city)]
    else:
        filtered_df=df3[df3["Region"].isin(region)&df3["State"].isin(state)&df3["City"].isin(city)]

#Creating plots
    fig=px.bar(filtered_df, x="Retailer", y="TotalSales", color="Product", template="gridon", barmode="group",
            title="Visualising total sales vs. retailer vs. product")
    st.plotly_chart(fig, use_container_width=True)
    expander=st.expander("Total sales vs. retailer vs. product data")
    data=filtered_df
    expander.write(data)
    st.download_button("Get data", data=data.to_csv(), file_name="Total sales vs. retailer vs. product data.csv", mime="txt/csv")

    df["Month_Year"]=(df["InvoiceDate"]).dt.strftime("%b, %y") 
    result=filtered_df.groupby(by=df["Month_Year"])["TotalSales"].sum().reset_index()

#Creating plots column-wise
    col1, col2=st.columns((2)) 
    with col1:
        fig1=px.line(result, x="Month_Year", y="TotalSales", title="Total sales over time",
                    template="seaborn")
        st.plotly_chart(fig1, use_container_width=True)
        expander=st.expander("Monthly sales")
        data=result
        expander.write(data)
        st.download_button("Get data", data=data.to_csv(), file_name="Month wise sales.csv", mime="text/csv")

    with col2:
        fig2=px.treemap(filtered_df, path=["Region", "State", "City"], values="UnitsSold", title="Tree map showing units sold region and state wise", height=500)
        st.plotly_chart(fig2, use_container_width=True)

    fig3=px.bar(filtered_df, x='SalesMethod', y="TotalSales", color="Product", barmode="group")
    st.plotly_chart(fig3, use_container_width=True)

    fig4=px.choropleth(filtered_df, locations="State_Code",locationmode="USA-states", color="UnitsSold", color_continuous_scale="Reds", hover_name="State", hover_data="TotalSales")
    fig4.update_layout(width=1200, height=700)
    st.plotly_chart(fig4, use_container_width=True)

except: 
    st.markdown("## Upload file")