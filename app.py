import streamlit as st
import preprocessor  # Ensure you have this module
import functions  # Ensure you have this module
import matplotlib.pyplot as plt  # Corrected import
import seaborn as sns

# Sidebar title
st.sidebar.title('WhatsApp Chat Analyzer')

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file", key="file_uploader")

if uploaded_file is None:
    st.markdown("""
        Please export your WhatsApp chat without media for Analysis
    """)
else:
    # Read file as bytes and decode
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess data
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_details = df['user'].unique().tolist()

    # Remove 'Group Notification' and add 'OverAll'
    if 'Group Notification' in user_details:
        user_details.remove('Group Notification')
    user_details.sort()
    user_details.insert(0, 'OverAll')

    # User selection
    selected_user = st.sidebar.selectbox('Show Analysis as:', user_details)

    # Analyze button
    if st.sidebar.button('Analyse'):

        # Fetch statistics
        num_msgs, num_med, link = functions.fetch_stats(selected_user, df)

        # Display overall statistics
        st.title('OverAll Basic Statistics')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Messages')
            st.subheader(num_msgs)
        with col2:
            st.header('Media Shared')
            st.subheader(num_med)
        with col3:
            st.header('Links Shared')
            st.subheader(link)

        # Monthly timeline
        timeline = functions.monthly_timeline(selected_user, df)
        st.title('Monthly Timeline')
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['msg'], color='maroon')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Daily timeline
        daily_timeline = functions.daily_timeline(selected_user, df)
        st.title('Daily Timeline')
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date'], daily_timeline['msg'], color='purple')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list = functions.activity_map(selected_user, df)
        with col1:
            st.header('Most Active Month')
            fig, ax = plt.subplots()
            ax.bar(active_month_df['month'], active_month_df['msg'], color='skyblue')
            ax.bar(month_list[month_msg_list.index(max(month_msg_list))], max(month_msg_list), color='green', label='Highest')
            ax.bar(month_list[month_msg_list.index(min(month_msg_list))], min(month_msg_list), color='red', label='Lowest')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header('Most Active Day')
            fig, ax = plt.subplots()
            ax.bar(active_day_df['day'], active_day_df['msg'], color='orange')
            ax.bar(day_list[day_msg_list.index(max(day_msg_list))], max(day_msg_list), color='green', label='Highest')
            ax.bar(day_list[day_msg_list.index(min(day_msg_list))], min(day_msg_list), color='red', label='Lowest')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # Most active users (Only for OverAll)
        if selected_user == 'OverAll':
            st.title('Most Active Users')
            x, percent = functions.most_chaty(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x, color='cyan')
                st.pyplot(fig)
            with col2:
                st.dataframe(percent)

        # WordCloud
        df_wc = functions.create_wordcloud(selected_user, df)
        st.title('Most Common Words')
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Footer
        st.markdown("**By - Mahesh Kawhale")
