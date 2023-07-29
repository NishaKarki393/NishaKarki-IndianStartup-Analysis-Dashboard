#  --> importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import streamlit as st


# -->  File reading and making date datetime
df = pd.read_csv('cleanedStartupFile.csv')

df['date'] = pd.to_datetime(df['date'])
df.set_index('date',inplace=True)

# --> cleaning remaining data
df = df.replace(['Accel Partners India', 'Accel Partner', 'Accel Partners'], 'Accel Partners', regex=True)
df = df.replace(['Accel Partnerss'], 'Accel Partners', regex=True)
df = df.replace(['Accel Partners,'], 'Accel Partners', regex=True)

# --> reading second file for investors list
df2 = pd.read_csv('cleanedStartupFile2.csv')
df2['date'] = pd.to_datetime(df2['date'], format='%d-%m-%Y')
df2.set_index('date',inplace=True)
# --> cleaning remaining data
df2 = df2.replace(['Accel Partners India', 'Accel Partner', 'Accel Partners'], 'Accel Partners', regex=True)
df2 = df2.replace(['Accel Partnerss'], 'Accel Partners', regex=True)
df2 = df2.replace(['Accel Partners,'], 'Accel Partners', regex=True)




#--> basic layouts
st.sidebar.header('Overall Analysis')
option = st.sidebar.selectbox('Choose One',['Project Details','Overall Analysis', 'Startups', 'Investors'])

st.header('Indian Startup Funding Analysis (2015-2020)')


#=====================================================================================
# Code for getting  unique investors list for Investors dropdown
investor_list = []

for i in df['investors'].str.split(', '):
    if len(i)>1:
        for j in i:
            if j not in investor_list:
                investor_list.append(j)
    else:
        investor_list.append(i[0])

investor_list = set(investor_list)
# st.write(len(investor_list))



#For investor list 
investor_list2 = []

for i in df2['investors'].str.split(', '):
    if len(i)>1:
        for j in i:
            if j not in investor_list2:
                investor_list2.append(j)
    else:
        investor_list2.append(i[0])

investor_list2 = set(investor_list2)
# st.write(len(investor_list2))

#================================================================================================

if option == 'Project Details':
    st.markdown(""" <h3> <u>Overview:<u/> </h3> """, unsafe_allow_html=True )
    st.markdown(""" <i> <h5>
 This project analyzes startup funding data in India from 2015 to 2020 using Python, NumPy, Pandas, Matplotlib, and Streamlit. The goal is to gain insights into the trends and patterns in startup funding during this period.</i>
            """, unsafe_allow_html=True) 
    
    st.image("Project-Image.jpg")
    st.write(""" <h4> Key Findings:</h4>
             

1. Increasing Funding Trends:<br>
Over the analyzed period, there has been a significant increase in the amount of funding received by startups. This indicates a positive growth trend in the Indian startup ecosystem.

2. Decline in Startup Count:<br>
Contrary to the rising funding amounts, the number of startups appears to be declining. This observation is crucial and may require further investigation to understand the reasons behind this trend.(in 2020 Covid is major cause of it)

3. Dominance of E-Commerce Sector:<br>
The majority of funded startups belong to the E-Commerce sector. This finding highlights the popularity and potential of the E-Commerce industry in India during the given time frame.

4. Bangalore as the Startup Hub:<br>
Bangalore emerges as the leading city for startups, with a considerable concentration of funded ventures. The city's vibrant startup ecosystem and favorable business environment likely contribute to this dominance.
""", unsafe_allow_html=True)



    #------------------------------- PART 1 - OVERALL ANALYSIS------------------------------------
elif  option == 'Overall Analysis':
    st.header('Overall Analysis')

    #--> metrics for overall analysis
    Total = df['amount'].sum()
    Max = df['amount'].max()
    Avg = round(df['amount'].mean(),2)
    Funded_Startup = df['startup'].count() 

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total',f"{Total} Cr")

    with col2:
        st.metric('Max',f"{Max} Cr")

    with col3:
        st.metric('Avg',f"{Avg} Cr")

    with col4:
        st.metric('Startup Funded',Funded_Startup)

    st.write(""" """)
    st.write(""" """)
    st.write(""" """)
    st.write(""" """)


    st.subheader('MOM Line plot for each company 2015-2020')
    # --> codes for plotting graphs
    option2 = st.selectbox('Options',['Total Funding', 'Counts'])

    if option2 == 'Total Funding':
        temp_df = df.resample('M')['amount'].sum().to_frame().reset_index()
        temp_df['date'] = temp_df['date'].astype('str')
        temp_df['date'] = temp_df['date'].str[0:7]
        temp_df.set_index('date', inplace=True)


        # st.markdown('## MOM total funding 2015-2020')   
        fig,ax = plt.subplots(figsize=(15,8))
        ax.plot(temp_df.index, temp_df.values)
        plt.xticks(rotation=90)
        plt.title('MOM total funding  2015-2020')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        st.pyplot(fig) 



    if option2 == 'Counts':
        temp_df2 = df.resample('M')['startup'].count().to_frame().reset_index()
        temp_df2['date'] = temp_df2['date'].astype('str')
        temp_df2['date'] = temp_df2['date'].str[0:7]
        temp_df2.set_index('date', inplace=True)

        fig,ax = plt.subplots(figsize=(15,8))
        ax.plot(temp_df2.index, temp_df2.values)
        plt.xticks(rotation=90)
        plt.title('MOM total  counts of startups 2015-2020')
        plt.xlabel('Date')
        plt.ylabel('Count')

        st.pyplot(fig) 


    st.write(""" """)
    st.write(""" """)
    st.write(""" """)
    st.write(""" """)

    st.subheader('Sectorwise analysis pie diagram 2015-2020')
    option3 = st.selectbox('Options',['Total Sector Funding', 'Sector Counts'])

    if option3 ==  'Total Sector Funding':
        temp_df4 = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(7)
        fig,ax = plt.subplots(figsize=(5,4))
        ax.pie(temp_df4.values,labels = temp_df4.index, autopct = '%0.1f%%',textprops={'fontsize': 5})
        plt.title('Top 7 sectors which got maximum funding',  fontsize=5)

        st.pyplot(fig) 

    
    if option3 == 'Sector Counts':
        temp_df3 = df['vertical'].value_counts().head(7)
        fig,ax = plt.subplots(figsize=(5,4))
        ax.pie(temp_df3.values,labels = temp_df3.index, autopct = '%0.1f%%',textprops={'fontsize': 5})
        plt.title('Top 7 sectors by count', fontsize=5)
        st.pyplot(fig) 


    col1,col2 = st.columns(2)

    with col1:
            # displaying top investor
        st.header("Types of funding")
        funding_types = sorted(df['round'].unique())
        funding_types_ser = pd.Series(funding_types, name='Types of Funding')
        st.dataframe(funding_types_ser,use_container_width=False, width=400)




    with col2:
    #bar plot
        st.header('Top 10 City wise funding')

        temp_df5 = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
        fig,ax = plt.subplots(figsize=(10,10))
        ax.bar(temp_df5.index, temp_df5.values )
        plt.title('top 10 cities funded')
        plt.xlabel('City')
        plt.ylabel('fund')
        plt.xticks(rotation=90)
        st.pyplot(fig) 



    st.header('Top Investor')
    max_amount = df['amount'].max()
    top_investor = (df[df['amount'] == max_amount][['investors','amount']]).set_index('investors')
    st.dataframe(top_investor, use_container_width=False, width=250)




    #------------------------------- PART 2 - STARTUP ANALYSIS------------------------------------

elif option == 'Startups':

    startup_list = sorted(df['startup'].unique())  #cal

    selected_startup =st.sidebar.selectbox('Option',startup_list )
    btn = st.sidebar.button('Find Startup Details')
    if btn:
        st.header(selected_startup)


        col1, col2, col3 = st.columns(3)

        with col1:
                #vertical
                st.header('Related Industry')
                startup_list = pd.Series(df[df['startup'] == selected_startup]['vertical'].unique(), name='Vertical')
                st.dataframe(startup_list, hide_index=True, width=250)


        with col2:
                #subvertical
                st.header('Sub Industry')
                startup_list = pd.Series(df[df['startup'] == selected_startup]['subvertical'].unique(), name='SubVertical')
                startup_list = startup_list[startup_list.notnull()]
                st.dataframe(startup_list, hide_index=True,  width=250)


        with col3:
                #city
                st.header('Location')
                startup_list = pd.Series(df[df['startup'] == selected_startup]['city'].unique(), name='City')
                st.dataframe(startup_list, hide_index=True,  width=250)

    

#---> second row 
        col1, col2, col3 = st.columns(3)

        with col1:
                #round
                st.header('Inversment Round')
                startup_list = pd.Series(df[df['startup'] == selected_startup]['round'].unique(), name='round')
                st.dataframe(startup_list, hide_index=True,  width=250)


        with col2:
                #investors (var: investor_list)
                st.header("inverstors")

                lst = []

                for i in df['investors'].str.split(', '):
                    if len(i)>1:
                        for j in i:
                            if j not in lst:
                                lst.append(j)

                    else:
                        lst.append(i[0])

                investor_list = pd.Series(list(set(lst)),name='investors')
                st.dataframe(investor_list,  width=250, hide_index=True)


        with col3:
                #date
                st.header('Investment Dates')
                dates = pd.Series(df[df['startup'] == selected_startup].index.date, name='Date').sort_values()
                st.dataframe(dates, hide_index=True, width=250)


        #invested amount
        st.write(""" """)
        st.write(""" """)
        st.write(""" """)
        st.write(""" """)

        st.subheader('Total Amount Invested')
        amount = pd.Series(round(df[df['startup'] == '1mg']['amount'].sum(),2), name='Amount')
        st.dataframe(amount,hide_index=True, width=100)
                




    #------------------------------- PART 3 - Investor ANALYSIS------------------------------------
          
elif option == 'Investors':

    df2 = df2[df2['amount'] != 0]
    selected_investor = st.sidebar.selectbox('Option', investor_list2)
    btn = st.sidebar.button('Find Investors details')
    if btn:
        st.header(selected_investor)
        st.write(""" """)
        st.write(""" """)
        st.write(""" """)
        st.write(""" """)

        #   most recent investments
                
        st.header('Recent Investments')
        filtered_df = df2[df2['investors'].str.contains(selected_investor)]
        filtered_df = filtered_df.sort_index(ascending=False)
        filtered_df = filtered_df.iloc[0:3, :]
        filtered_df = filtered_df[['startup','vertical','city','round', 'amount']]
        filtered_df.index = filtered_df.index.date
        st.dataframe(filtered_df)


        col1,col2 = st.columns(2)


        #   biggest  investments
        with col1:
            st.header('Biggest  investments')
            filtered_df = df2[df2['investors'].str.contains(selected_investor)]
            filtered_df =filtered_df.sort_values(by='amount', ascending=False)[['startup','amount']].head()
            filtered_df = filtered_df.drop_duplicates()
            fig,ax= plt.subplots(figsize=(6,4.2))
            ax.bar(filtered_df['startup'], filtered_df['amount'])

            ax.set_xlabel('Statups')
            ax.set_ylabel('Amounts in crores')
            st.pyplot(fig, use_container_width=True)


        with col2:
            st.header('Top Sector Invested In')

            filtered_df = df2[df2['investors'].str.contains(selected_investor)]
            filtered_df =filtered_df.sort_values(by='amount', ascending=False)[['vertical','amount']]
            filtered_df = filtered_df.drop_duplicates()
            filtered_df = filtered_df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()

            fig1,ax1 = plt.subplots(figsize=(5,5))
            ax1.pie(filtered_df.values, labels=filtered_df.index, autopct='%0.1f%%')
            st.pyplot(fig1, use_container_width=True)



        col1,col2 = st.columns(2)

        #  Stagewise funding top
        with col1:
            st.header('Stagewise Funding')
            filtered_df = df2[df2['investors'].str.contains(selected_investor)]
            filtered_df = filtered_df.sort_values(by='amount', ascending=False)[['round','amount']]
            filtered_df = filtered_df.drop_duplicates()
            filtered_df = filtered_df.groupby('round')['amount'].sum().sort_values(ascending=False).head()
            filtered_df = filtered_df[filtered_df.values != 0.00].head()

            fig2,ax2 = plt.subplots(figsize=(5,5))
            ax2.pie(filtered_df.values, labels=filtered_df.index, autopct='%0.1f%%')
            st.pyplot(fig2, use_container_width=True)



        with col2:
            st.header('City Wise Funding')
            filtered_df = df2[df2['investors'].str.contains(selected_investor)]
            filtered_df = filtered_df.sort_values(by='amount', ascending=False)[['city','amount']]
            filtered_df = filtered_df.drop_duplicates()
            filtered_df = filtered_df.groupby('city')['amount'].sum().sort_values(ascending=False).head()
            filtered_df = filtered_df[filtered_df.values != 0.00].head()

            fig3,ax3 = plt.subplots(figsize=(5,5))
            ax3.pie(filtered_df.values, labels=filtered_df.index, autopct='%0.1f%%')
            st.pyplot(fig3, use_container_width=True)

