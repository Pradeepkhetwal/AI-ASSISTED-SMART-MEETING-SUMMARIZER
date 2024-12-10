import json
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import requests
from get_results import *
import assemblyai as aai
# AssemblyAI API endpoint for audio/video transcription
ASSEMBLYAI_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

# Your AssemblyAI API key (replace with your actual API key)
ASSEMBLYAI_API_KEY = "d2d4a318dbd14ecfa920c5ff195e49e4"
# load json data to show initial data
response = open('./json/response.json')
data = json.load(response)
utterances = data['utterances']
# save speaker label utterances data to dataframe for ease of visualization
utterances_df = pd.DataFrame(utterances)
utterances_df['start_str'] = utterances_df['start'].apply(convertMillis)
# variable to track whether to show initial json data or data from an uploaded file
uploaded = False

## body



st.title("AI Assisted Smart Meeting Summarizer")
uploaded_file = st.file_uploader("Please Upload a  video or audio of a meeting ")



if uploaded_file is not None:
    polling_endpoint = upload_to_AssemblyAI(uploaded_file)
    # status of file submitted to AAI for transcription
    status = 'submitted'

# AssemblyAI API endpoint for audio transcription
ASSEMBLYAI_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

# Your AssemblyAI API key (replace with your actual API key)
aai.settings.api_key = "d2d4a318dbd14ecfa920c5ff195e49e4"

# Streamlit app layout




if uploaded_file:
    st.audio(uploaded_file)

    # Transcribe using AssemblyAI 
    st.write("Summarizing the meeting...")
    
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(uploaded_file,config = aai.TranscriptionConfig(summarization = True))
    
    st.write(transcript.summary)
  
    while status != 'completed':
        uploaded = True
        polling_response = requests.get(polling_endpoint, headers=headers)
        status = polling_response.json()['status']
                 
        # display speaker label data when transcription is completed. 
        if status == 'completed':

            
            st.subheader('Turn-by-Turn Conversation Recap')
            utterances = polling_response.json()['utterances']
            utterances_df = pd.DataFrame(utterances)
            utterances_df['start_str'] = utterances_df['start'].apply(convertMillis)

            for index, row in utterances_df.iterrows():
                st.markdown(f'#### Speaker {row["speaker"]} - __{row["start_str"]}__')
                st.markdown(f'{row["text"]}')

# displays data from static json file when page first loads
# if uploaded == False:
#     st.video('https://youtu.be/Da3SBwlgcDc')

#     st.title('Turn-by-Turn Conversation Recap')

    # display speaker label data
    for index, row in utterances_df.iterrows():
        st.markdown(f'#### Speaker {row["speaker"]} - __{row["start_str"]}__')
        st.markdown(f'{row["text"]}')



    
        
        













