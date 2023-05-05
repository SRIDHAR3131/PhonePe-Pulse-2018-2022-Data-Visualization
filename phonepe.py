#-------------------------------------------IMPORTING MODULE------------------------------------------------------------
import os
import json
import time
import pymysql
from sqlalchemy import create_engine

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from streamlit_option_menu import option_menu




#-------------------------------------------NUMBER CONVERSION IN LAKHS AND CRORES---------------------------------------
def convert_to_crore(number):
    crore = number / 10000000
    return f'₹{crore:.1f} Cr'

def convert_to_crore1(number):
    crore1 = number / 10000000
    return f'{crore1:.1f} Cr'
def convert_to_lakh1(number):
    lakh = number / 100000
    return f'{lakh:.1f} L'

def convert_to_per(number):
    per = number/10
    return f'{per:.2f} %'


#--------------------------------PYTHON TO MYSQL DATABASE CONNECT AND UPLOAD DATAFRAME ---------------------------------
engine =create_engine("mysql+pymysql://root:Sridhar15@localhost/phonepepulse")
conn=engine.connect()
# df.to_sql(name='table name', con=engine, if_exists='replace', index=False)


#---------------------------------MYSQL TO PYTHON CONNECT AND READ THE QUERY--------------------------------------------
map_tran = pd.read_sql_table('map_transaction_states_dist', conn) #1
map_user= pd.read_sql_table('map_user_reg_states_dist', conn) #2

agg_tran = pd.read_sql_table('agg_transaction', conn) #3
agg_user = pd.read_sql_table('agg_user', conn) #4
agg_user_device = pd.read_sql_table('agg_user_device', conn) #5

top_tran= pd.read_sql_table('top_transaction', conn) #6
top_user= pd.read_sql_table('top_user', conn) #7

geo_code= pd.read_sql_table('states_code_lon_lat', conn) #8
geo_dist= pd.read_sql_table('state_dist_lat_lon', conn) #9


#------------------------------------------PAGE CONFIGURATION AND LAYOUT------------------------------------------------
st.set_page_config(
     page_title="PhonePe data",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded",)
# Hide the app content
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
# Create a sidebar with options for different pages
option = st.sidebar.selectbox("Select an option", ["Geomap", "Transaction", "User"],key=0)

year_c,state_c=st.sidebar.columns([1.5,2 ])
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
#===============================================Geo Map analysis========================================================

# Create the content of the home
if option == "Geomap":

    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["TRANSACTION VISUALIZATION", "USER VISUALIZATION"],
        icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    if selected=='TRANSACTION VISUALIZATION':
        st.markdown('## PhonePe transaction:pushpin:')

        mat=map_tran.loc[(map_tran['year_wise'] == Year) & (map_tran['quarter_wise'] == Quarter)]
        mat1=mat
        mat2=mat1
        st_scatter = mat1.groupby(['state_wise'], as_index=False).sum(numeric_only=True)
        dt_scatter = mat2.groupby(['state_wise', 'district_wise'], as_index=False).sum(numeric_only=True)
        st_code = geo_code  # state with code
        dt = geo_dist

        # state trace
        amount = []
        count = []
        for i in st_scatter['pay_amount']:
            amount.append(i)

        st_code['amount'] = amount
        for j in st_scatter['pay_count']:
            count.append(j)
        st_code['count'] = count
        # district trace
        amount = []
        count = []
        for i in dt_scatter['pay_amount']:
            amount.append(i)
        dt['amount'] = amount

        for j in dt_scatter['pay_count']:
            count.append(j)
        dt['count'] = count

        # state trace
        state_0 = px.scatter_geo(st_code,
                                     lon=st_code['Longitude'],
                                     lat=st_code['Latitude'],
                                     text=st_code['code'],  # code of state
                                     hover_name="state",
                                     hover_data=["amount", 'count'],
                                     )
        state_0.update_traces(marker=dict(color="white", size=0.3))
        state_0.update_geos(fitbounds="locations", visible=False)
        # districts trace
        dist_0 = px.scatter_geo(dt,
                                    lon=dt['Longitude'],
                                    lat=dt['Latitude'],
                                    size=dt['amount'],
                                    hover_name="District",
                                    hover_data=["State", 'amount', 'count'],
                                    title='District',
                                    size_max=20)
        dist_0.update_traces(marker=dict(color="orangered", line_width=.15))
        # coropleth map
        map_data = px.choropleth(
                st_code,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                hover_name="state",
                hover_data=["amount", 'count'],
                color="amount",
                color_continuous_scale='viridis',

                width=1000,
                height=800
            )
        map_data.update_geos(fitbounds="locations", visible=False, )
        # combining districts states and coropleth
        map_data.add_trace(state_0.data[0])
        map_data.add_trace(dist_0.data[0])

        mapamount=st.columns(1)
        with mapamount[0]:
            st.plotly_chart(map_data, use_container_width=True)

    else:
        st.markdown('## PhonePe user:pushpin:')
        map_reg=map_user.loc[(map_user['year_wise'] == Year) & (map_user['quarter_wise'] == Quarter)]
        map_1=map_reg
        st_scatter = map_reg.groupby(['state_wise'], as_index=False).sum(numeric_only=True)
        dt_scatter = map_1.groupby(['state_wise', 'district'], as_index=False).sum(numeric_only=True)
        st_code0 = geo_code  # state with code
        dt0 = geo_dist
        # state trace
        reg = []
        app = []
        for i in st_scatter['registered_users']:
            reg.append(i)
        st_code0['registered'] = reg
        for j in st_scatter['app_opening']:
            app.append(j)
        st_code0['app_opened'] = app
        # district trace
        reg = []
        app = []
        for i in dt_scatter['registered_users']:
            reg.append(i)
        dt0['registered'] = reg
        for j in dt_scatter['app_opening']:
            app.append(j)
        dt0['app_opened'] = app
        # state trace
        state_1 = px.scatter_geo(st_code0,
                                     lon=st_code0['Longitude'],
                                     lat=st_code0['Latitude'],
                                     text=st_code0['code'],  # code of state
                                     hover_name="state",
                                     hover_data=["registered", 'app_opened'],
                                     )
        state_1.update_traces(marker=dict(color="white", size=0.3))
        state_1.update_geos(fitbounds="locations", visible=False)
        # districts trace
        dist_1 = px.scatter_geo(dt0,
                                    lon=dt0['Longitude'],
                                    lat=dt0['Latitude'],
                                    size=dt0['registered'],
                                    hover_name="District",
                                    hover_data=["State", 'registered', 'app_opened'],
                                    title='District',
                                    size_max=20)
        dist_1.update_traces(marker=dict(color="tomato", line_width=.15))
        # coropleth map
        map_data_1 = px.choropleth(
                st_code0,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                hover_name="state",
                hover_data=["registered", 'app_opened'],
                color="registered",
                color_continuous_scale='picnic',

                width=1000,
                height=800
            )
        map_data_1.update_geos(fitbounds="locations", visible=False, )
        # combining districts states and coropleth
        map_data_1.add_trace(state_1.data[0])
        map_data_1.add_trace(dist_1.data[0])

        mapuser = st.columns(1)
        with mapuser[0]:
            st.plotly_chart(map_data_1, use_container_width=True)






#========================================Transaction analysis state and district========================================
elif option == "Transaction":

    amount,count=st.tabs(['TRANSACTION AMOUNT', 'TRANSACTION COUNT'])
    with amount:

        st.markdown('## STATE TRANSACTION AMOUNT')
        st_tran = agg_tran.loc[(agg_tran['year_wise'] == Year) & (agg_tran['quarter_wise'] == Quarter)]
        stt_tran = st_tran.groupby(['year_wise', 'quarter_wise', 'state_wise'], as_index=False).sum(numeric_only=True)
        stt_tran = stt_tran.sort_values('pay_amount', ascending=False, ignore_index=True, axis=0)
        fig2 = px.bar(stt_tran, x='state_wise', y='pay_amount', color='pay_amount', color_continuous_scale="Viridis",height=500)


        stt1 = st.columns(1)
        with stt1[0]:
            st.write('###', Year + ' - ', Quarter)
            st.plotly_chart(fig2, use_container_width=True)
            # =======================sidebar transaction amount==========================================================
            side0 = st.sidebar.columns(1)
            with side0[0]:
                total_amt = agg_tran.loc[(agg_tran['year_wise'] == Year) & (agg_tran['quarter_wise'] == Quarter)]
                total = total_amt.groupby(['year_wise'], as_index=False).sum(numeric_only=True)
                total['Transaction'] = total['pay_amount'].apply(convert_to_crore)
            tot1 = st.sidebar.columns(1)
            with tot1[0]:
                st.markdown('# Transaction amount')
                st.write('##', Year + ' - ', Quarter)
                ss=st.write(total[['Transaction']].style.hide(axis="index").to_html(), unsafe_allow_html=True)


            # ====================side bar transaction amount======================================================


        st.markdown('## DISTRICT TRANSACTION AMOUNT')

        dt_tran= top_tran.loc[(top_tran['year_wise'] == Year) & (top_tran['quarter_wise'] == Quarter) & (top_tran['state_wise'] == State)]
        dist_tran = dt_tran.groupby(['year_wise','quarter_wise','state_wise','district_wise'], as_index=False).sum(numeric_only=True)
        # pay_mode['pay_count'] = pay_mode['pay_count'].apply(convert_to_crore1)
        fig1 = px.bar(dist_tran, x='district_wise', y='pay_amount', color='district_wise')

        stt0 = st.columns(1)
        with stt0[0]:
            st.write('####',State.upper())
            st.plotly_chart(fig1, use_container_width=True)

        st.markdown('## PAYMENT INSTRUMENT BY YEAR')

        c111= st.columns(1)
        with c111[0]:
            mode = st.selectbox('Please select mode', ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'))

            payment = agg_tran.loc[(agg_tran['payment instrument'] == mode)&(agg_tran['state_wise'] == State)]
            payment['year'] = payment['year_wise'] + ' ' + payment['quarter_wise']
            pay_mode = payment.groupby(['year', 'payment instrument'], as_index=False).sum(numeric_only=True)
            fig = px.bar(pay_mode, x='year', y='pay_amount', color='pay_amount')
        stt = st.columns(1)
        with stt[0]:
            st.write('###', mode + ' analaysis')
            st.plotly_chart(fig, use_container_width=True)


    with count:
        st.markdown('## STATE TRANSACTION COUNT')

        st_count = agg_tran.loc[(agg_tran['year_wise'] == Year) & (agg_tran['quarter_wise'] == Quarter)]
        stt_count = st_count.groupby(['year_wise', 'quarter_wise', 'state_wise'], as_index=False).sum(numeric_only=True)
        stt_count = stt_count.sort_values('pay_count', ascending=True, ignore_index=True, axis=0)
        stt_count['pay_count']= stt_count['pay_count'].apply(convert_to_crore1)
        figg2=px.line(stt_count,x = 'state_wise', y = 'pay_count')
        # figg2 = px.bar(stt_count, x='state_wise', y='pay_count', color='pay_count',color_continuous_scale='Cividis')

        stt11 = st.columns(1)
        with stt11[0]:
            st.write('###', Year + ' - ', Quarter)
            st.plotly_chart(figg2, use_container_width=True)
            # =======================sidebar transactio count==========================================================
            side1 = st.sidebar.columns(1)
            with side1[0]:
                total_count = agg_tran.loc[(agg_tran['year_wise'] == Year) & (agg_tran['quarter_wise'] == Quarter)]
                total1 = total_count.groupby(['year_wise'], as_index=False).sum(numeric_only=True)
                total1['Transaction'] = total1['pay_count'].apply(convert_to_crore1)
            tot1 = st.sidebar.columns(1)
            with tot1[0]:
                st.markdown('# Total transaction')
                st.write('##', Year + ' - ', Quarter)
                st.write(total1[['Transaction']].style.hide(axis="index").to_html(), unsafe_allow_html=True)




        st.markdown('## DISTRICT TRANSACTION COUNT')

        dt_tran = top_tran.loc[(top_tran['year_wise'] == Year) & (top_tran['quarter_wise'] == Quarter) & (top_tran['state_wise'] == State)]
        dist_tran = dt_tran.groupby(['year_wise', 'quarter_wise', 'state_wise', 'district_wise'], as_index=False).sum(numeric_only=True)
        # pay_mode['pay_count'] = pay_mode['pay_count'].apply(convert_to_crore1)
        figg1 = px.bar(dist_tran, x='district_wise', y='pay_amount', color='pay_amount',color_continuous_scale='thermal')

        stt00 = st.columns(1)
        with stt00[0]:
            st.write('####', State.upper())
            st.plotly_chart(figg1, use_container_width=True)

        #
        #
        # st.markdown('## PAYMENT INSTRUMENT COUNT')
        #
        # payment = agg_tran.loc[(agg_tran['year_wise'] == Year) &(agg_tran['quarter_wise'] == Quarter) &(agg_tran['state_wise'] == State) ]
        # pay_mode = payment.groupby(['year_wise','state_wise','payment instrument'], as_index=False).sum(numeric_only=True)
        # # pay_mode['pay_count'] = pay_mode['pay_count'].apply(convert_to_crore1)
        # figg = px.bar(pay_mode, x='payment instrument', y='pay_count', color='payment instrument')
        #
        # stt00 = st.columns(1)
        # with stt00[0]:
        #     st.write('###', Year +'  '+State)
        #     st.plotly_chart(figg, use_container_width=True)


        st.markdown('## PAYMENT INSTRUMENT BY YEAR')
        anii = st.columns(1)
        with anii[0]:
            agg_tran['year'] = agg_tran['year_wise'] + ' ' + agg_tran['quarter_wise']
            pay_mod = agg_tran.groupby(['year', 'payment instrument'], as_index=False).sum(numeric_only=True)
            figkk = px.bar(pay_mod,
                         x="payment instrument",
                         y="pay_count",
                         color='pay_count',
                         color_continuous_scale='icefire',
                         animation_frame='year',
                         hover_name='pay_count',
                        height=600,
                         range_y=[0, 4000000000])
        ani = st.columns(1)
        with ani[0]:
            st.plotly_chart(figkk, use_container_width=True)


#========================================TOP TRANSACTION AND USER STATE AND DISTRICT====================================

    with amount:
        st.write("## TOP 10 STATE AND DISTRICT TRANSACTION")
        state_tran = top_tran.loc[(top_tran['year_wise'] == Year) & (top_tran['quarter_wise'] == Quarter)]
        top_state = state_tran.groupby(['state_wise'], as_index=False).sum(numeric_only=True)
        top_dist = state_tran.groupby(['district_wise'], as_index=False).sum(numeric_only=True)

        top10_tran_amount = top_state.sort_values('pay_amount',ascending=False,ignore_index=True,axis=0)
        top10_dt_tran_amount = top_dist.sort_values('pay_amount', ascending=False, ignore_index=True, axis=0)

        top10_tran_amount['pay_amount'] = top10_tran_amount['pay_amount'].apply(convert_to_crore)
        top10_dt_tran_amount['pay_amount'] = top10_dt_tran_amount['pay_amount'].apply(convert_to_crore)
        # ===============================================pie chart transaction========================================================================================
        pie0=st.columns(1)
        with pie0[0]:

            agg_tran.groupby('year_wise')
            colors = ['red', 'gold', 'mediumturquoise', 'darkorange', 'green']
            fig = go.Figure(data=go.Pie(
                labels=agg_tran['year_wise'],
                values=agg_tran['pay_amount'],
                pull=[0.3, 0.2, 0, 0, 0],
                hole=.3, ))

            fig.update_traces(hoverinfo='percent', textfont_size=15,
                              marker=dict(colors=colors, line=dict(color='#000000', width=5)))
            fig.update_layout(
                title_text="OVERALL TRANSACTION AMOUNT",
                annotations=[dict(text='AMOUNT', x=0.50, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig, use_container_width=True)
        st_amount,st1_amount= st.columns(2)

        with st_amount:
            st.markdown('#### State transaction amount')
            st.write(top10_tran_amount[['state_wise','pay_amount']][0:10].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        with st1_amount:
            st.markdown('#### District transaction amount')
            st.write(top10_dt_tran_amount[['district_wise','pay_amount']][0:10].style.hide(axis="index").to_html(), unsafe_allow_html=True)




    with count:
        st.write("## TOP 10 STATE AND DISTRICT COUNT")
        state1_tran = top_tran.loc[(top_tran['year_wise'] == Year) & (top_tran['quarter_wise'] == Quarter)]
        top_state1 = state1_tran.groupby(['state_wise'], as_index=False).sum(numeric_only=True)
        top_dist1 = state1_tran.groupby(['district_wise'], as_index=False).sum(numeric_only=True)

        top10_tran_count = top_state1.sort_values('pay_count',ascending=False,ignore_index=True,axis=0)
        top10_dt_tran_count = top_dist1.sort_values('pay_count', ascending=False, ignore_index=True, axis=0)
        top10_tran_count['pay_count'] = top10_tran_count['pay_count'].apply(convert_to_crore1)
        top10_dt_tran_count['pay_count'] = top10_dt_tran_count['pay_count'].apply(convert_to_crore1)

        pie1 =st.columns(1)
        with pie1[0]:
            agg_tran.groupby('year_wise')
            colors = ['red', 'gold', 'mediumturquoise', 'darkorange', 'lightgreen']
            fig = go.Figure(data=go.Pie(
                labels=agg_tran['year_wise'],
                values=agg_tran['pay_count'],
                pull=[0.3, 0.2, 0, 0, 0],
                hole=.6, ))

            fig.update_traces(hoverinfo='percent', textfont_size=15,
                              marker=dict(colors=colors, line=dict(color='#000000', width=5)))
            fig.update_layout(
                title_text="OVERALL TRANSACTION COUNT",
                annotations=[dict(text='COUNT', x=0.50, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig, use_container_width=True)
        dt_count, dt_count1 = st.columns(2)
        with dt_count:
            st.markdown('#### State transaction count')
            st.write(top10_tran_count[['state_wise', 'pay_count']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)
        with dt_count1:
            st.markdown('#### District transaction count')
            st.write(top10_dt_tran_count[['district_wise', 'pay_count']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)




#============================================User Analysis state and district===========================================
else:
    Reg,app,dev = st.tabs(['REGISTERED USER', 'APP OPENED','DEVICE USER'])

    with Reg:
        st.markdown('## STATE REGISTERED USER')
        reg_user = agg_user.loc[(agg_user['year_wise'] == Year) & (agg_user['quarter_wise'] == Quarter)]
        reg = reg_user.groupby(['state_wise'], as_index=False).sum( numeric_only=True)
        reg0 = reg.sort_values('registered_users', ascending=False, ignore_index=True, axis=0)
        fig = px.bar(reg0, x='state_wise', y='registered_users', color='registered_users', color_continuous_scale='dense',height=500)

        stt = st.columns(1)
        with stt[0]:
            st.write('###', Year + ' - ', Quarter)
            st.plotly_chart(fig, use_container_width=True)

            # ==============================sidebar register user================================================
            side2 = st.sidebar.columns(1)
            with side2[0]:
                total_reg = agg_user.loc[(agg_user['year_wise'] == Year) & (agg_user['quarter_wise'] == Quarter)]
                total_r = total_reg.groupby(['year_wise'], as_index=False).sum(numeric_only=True)
                total_r['registered_users'] = total_r['registered_users'].apply(convert_to_crore1)
            tot3 = st.sidebar.columns(1)
            with tot3[0]:
                st.markdown('# Total Registered User')
                st.write('##', Year + ' - ', Quarter)
                st.write(total_r[['year_wise', 'registered_users']].style.hide(axis="index").to_html(),
                         unsafe_allow_html=True)



        st.markdown('## DISTRICT REGISTERED USER')
        dt_reg_user = map_user.loc[(map_user['year_wise'] == Year) & (map_user['quarter_wise'] == Quarter) & (map_user['state_wise'] == State)]
        dt_reg = dt_reg_user.groupby(['year_wise', 'quarter_wise', 'district','state_wise'], as_index=False).sum(numeric_only=True)
        dt_reg0= dt_reg.sort_values('registered_users', ascending=False, ignore_index=True, axis=0)
        fig1 = px.bar(dt_reg0, x='registered_users', y='district', color='registered_users',color_continuous_scale='peach',height=550)

        stt0 = st.columns(1)
        with stt0[0]:
            st.write('####', State.upper())
            st.plotly_chart(fig1, use_container_width=True)

            st.write("## TOP 10 REGISTERED USER")

            reg_user = top_user.loc[(top_user['year_wise'] == Year) & (top_user['quarter_wise'] == Quarter)]
            top_reg_user = reg_user.groupby(['state_wise'], as_index=False).sum(numeric_only=True)
            top_dt_reg_user = reg_user.groupby(['district_wise'], as_index=False).sum(numeric_only=True)
            top10_reg_user = top_reg_user.sort_values('registered_users', ascending=False, ignore_index=True, axis=0)
            top10_dt_reg_user = top_dt_reg_user.sort_values('registered_users', ascending=False, ignore_index=True,axis=0)
            top10_reg_user['registered_users'] = top10_reg_user['registered_users'].apply(convert_to_lakh1)
            top10_dt_reg_user['registered_users'] = top10_dt_reg_user['registered_users'].apply(convert_to_lakh1)

            cll1, cll2 = st.columns(2)
            with cll1:
                st.markdown('#### State registered user')
                st.write(top10_reg_user[['state_wise', 'registered_users']][0:10].style.hide(axis="index").to_html(),
                         unsafe_allow_html=True)
            with cll2:
                st.markdown('#### District registered user')
                st.write(
                    top10_dt_reg_user[['district_wise', 'registered_users']][0:10].style.hide(axis="index").to_html(),
                    unsafe_allow_html=True)


    with app:
        st.markdown('## APP OPENED BY STATE USER')
        app_user = agg_user.loc[(agg_user['year_wise'] == Year) & (agg_user['quarter_wise'] == Quarter)]
        app = app_user.groupby(['year_wise', 'quarter_wise', 'state_wise'], as_index=False).sum(numeric_only=True)
        app= app.sort_values('app_opening', ascending=False, ignore_index=True, axis=0)
        figg = px.bar(app, x='state_wise', y='app_opening', color='app_opening',height=700,color_continuous_scale='rainbow')

        stt00 = st.columns(1)
        with stt00[0]:
            st.write('###', Year + ' - ', Quarter)
            st.plotly_chart(figg, use_container_width=True)

            # ========================sidebar app user==============================================
            side3 = st.sidebar.columns(1)
            with side3[0]:
                total_app = agg_user.loc[(agg_user['year_wise'] == Year) & (agg_user['quarter_wise'] == Quarter)]
                total_a = total_app.groupby(['year_wise'], as_index=False).sum(numeric_only=True)
                total_a['app_opening'] = total_a['app_opening'].apply(convert_to_crore1)
            tot4 = st.sidebar.columns(1)
            with tot4[0]:
                st.markdown('# Total App Opened user')
                st.write('##', Year + ' - ', Quarter)
                st.write(total_a[['year_wise', 'app_opening']].style.hide(axis="index").to_html(),unsafe_allow_html=True)



        st.markdown('## APP & REGISTERED USER')

        ar_user = agg_user.loc[(agg_user['year_wise'] == Year) & (agg_user['quarter_wise'] == Quarter)]
        ap_rg = ar_user.groupby(['year_wise', 'quarter_wise', 'state_wise'], as_index=False).sum()
        app_reg = ap_rg.sort_values('registered_users', ascending=True, ignore_index=True, axis=0)

        app_reg['registered_users'] = app_reg['registered_users'].apply(convert_to_lakh1)
        app_reg['app_opening']=app_reg['app_opening'].apply(convert_to_lakh1)

        t1 = go.Bar(

            x=app_reg['state_wise'],
            y=app_reg['registered_users'],
            name='Registered user',
            marker={'color': 'white'}
        )
        t2 = go.Bar(
            x=app_reg['state_wise'],
            y=app_reg['app_opening'],
            name='App opened',
            marker={'color': 'green'}
        )

        dt = [t1, t2]
        layout = go.Layout(barmode='stack',height=650)
        compare = go.Figure(data=dt, layout=layout)

        stt001 = st.columns(1)
        with stt001[0]:
            st.write('###', Year + ' - ', Quarter)
            st.plotly_chart(compare, use_container_width=True)





        st.markdown('## APP OPENED BY DISTRICT USER')

        dt_app = map_user.loc[(map_user['year_wise'] == Year) & (map_user['quarter_wise'] == Quarter) & (map_user['state_wise'] == State)]
        dt_app0 = dt_app.groupby(['year_wise', 'quarter_wise', 'state_wise', 'district'], as_index=False).sum(numeric_only=True)
        app1 = dt_app0.sort_values('district', ascending=True, ignore_index=True, axis=0)
        figg1 = px.bar(app1, x='district', y='app_opening', color='app_opening',color_continuous_scale='electric')

        stt00 = st.columns(1)
        with stt00[0]:
            st.write('####', State.upper())
            st.plotly_chart(figg1, use_container_width=True)

    with dev:

        st.markdown('## STATE DEVICE USER')

        st_dev_user = agg_user_device.loc[(agg_user_device['year_wise'] == Year) & (agg_user_device['quarter_wise'] == Quarter) & (agg_user_device['state_wise'] == State)]
        st_dev = st_dev_user.groupby(['year_wise','quarter_wise','state_wise','Device_used'], as_index=False).sum(numeric_only=True)
        st_dev = st_dev.sort_values('Device_used', ascending=False, ignore_index=True, axis=0)
        fig1 = px.bar(st_dev, x='Device_used', y='user_count', color='Device_used')

        stt0 = st.columns(1)
        with stt0[0]:
            st.write('####', State.upper())
            st.plotly_chart(fig1, use_container_width=True)


        st.markdown('## DEVICE USER')
        c011= st.columns(1)
        with c011[0]:
            device = st.selectbox('Please select Year', ('Apple','Samsung','OnePlus','Realme', 'Xiaomi', 'Oppo', 'Vivo',
                                                         'Motorola', 'Lenovo','Micromax', 'Huawei', 'Lyf','Gionee', 'Asus','COOLPAD', 'Lava', 'Infinix',
                                                       'HMD Global','Tecno','Others'))

        yr_dev_user = agg_user_device.loc[(agg_user_device['Device_used'] == device) & (agg_user_device['state_wise'] == State)]
        yr_dev_user['year'] = yr_dev_user['year_wise'] + ' ' + yr_dev_user['quarter_wise']
        yr_dev = yr_dev_user.groupby(['year', 'Device_used'], as_index=False).sum(numeric_only=True)
        #yr_dev = yr_dev.sort_values('Device_used', ascending=False, ignore_index=True, axis=0)
        fig1 = px.bar(yr_dev, x='year', y='user_count', color='user_count', color_continuous_scale='twilight')

        stt0 = st.columns(1)
        with stt0[0]:
            st.write('####', device + ' - ', State)
            st.plotly_chart(fig1, use_container_width=True)


        device_user = agg_user_device.loc[(agg_user_device['year_wise'] == Year) & (agg_user_device['quarter_wise'] == Quarter)]
        top_device_user = device_user.groupby(['year_wise','quarter_wise','Device_used'], as_index=False).sum(numeric_only=True)

        top10_device_count = top_device_user.sort_values(['user_count'], ascending=False, ignore_index=True, axis=0)
        top10_device_count1 = top_device_user.sort_values(['user_percentage'], ascending=False,ignore_index=True, axis=0)
        top10_device_count['user_count'] = top10_device_count['user_count'].apply(convert_to_crore1)
        top10_device_count1['user_percentage'] = top10_device_count1['user_percentage'].apply(convert_to_per)

        coll1,coll2 = st.columns(2)
        with coll1:
            st.markdown('#### Device user count')
            st.write(top10_device_count[['Device_used', 'user_count']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)
        with coll2:
            st.markdown('#### Device user percentage')
            st.write(top10_device_count1[['Device_used', 'user_percentage']][0:10].style.hide(axis="index").to_html(),unsafe_allow_html=True)






















