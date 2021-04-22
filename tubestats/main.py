#!/usr/bin/python3
# display.py - main script for showing information using streamlit

from datetime import datetime, timedelta

import streamlit as st

from helpers import DataFunctions

@st.cache
def fetch_data(channel_id):
        youtuber_data = DataFunctions(channel_id)
        return youtuber_data

def main():

    ALI_ABDAAL_CHANNEL_ID = 'UCoOae5nYA7VqaXzerajD0lg'

    st.title('Youtube Analysis')
    """
    *by Shivan Sivakumaran 2021*
    ## Introduction
    This page provides a brief analysis of a YouTube Channel.
    """

    channel_id = st.text_input('Please enter Youtube channel ID:', ALI_ABDAAL_CHANNEL_ID)
    if not channel_id:
        st.warning('Please input a Youtube channel ID (e.g. %s)' % ALI_ABDAAL_CHANNEL_ID)
        st.stop()
    youtuber_data = fetch_data(channel_id)

    st.header(youtuber_data.channel_name())
    st.image(youtuber_data.thumbnail_url(), width=400)
    st.write(youtuber_data.channel_description())

    st.header('Quick Statistics')
    st.markdown('Total Number of Videos: `' + '{:,}'.format(int(youtuber_data.video_count())) + '`')
    st.markdown('Join Date: `' + str(youtuber_data.start_date()) + '`')
    st.markdown('Total View Count:  `' + '{:,}'.format(int(youtuber_data.total_stat(stat_type='view'))) + '`')
    st.markdown('Total Comments: `' + '{:,}'.format(int(youtuber_data.total_stat(stat_type='comment'))) + '`')
    st.markdown('Total Watch Time: `' + str(youtuber_data.total_stat(stat_type='watchtime')) + '`')

    st.subheader('Videos')
    """
    List of videos and all relevant features.
    """
    df = youtuber_data.dataframe()
    st.write(df)
    """
    Below is a graph plotting the views of each video over time. The colour represents the like and dislike, the size represents the number of views.
    """
    with st.beta_container():
        first_video_date = df['snippet.publishedAt_REFORMATED'].min().to_pydatetime()
        last_video_date = df['snippet.publishedAt_REFORMATED'].max().to_pydatetime()
        
        def date_slider(date_end=datetime.today()):
            date_start, date_end = st.slider(
                    'Date range to include',
                    min_value=first_video_date, # first video
                    max_value=last_video_date, #value for date_end
                    value=(first_video_date , last_video_date), #same as min value
                    step=timedelta(days=2),
                    format='YYYY-MM-DD',
                    key=999)
            return date_start, date_end
      
        date_start, date_end = date_slider()

        transformed_df = youtuber_data.transform_dataframe(date_start=date_start, date_end=date_end) 
        
        c = youtuber_data.scatter_all_videos(transformed_df)
        st.altair_chart(c, use_container_width=True)
    
    #TODO: display links to most popular video
    #TODO: display links to least popular video (1st video is video link)
    def display_vid_links(data, num):
            st.write('Here are links to the videos:')
            for i in range(num):
                title, link = data(i)
                st.markdown(str(i+1) +'. ' + '[' + title +']' + '(' + link + ')')
    
    """
    Again my opinion, views are a good example of well performing videos. The content is engaging enough and liked to be recommended and viewed more often.
    """
    st.subheader('Most Popular Videos')
    #st.write(most_viewed)
    #display_vid_links(youtuber_data.most_viewed_video, 5)
    
    #test link for video
    ALI_VID_TEST = 'https://www.youtube.com/watch?v=1ArVtCQqQRE'
    st.video(data=ALI_VID_TEST)
    

 
    dislike_num = st.slider('Number of videos', 5, 20, key=0)
    disliked = youtuber.disliked_videos(dislike_num)
    st.write(disliked)
    display_vid_links(youtuber.most_disliked_video, dislike_num)
    st.subheader('Most Unpopular Videos')
    """
    Remaining a hypothesis, people actively show their digust for a video by hitting dislike video. Hence, we are provided with a like-dislike ratio. We also have the sum to ensure we have enough likes/dislikes for fair comparison.
    """

   
    st.subheader('Videos by time difference')
    youtuber.time_difference_calculate()
    timed_num = st.slider('Number of videos', 10, 30, key=2)
    time_diff = youtuber.list_time_difference_ranked(timed_num)
    st.write(time_diff)
    
if __name__ == '__main__':
        main()