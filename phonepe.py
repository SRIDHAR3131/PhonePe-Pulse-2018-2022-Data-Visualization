
#-------------------------------------------IMPORTING MODULE------------------------------------------------------------
import os                             #for accessing my directores
import json                           #for read JSON file format
import time                           #for loading spinner
import pymysql                        #for connecting and read MySQL database
from sqlalchemy import create_engine
from PIL import Image
import pandas as pd
import plotly.express as px           #plotly express-data visualization
import plotly.graph_objects as go     #plotly graph object-data visualization
import streamlit as st                #GUI
from streamlit_option_menu import option_menu   #option menu
import requests


#-------------------------------------------NUMBER CONVERSION IN LAKHS AND CRORES---------------------------------------
#-------optional case--------

def convert_to_crore2(number):
    crore = number / 10000000
    return round(crore,2)

def convert_to_lakh2(number):
    lakh = number / 100000
    return round(lakh,2)

def convert_to_thousand(number):
    the = number / 1000
    return round(the,2)

def number_convert(number): #number conversion str
    formatted_number = "{:,}".format(number)
    return formatted_number

def format_number(num):  #user str
    if num >= 10000000:
        return f"{num/10000000:.2f} Cr"
    elif num >= 100000:
        return f"{num/100000:.2f} L"
    else:
        return str(num)
def format_number1(num): #transaction str
    if num >= 10000000:
        return f"₹{num/10000000:.2f} Cr"
    elif num >= 100000:
        return f"₹{num/100000:.2f} L"
    else:
        return str(num)

def format_number2(num): #number int
    if num >= 10000000:
        return round(num,2)
    elif num >= 100000:
        return round(num,2)
    else:
        return round(num,2)

#percentage conversion varies
def convert_to_per(number):
    per = (number*100)/10
    return f'{per:.2f} %'

#--------------------------------PYTHON TO MYSQL DATABASE CONNECT AND UPLOAD DATAFRAME ---------------------------------

engine =create_engine("mysql+pymysql://root:Sridhar15@localhost/phonepe_pulse_data")
conn=engine.connect()

#---------------------------------MYSQL TO PYTHON CONNECT AND READ THE QUERY--------------------------------------------
map_tran = pd.read_sql_table('map_transaction', conn) #1
map_user= pd.read_sql_table('map_users', conn) #2

agg_tran = pd.read_sql_table('agg_transaction', conn) #3
agg_user = pd.read_sql_table('agg_user', conn) #4
agg_user_device = pd.read_sql_table('agg_user_device', conn) #5

top_tran= pd.read_sql_table('top_transaction', conn) #6
top_user= pd.read_sql_table('top_user', conn) #7
top_pin = pd.read_sql_table('top_pincode', conn)#8

geo_code= pd.read_sql_table('state_code_lat_lon', conn) #9
geo_dist= pd.read_sql_table('state_dist_lat_lon', conn) #10

#------------------------------------------PAGE CONFIGURATION AND LAYOUT------------------------------------------------

st.set_page_config(
     page_title="PhonePe data visualization",
     page_icon="chart_with_upwards_trend",
     layout="wide",
     initial_sidebar_state="expanded",)
# Hide the streamlit app content
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

#==============================================Loading spinner==========================================================
with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(1)
# sidebar with options for home and visualization
with st.sidebar:
    main = option_menu(None, ["Home", 'Visualization'],icons=['house', 'pin-map'], menu_icon="cast")
#=====================================home page============================================================
if main=='Home':

    image = Image.open("phone.png")
    st.sidebar.image(image, width=310)

    main_img,img1=st.columns([2,1])
    with main_img:
        main_i = Image.open("PhonePe_Logo_full.png")
        st.image(main_i,width=400)
    with img1:
        main_i2 = Image.open("phonepe process.jpg")
        st.image(main_i2,width=250)
    st.markdown("#### Welcome to the **:violet[PhonePe Pulse]** Data Visualization! ")
    st.markdown("This visualization allows you to explore and analyze PhonePe's pulse data from 2018 to 2022. With interactive charts and various metrics to choose, you can gain insights into PhonePe's business performance and growth over time.")
    st.markdown("To get started, select the desired ****date range**** and ****metrics**** to visualize using the sidebar on the left. Then, explore the data using the interactive charts provided by Plotly Express.")
    st.markdown("This tool is built using  *:red[Python]* - scripting,  *:blue[Streamlit]* - creating GUI, *:green[Plotly Express]* - interactive data visualization tool like bar chart,line chart,sunburst chart,scatter geo, choropleth map etc.. and  *:orange[MySQL Database]* - store and read the data by raising query."
                " It is available as an open-source project on GitHub.")
    st.markdown("Click on the ****:red[Visualization]**** option in the sidebar to start exploring the PhonePe Pulse data.")
    st.write("This project inspired from [PhonePe Pulse](https://www.phonepe.com/pulse/explore/transaction/2022/4/) ", " Data source:","[Git Hub](https://github.com/PhonePe/pulse)")
    st.info("Amount and Count values(₹) are converted into Crores and Lakhs respectively for better visualization",icon="ℹ️")
if main== "Visualization":
 # navigation menu
    with st.sidebar:
        analyser = option_menu(
            menu_title=None,
            options=["Transaction","User"],    # "REGISTER USER","APP OPENED USER"
            icons=["bank", "person"],  # https://icons.getbootstrap.com/
        )


    #sidebar with drop down menu for accssing the features
    year_c,state_c=st.sidebar.columns([1.5,2])
    with year_c:
        Year = st.selectbox('Please select Year',('2018', '2019', '2020', '2021', '2022'),key='side1')
    with state_c:
        Quarter = st.selectbox('Please select Quarter',('Q1 (Jan - Mar)','Q2 (Apr - Jun)','Q3 (Jul - Sep)','Q4 (Oct - Dec)'),key='side2')
    with st.sidebar:
        State = st.selectbox('Please select State',
                             ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
                              'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                              'Gujarat','Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala',
                              'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur','Meghalaya', 'Mizoram',
                              'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim','Tamil Nadu', 'Telangana',
                              'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'),
                             key='side3')

    #===============================================Transaction analysis========================================================

    if analyser == "Transaction":
        # navigation menu
        selected = option_menu(
            menu_title=None,
            options=["TRANSACTION AMOUNT","TOTAL TRANSACTION"],    # "REGISTER USER","APP OPENED USER"
            icons=[None, "bar-chart-fill"],  # https://icons.getbootstrap.com/"currency-rupee", "fill-person-fill"
            orientation="horizontal",
        )
        #sidebar overall transaction and amount

        tran, count = st.sidebar.columns(2)
        with tran:
            total_amt = agg_tran.loc[(agg_tran['Year'] == Year) & (agg_tran['Quarter'] == Quarter)]
            total = total_amt.groupby(['Year'], as_index=False).sum(numeric_only=True)
            total['Amount'] = total['Transaction_amount'].apply(format_number1)
            st.markdown('#### Payment value')
            ss = st.write(total[['Amount']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        with count:
            total_amt = agg_tran.loc[(agg_tran['Year'] == Year) & (agg_tran['Quarter'] == Quarter)]
            total = total_amt.groupby(['Year'], as_index=False).sum(numeric_only=True)
            total['Transaction'] = total['Total_transaction'].apply(number_convert)
            st.markdown('#### Total transaction ')
            ss1 = st.write(total[['Transaction']].style.hide(axis="index").to_html(), unsafe_allow_html=True)

    #===================================GEO MAP TRANSACTION AMOUNT ==============================================================
        if selected=='TRANSACTION AMOUNT':
            map_t = map_tran.loc[(map_tran['Year'] == Year) & (map_tran['Quarter'] == Quarter)]
            st_scatter = map_t.groupby(['State'], as_index=False).sum(numeric_only=True)
            #using for loop append transaction amount into state and district with lon and lat table
            st_code0 = geo_code  # state with code
            # state trace
            amount = []
            for i in st_scatter['Transaction_amount']:
                amount.append(i)
            st_code0['Transaction_amount'] = amount

            # using scatter geo for state trace
            state = px.scatter_geo(st_code0,
                                     lon=st_code0['Longitude'],
                                     lat=st_code0['Latitude'],
                                     hover_name="state",
                                     hover_data=["Transaction_amount"],
                                     )
            state.update_traces(marker=dict(color="white", size=4))
            state.update_geos(fitbounds="locations", visible=False)
            # using choropleth map for plod add trace of state and district
            map_data = px.choropleth(
                st_code0,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                hover_name="state",
                hover_data=["Transaction_amount"],
                color="Transaction_amount",
                color_continuous_scale='viridis'
            )
            map_data.update_geos(fitbounds="locations", visible=False, )
            # combining districts states and coropleth
            map_data.add_trace(state.data[0])

            mapamount,district= st.columns([4,1])
            with mapamount:
                st.write('#####', Year + ' - ', Quarter)
                st.plotly_chart(map_data, use_container_width=True)

            # district transaction amount
            dt_tran = top_tran.loc[(top_tran['Year'] == Year) & (top_tran['Quarter'] == Quarter) & (top_tran['State'] == State)]
            dist_tran = dt_tran.groupby(['Year', 'Quarter', 'State', 'District'], as_index=False).sum(numeric_only=True)
            dist_tran['Transaction_amount'] = dist_tran['Transaction_amount'].apply(convert_to_crore2)
            fig1 = px.sunburst(dist_tran, path=['State', 'District'], values='Transaction_amount',title="DISTRICT TRANSACTION")
            with district:
                st.plotly_chart(fig1, use_container_width=True)

            # overall state transaction amount
            st_tran = top_tran.loc[(top_tran['Year'] == Year) & (top_tran['Quarter'] == Quarter)]
            stt_tran = st_tran.groupby(['Year', 'Quarter', 'State'], as_index=False).sum(numeric_only=True)
            stt_tran = stt_tran.sort_values('Transaction_amount', ascending=False, ignore_index=True, axis=0)
            stt_tran['Transaction_amount'] = stt_tran['Transaction_amount'].apply(convert_to_crore2)
            fig2 = px.bar(stt_tran, title='STATE TRANSACTION AMOUNT', x='State', y='Transaction_amount',color='Transaction_amount', color_continuous_scale='algae', height=600)

            state, top = st.columns([3.5, 1.5])
            with state:
                st.plotly_chart(fig2, use_container_width=True)

            # ========================================TOP TRANSACTION AND USER STATE AND DISTRICT====================================

            with top:
                state_tran = top_tran.loc[(top_tran['Year'] == Year) & (top_tran['Quarter'] == Quarter)]
                top_state = state_tran.groupby(['State'], as_index=False).sum(numeric_only=True)
                top_dist = state_tran.groupby(['District'], as_index=False).sum(numeric_only=True)
                top10_tran_amount = top_state.sort_values('Transaction_amount', ascending=False, ignore_index=True, axis=0)
                top10_dt_tran_amount = top_dist.sort_values('Transaction_amount', ascending=False, ignore_index=True,axis=0)
                top10_tran_amount['Transaction_amount'] = top10_tran_amount['Transaction_amount'].apply(format_number1)
                top10_dt_tran_amount['Transaction_amount'] = top10_dt_tran_amount['Transaction_amount'].apply(format_number1)

                top = st.radio('', ('STATE', 'DISTRICT'), horizontal=True)
                if top == 'STATE':
                    st.markdown(' **TOP 10 STATE**')
                    st.write(
                        top10_tran_amount[['State', 'Transaction_amount']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)
                else:
                    st.markdown(' **TOP 10 DISTRICT** ')
                    st.write(top10_dt_tran_amount[['District', 'Transaction_amount']][0:10].style.hide(axis="index").to_html(), unsafe_allow_html=True)

            mode,mode1= st.columns([3,1.5])
            # payment instrument
            with mode:
                payment = agg_tran.loc[(agg_tran['Year'] == Year) & (agg_tran['Quarter'] == Quarter) & (agg_tran['State'] == State)]
                pie_1 = payment.groupby(['Transaction_type'], as_index=False).sum(numeric_only=True)
                pie_1['Transaction_amount'] = pie_1['Transaction_amount'].apply(convert_to_crore2)
                fig = px.pie(pie_1,title='TYPE OF TRANSACTION IN STATE',values="Transaction_amount",names="Transaction_type",hole=0.6,
                             color='Transaction_type',color_discrete_sequence=['red','black','lime','green','yellow'])
                st.plotly_chart(fig, use_container_width=True)

            #pie chart transaction
            with mode1:
                state_data = agg_tran.loc[(agg_tran['Year'] == Year) & (agg_tran['Quarter'] == Quarter)]
                val = state_data.groupby(['Transaction_type'], as_index=False).sum(numeric_only=True)
                val_1=val.sort_values('Transaction_amount', ascending=False, ignore_index=True, axis=0)
                val_1['Transaction_amount'] = val_1['Transaction_amount'].apply(format_number1)
                st.write('') #new line
                st.write('') #new line
                st.markdown("###### **TRANSACTION PAYMENT VALUE**")
                st.write(val_1[['Transaction_type','Transaction_amount']].style.hide(axis="index").to_html(),unsafe_allow_html=True)



    # ===================================GEO MAP TRANSACTION COUNT ==============================================================

        else:
            map_c = map_tran.loc[(map_tran['Year'] == Year) & (map_tran['Quarter'] == Quarter)]
            st_scatter = map_c.groupby(['State'], as_index=False).sum(numeric_only=True)
            dt_scatter = map_c.groupby(['State', 'District'], as_index=False).sum(numeric_only=True)

            #using for loop append transaction count into state,district with lon and lat table
            st_code0 = geo_code
            # state trace
            count = []
            for i in st_scatter['Total_transaction']:
                count.append(i)
            st_code0['Total_transaction'] = count
            # state trace
            state_0= px.scatter_geo(st_code0,
                                     lon=st_code0['Longitude'],
                                     lat=st_code0['Latitude'],
                                     hover_name="state",
                                     hover_data=["Total_transaction"],
                                     )
            state_0.update_traces(marker=dict(color="white", size=4))
            state_0.update_geos(fitbounds="locations", visible=False)
            # using choropleth map for plod add trace of state and district
            map_data_0 = px.choropleth(
                st_code0,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                hover_name="state",
                hover_data=["Total_transaction"],
                color="Total_transaction",
                color_continuous_scale='plasma',

            )
            map_data_0.update_geos(fitbounds="locations", visible=False, )
            # combining districts states and coropleth
            map_data_0.add_trace(state_0.data[0])

            mapcount,district0 = st.columns([3,1])
            with mapcount:
                st.write('#####', Year + ' - ', Quarter)
                st.plotly_chart(map_data_0, use_container_width=True)

            # sunburst-district transaction amount
            with district0:
                dt_tran1 = top_tran.loc[(top_tran['Year'] == Year) & (top_tran['Quarter'] == Quarter) & (top_tran['State'] == State)]
                dist_tran1 = dt_tran1.groupby(['Year', 'Quarter', 'State', 'District'], as_index=False).sum(numeric_only=True)
                fig11 = px.sunburst(dist_tran1, path=['State', 'District'], values='Total_transaction',title="DISTRICT TRANSACTION ")
                st.plotly_chart(fig11, use_container_width=True)

            state,top=st.columns([3.5,1.5])
            with state:
                st_count = agg_tran.loc[(agg_tran['Year'] == Year) & (agg_tran['Quarter'] == Quarter)]
                stt_count = st_count.groupby(['Year', 'Quarter', 'State'], as_index=False).sum(numeric_only=True)
                stt_count = stt_count.sort_values('Total_transaction', ascending=True, ignore_index=True, axis=0)
                stt_count['Total_transaction'] = stt_count['Total_transaction'].apply(format_number2)

                fig2 = go.Figure(data=go.Scatter(x=stt_count['Total_transaction'], y=stt_count['State'], text='Total_transaction',
                                                mode='markers+lines', line=dict(color='red', width=.4)))
                fig2.update_layout(title='STATE TRANSACTION ', plot_bgcolor='mintcream')
                st.plotly_chart(fig2, use_container_width=True)
            #top transaction count state and district
            with top:
                state_tran = top_tran.loc[(top_tran['Year'] == Year) & (top_tran['Quarter'] == Quarter)]
                top_state = state_tran.groupby(['State'], as_index=False).sum(numeric_only=True)
                top_dist = state_tran.groupby(['District'], as_index=False).sum(numeric_only=True)

                top10_tran_amount = top_state.sort_values('Total_transaction', ascending=False, ignore_index=True, axis=0)
                top10_dt_tran_amount = top_dist.sort_values('Total_transaction', ascending=False, ignore_index=True, axis=0)

                top10_tran_amount['Total_transaction'] = top10_tran_amount['Total_transaction'].apply(format_number)
                top10_dt_tran_amount['Total_transaction'] = top10_dt_tran_amount['Total_transaction'].apply(format_number)

                top = st.radio('', ('STATE', 'DISTRICT'), horizontal=True, key='radio')
                if top == 'STATE':
                    st.markdown(' **TOP 10 STATE**')
                    st.write(top10_tran_amount[['State', 'Total_transaction']][0:10].style.hide(axis="index").to_html(), unsafe_allow_html=True)
                else:
                    st.markdown(' **TOP 10 DISTRICT** ')
                    st.write(top10_dt_tran_amount[['District', 'Total_transaction']][0:10].style.hide(axis="index").to_html(), unsafe_allow_html=True)

            # hbar chart-payment instrument
            mode, mode1 = st.columns([3, 1.5])
            # payment instrument
            with mode:
                payment = agg_tran.loc[
                    (agg_tran['Year'] == Year) & (agg_tran['Quarter'] == Quarter) & (agg_tran['State'] == State)]
                pie_1 = payment.groupby(['Transaction_type'], as_index=False).sum(numeric_only=True)
                pie_1['Total_transaction'] = pie_1['Total_transaction'].apply(format_number2)
                fig = px.pie(pie_1, title='TYPE OF TRANSACTION IN STATE', values="Total_transaction", names="Transaction_type",
                             hole=0.6,color='Transaction_type',
                             color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)

            # pie chart transaction
            with mode1:
                state_data = agg_tran.loc[
                    (agg_tran['Year'] == Year) & (agg_tran['Quarter'] == Quarter)]
                val = state_data.groupby(['Transaction_type'], as_index=False).sum(numeric_only=True)
                val_1 = val.sort_values('Total_transaction', ascending=False, ignore_index=True, axis=0)
                val_1['Total_transaction'] = val_1['Total_transaction'].apply(number_convert)
                st.write('')  # new line
                st.write('')  # new line
                st.markdown("###### **TOTAL TRANSACTION VALUE**")
                st.write(val_1[['Transaction_type', 'Total_transaction']].style.hide(axis="index").to_html(),
                         unsafe_allow_html=True)

            line=st.columns(1)
            # line chart-transaction count
            with line[0]:
                line = agg_tran.loc[(agg_tran['State'] == State)]
                line = line.groupby(['Year','Quarter','State'], as_index=False).sum(numeric_only=True)
                line = line.sort_values('Total_transaction', ascending=True, ignore_index=True, axis=0)
                line['year']=line['Year']+line['Quarter']
                line['Total_transaction'] = line['Total_transaction'].apply(format_number)
                fig = go.Figure(data=go.Scatter(x=line['year'], y=line['Total_transaction'], text='Total_transaction',mode='markers+lines',line=dict(color='grey', width=2.5)))
                fig.update_layout(title='YEARLY STATE TRANSACTION ',plot_bgcolor='mintcream',)
                st.plotly_chart(fig, use_container_width=True)


    else:
        # NAVIGATION MENU
        selected = option_menu(
            menu_title=None,
            options=["REGISTER USER", "APP OPENED USER",'DEVICE USER'],
           # icons=["pencil-fill", "bar-chart-fill"],# https://icons.getbootstrap.com/
            icons=['person-check-fill', 'app-indicator','phone'],
            orientation="horizontal",
        )

    # ==============================overall register and app opened user================================================
        reg, app= st.sidebar.columns(2)
        with reg:
            total_reg = agg_user.loc[(agg_user['Year'] == Year) & (agg_user['Quarter'] == Quarter)]
            total_r = total_reg.groupby(['Year'], as_index=False).sum(numeric_only=True)
            total_r['Register'] = total_r['Register'].apply(number_convert)
            st.markdown('##### Registered User')
            st.write(total_r[['Register']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        with app:
            total_app = agg_user.loc[(agg_user['Year'] == Year) & (agg_user['Quarter'] == Quarter)]
            total_a = total_app.groupby(['Year'], as_index=False).sum(numeric_only=True)
            total_a['App_opened'] = total_a['App_opened'].apply(number_convert)
            st.markdown('##### App Opened User')
            st.write(total_a[['App_opened']].style.hide(axis="index").to_html(), unsafe_allow_html=True)

    #==================================REGISTER USER ANALYSIS==============================================================
        if selected=="REGISTER USER":

            map_reg=map_user.loc[(map_user['Year'] == Year) & (map_user['Quarter'] == Quarter)]
            st_scatter = map_reg.groupby(['State'], as_index=False).sum(numeric_only=True)
            dt_scatter = map_reg.groupby(['State', 'District'], as_index=False).sum(numeric_only=True)

            #using for loop append register user into state,district with lon and lat table
            st_code0 = geo_code# state with code
            dt0 = geo_dist
            # state trace
            reg = []

            for i in st_scatter['Register']:
                reg.append(i)
            st_code0['Register'] = reg
            # district trace
            reg = []

            for i in dt_scatter['Register']:
                reg.append(i)
            dt0['Register'] = reg

            # state trace
            state_1 = px.scatter_geo(st_code0,
                                     lon=st_code0['Longitude'],
                                     lat=st_code0['Latitude'],
                                     text=st_code0['code'],  # code of state
                                     hover_name="state",
                                     hover_data=["Register"],
                                     )
            state_1.update_traces(marker=dict(color="white", size=0.3))
            state_1.update_geos(fitbounds="locations", visible=False)
            # districts trace
            dist_1 = px.scatter_geo(dt0,
                                    lon=dt0['Longitude'],
                                    lat=dt0['Latitude'],
                                    size=dt0['Register'],
                                    hover_name="District",
                                    hover_data=["State", 'Register'],
                                    title='District',
                                    size_max=10)
            dist_1.update_traces(marker=dict(color='rebeccapurple',line_width=.05))
            # using choropleth map for plod add trace of state and district
            map_data_1 = px.choropleth(
                st_code0,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                color="Register",
                color_continuous_scale='hot',

            )
            map_data_1.update_geos(fitbounds="locations", visible=False, )
            # combining districts states and coropleth
            map_data_1.add_trace(state_1.data[0])
            map_data_1.add_trace(dist_1.data[0])

            mapreg,dist3 = st.columns([3,1])
            with mapreg:
                st.write('#####', Year + ' - ', Quarter)
                st.plotly_chart(map_data_1, use_container_width=True)

            #district user
            with dist3:
                dt_reg_user = map_user.loc[(map_user['Year'] == Year) & (map_user['Quarter'] == Quarter) & (map_user['State'] == State)]
                dt_reg = dt_reg_user.groupby(['Year', 'Quarter', 'District','State'], as_index=False).sum(numeric_only=True)
                dt_reg0= dt_reg.sort_values('Register', ascending=False, ignore_index=True, axis=0)
                fig1 = px.sunburst(dt_reg0, path=['State', 'District'], values='Register',title="DISTRICT REGISTER USER")
                st.plotly_chart(fig1, use_container_width=True)


            reg,top=st.columns([2,1])
            # bar chart-state user
            with reg:
                reg_user = agg_user.loc[(agg_user['Year'] == Year) & (agg_user['Quarter'] == Quarter)]
                reg = reg_user.groupby(['State'], as_index=False).sum( numeric_only=True)
                reg['Register']=reg['Register'].apply(convert_to_lakh2)
                reg0 = reg.sort_values('Register', ascending=True, ignore_index=True, axis=0)
                fig = px.bar(reg0, x='Register', y='State', color='Register', color_continuous_scale='dense',height=650,title='STATE REGISTER USER')
                st.plotly_chart(fig,use_container_width=True)
            #top state , disrict and pincodes
            with top:
                reg_user = top_user.loc[(top_user['Year'] == Year) & (top_user['Quarter'] == Quarter)]
                pin_user=top_pin.loc[(top_pin['Year'] == Year) & (top_pin['Quarter'] == Quarter)]

                top_reg_user = reg_user.groupby(['State'], as_index=False).sum(numeric_only=True)
                top_dt_reg_user = reg_user.groupby(['District'], as_index=False).sum(numeric_only=True)
                top_pin_user =pin_user.groupby(['Pincode'], as_index=False).sum(numeric_only=True)

                top10_reg_user = top_reg_user.sort_values('Register', ascending=False, ignore_index=True, axis=0)
                top10_dt_reg_user = top_dt_reg_user.sort_values('Register', ascending=False, ignore_index=True,axis=0)
                top10_pincode = top_pin_user.sort_values('Register', ascending=False, ignore_index=True, axis=0)

                top10_reg_user['Register'] = top10_reg_user['Register'].apply(format_number)
                top10_dt_reg_user['Register'] = top10_dt_reg_user['Register'].apply(format_number)
                top10_pincode['Register'] = top10_pincode['Register'].apply(format_number)
                top = st.radio('', ('STATE', 'DISTRICT','PINCODE'), horizontal=True, key='radio')
                st.write('######', Year + ' - ', Quarter)
                if top == 'STATE':
                    st.write('###### **TOP 10 STATE USER**')
                    st.write(top10_reg_user[['State', 'Register']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)
                elif top=='DISTRICT':
                    st.write('###### **TOP 10 DISTRICT USER**')
                    st.write(top10_dt_reg_user[['District', 'Register']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)
                else:
                    st.write('###### **TOP 10 PINCODE**')
                    st.write(top10_pincode[['Pincode', 'Register']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)

            #line chart-overall state app opened user
            line=st.columns(1)
            with line[0]:
                line = agg_user.loc[(agg_user['State'] == State)]
                line['year'] = line['Year'] + line['Quarter']
                line1 = line.groupby(['year','State'], as_index=False).sum(numeric_only=True)
                line0 = line1.sort_values('Register', ascending=True, ignore_index=True, axis=0)
                line0['Register']=line0['Register'].apply(format_number)

                fig = go.Figure(data=go.Scatter(x=line0['year'], y=line0['Register'], text='Register',
                                                mode='markers+lines',hovertext=line0['State'],
                                                line=dict(color='green',width=1),))
                fig.update_layout(title='YEARLY STATE REGISTER ',plot_bgcolor='white')
                st.plotly_chart(fig, use_container_width=True)

    #===================================APP OPENED USER ANALYSIS===========================================================
        elif selected=='APP OPENED USER' :
            st.warning('Please note: App opened user data available after 2019-Q2', icon="⚠️")

            map_app = map_user.loc[(map_user['Year'] == Year) & (map_user['Quarter'] == Quarter)]
            st_scatter = map_app.groupby(['State'], as_index=False).sum(numeric_only=True)
            dt_scatter = map_app.groupby(['State', 'District'], as_index=False).sum(numeric_only=True)
            #using for loop append app opened user into state,district with lon and lat table
            st_code0 = geo_code  # state with code
            dt0 = geo_dist
            # state trace
            app= []

            for i in st_scatter['App_opened']:
                app.append(i)
            st_code0['App_opened'] = app
            # district trace
            app= []

            for i in dt_scatter['App_opened']:
                app.append(i)
            dt0['App_opened'] = app

            # state trace
            state_1 = px.scatter_geo(st_code0,
                                     lon=st_code0['Longitude'],
                                     lat=st_code0['Latitude'],
                                     text=st_code0['code'],  # code of state
                                     hover_name="state",
                                     hover_data=["App_opened"],
                                     )
            state_1.update_traces(marker=dict(color="white", size=0.3))
            state_1.update_geos(fitbounds="locations", visible=False)
            # districts trace
            dist_1 = px.scatter_geo(dt0,
                                    lon=dt0['Longitude'],
                                    lat=dt0['Latitude'],
                                    size=dt0['App_opened'],
                                    hover_name="District",
                                    hover_data=["State", 'App_opened'],
                                    title='District',
                                    size_max=10)
            dist_1.update_traces(marker=dict(color="darkred", line_width=.05))

            # using choropleth map for plod add trace of state and district
            map_data_1 = px.choropleth(
                st_code0,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                color="App_opened",
                color_continuous_scale='tempo',
                width=900

            )
            map_data_1.update_geos(fitbounds="locations", visible=False, )
            # combining districts states and coropleth

            map_data_1.add_trace(state_1.data[0])
            map_data_1.add_trace(dist_1.data[0])
            mapapp, dist= st.columns([3,.76])
            with mapapp:
                st.write('#####', Year + ' - ', Quarter)
                st.plotly_chart(map_data_1, use_container_width=True)
            # sunbusrt chart - district app user
            with dist:
                dt_app = map_user.loc[(map_user['Year'] == Year) & (map_user['Quarter'] == Quarter) & (map_user['State'] == State)]
                dt_app0 = dt_app.groupby(['Year', 'Quarter', 'State', 'District'], as_index=False).sum(numeric_only=True)
                app1 = dt_app0.sort_values('App_opened', ascending=True, ignore_index=True, axis=0)
                app1['App_opened'] = app1['App_opened'].apply(convert_to_lakh2)
                fig1 = px.sunburst(app1, path=['State', 'District'], values='App_opened',title="DISTRICT APP OPENED USER")
                st.plotly_chart(fig1, use_container_width=True)

            #grouped bar chart - app and register user
            app_trend,top=st.columns([3,.7])
            with app_trend:
                ar_user = agg_user.loc[(agg_user['State'] == State) ]
                ar_user['year']=ar_user['Year']+ar_user['Quarter']
                app_0 = ar_user.groupby(['year','State'], as_index=False).sum()
                app_0['App_opened']=app_0['App_opened'].apply(format_number)
                fig = go.Figure(data=go.Scatter(x=app_0['year'], y=app_0['App_opened'], text='App_opened',
                                                mode='markers+lines', hovertext=app_0['State'],
                                                line=dict(color='darkred',width=.2), ))
                fig.update_layout(title='YEARLY STATE APP OPENED',plot_bgcolor='mintcream')
                st.plotly_chart(fig, use_container_width=True)
            with top:
                st.write('###### TOP 10 APP OPEN USER')
                st.info("NO DATA AVAILABLE")


    #=========================================DEVICE USER ANALYSIS=================================================================
        else:
            year,state,top=st.columns([2,0.9,0.8])
            #horizontal bar -year wise device user
            with year:
                device = st.selectbox('Please select Device', ('Apple','Samsung','OnePlus','Realme', 'Xiaomi', 'Oppo', 'Vivo',
                                                             'Motorola', 'Lenovo','Micromax', 'Huawei', 'Lyf','Gionee', 'Asus','COOLPAD', 'Lava', 'Infinix',
                                                           'HMD Global','Tecno','Others'))

                yr_dev_user = agg_user_device.loc[(agg_user_device['Device_user'] == device) & (agg_user_device['State'] == State)]
                yr_dev_user['year'] = yr_dev_user['Year'] + ' ' + yr_dev_user['Quarter']
                yr_dev = yr_dev_user.groupby(['year', 'Device_user'], as_index=False).sum(numeric_only=True)
                fig1 = px.bar(yr_dev, y='year', x='Total_User', color='Total_User', color_continuous_scale='balance')
                st.plotly_chart(fig1, use_container_width=True)
            #sunbusrt chart-state device user
            with state:
                st_dev_user = agg_user_device.loc[(agg_user_device['Year'] == Year) & (agg_user_device['Quarter'] == Quarter) & (agg_user_device['State'] == State)]
                st_dev = st_dev_user.groupby(['Year','Quarter','State','Device_user'], as_index=False).sum(numeric_only=True)
                st_dev = st_dev.sort_values('Total_User', ascending=False, ignore_index=True, axis=0)
                st_dev['Total_User'] = st_dev['Total_User'].apply(convert_to_thousand)
                fig11 = px.sunburst(st_dev, path=['State','Device_user'], values='Total_User',title="STATE DEVICE USER")
                st.plotly_chart(fig11, use_container_width=True)

            #top device user percentage
            with top:
                device_user = agg_user_device.loc[(agg_user_device['Year'] == Year) & (agg_user_device['Quarter'] == Quarter)]
                top_device_user = device_user.groupby(['Device_user'], as_index=False).sum(numeric_only=True)
                top10_device_per = top_device_user.sort_values('User_percent', ascending=False, ignore_index=True, axis=0)

                top10_device_per['User_percent'] = top10_device_per['User_percent'].apply(convert_to_per)
                st.markdown('###### TOP DEVICE USER PERCENTAGE')
                st.write(top10_device_per[['Device_user', 'User_percent']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)









