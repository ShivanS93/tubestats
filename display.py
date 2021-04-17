#!/usr/bin/python3
# display.py - main programme for showing information using streamlit


import streamlit as st
from PIL import Image

from functions import YT_functions

youtuber = YT_functions()
ali.load_data()
df = youtuber.transformed_data()


st.title('Youtube Analysis')
"""
## Introduction

"""

st.write('Total Number of Videos: ', str(ali.total_videos()))
st.write('Total View Count:  ' + '{:,}'.format(int(ali.total_stat(stat_type='view'))))
st.write('Total Comments: ' + '{:,}'.format(int(ali.total_stat(stat_type='comment'))))
st.write('Total Watch Time: ', str(ali.total_stat(stat_type='watchtime')))

st.subheader('His Videos')
"""
Here are all his videos and relevant features.
"""
st.write(df)

"""
Below is a graph plotting the views of each video over time. The colour represents the like and dislike, the size represents the number of views.
"""

views = st.slider('Show videos above natural log of view', 0, int(ali.max_views()), key=999)
ratio = st.slider('Show video above like-dislike ratio', 0.0, 1.0, key=998)
c = ali.scatter_all_videos(views, ratio)
st.altair_chart(c, use_container_width=True)

ali.snip_dates()
"""
We can see Ali takes his YouTube channel more serious around mid-June 2017, so videos before this are snipped from analysis.
"""

st.subheader('Most Unpopular Videos')
"""
People actively show their digust for a video by hitting dislike video (my hypothesis). Hence, we are provided with a like-dislike ratio. We also have the sum to ensure we have enough likes/dislikes for fair comparison.
"""
def display_vid_links(data, num):
    st.write('Here are links to the videos:')
    for i in range(num):
        title, link = data(i)
        st.markdown(str(i+1) +'. ' + '[' + title +']' + '(' + link + ')')

dislike_num = st.slider('Number of videos', 5, 20, key=0)
disliked = ali.disliked_videos(dislike_num)
st.write(disliked)
display_vid_links(ali.most_disliked_video, dislike_num)

st.subheader('Most Popular Videos')
"""
Again my opinion, views are a good example of well performing videos. The content is engaging enough and liked to be recommended and viewed more often.
"""
view_num = st.slider('Number of videos', 5, 20, key=1)
most_viewed = ali.viewed_videos(view_num)
st.write(most_viewed)
display_vid_links(ali.most_viewed_video, view_num)

st.subheader('Videos by time difference')
ali.time_difference_calculate()
timed_num = st.slider('Number of videos', 10, 30, key=2)
time_diff = ali.list_time_difference_ranked(timed_num)
st.write(time_diff)

st.altair_chart(ali.jitter_plot(), use_container_width=True)
