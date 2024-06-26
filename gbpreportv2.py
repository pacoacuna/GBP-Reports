import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def process_data(file):
    data = pd.read_csv(file)
    data['date'] = pd.to_datetime(data['date'])
    data['year_month'] = data['date'].dt.to_period('M')
    monthly_calls = data.groupby(['account_name', 'year_month'])['call_clicks'].sum().reset_index()
    pivot_table = monthly_calls.pivot(index='account_name', columns='year_month', values='call_clicks').fillna(0)
    pivot_table.columns = pivot_table.columns.astype(str)
    return pivot_table, monthly_calls


def plot_data(monthly_calls):
    accounts = monthly_calls['account_name'].unique()
    for account in accounts:
        account_data = monthly_calls[monthly_calls['account_name'] == account]
        plt.figure()
        plt.plot(account_data['year_month'].astype(str), account_data['call_clicks'], marker='o')
        for i, txt in enumerate(account_data['call_clicks']):
            plt.annotate(txt, (account_data['year_month'].astype(str).iloc[i], account_data['call_clicks'].iloc[i]),
                         textcoords="offset points", xytext=(0, 10), ha='center')
        plt.title(f'Call Clicks per Month for {account}')
        plt.xlabel('Month')
        plt.ylabel('Call Clicks')
        plt.xticks(rotation=45)
        st.pyplot(plt)


st.title('Google Business Profile Call Clicks Report')

uploaded_file = st.file_uploader('Upload your CSV file', type='csv')

if uploaded_file is not None:
    st.write('Processing your file...')
    pivot_table, monthly_calls = process_data(uploaded_file)

    st.write('### Monthly Call Clicks by Account')
    st.dataframe(pivot_table)

    st.download_button(
        label="Download data as CSV",
        data=pivot_table.to_csv().encode('utf-8'),
        file_name='monthly_call_clicks_by_account.csv',
        mime='text/csv',
    )

    st.write('### Call Clicks per Month for Each Account')
    plot_data(monthly_calls)