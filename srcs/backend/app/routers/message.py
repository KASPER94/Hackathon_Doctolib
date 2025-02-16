import io
import json
import os
import time
import base64
import asyncio

from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()

# LOAD THE MEDIAPIPES metrics
# angles_exercice_batch = angles_exercice_json_exemple
# angles_patient_batch = angles_patient_json_exemple

# PROMPT
SYSTEM_INSTRUCTIONS = "You are a helpful physiotherapist assistant that talks to a patient. Your task is to analyze a patient's squat movement data to provide clear and concise feedback in 10 words or less. If the exercise is well executed, say nothing, or encourage"
# USER_INSTRUCTIONS = f"""As a physiotherapist, your task is to analyze a patient's movement data to provide clear and concise feedback in 5 words or less. \
#         The feedback needs to help the patient to correct their movement. You absolutly can't use the word "angles" in your answer and try to be a human as much as possible. \
#             You will be provided with two JSON datasets:

# 	**Patient's Angles JSON**: Contains the patient's recorded angles for the same body parts during the exercise:
#     {angles_patient_batch}

# **Instructions:**
# - Compare the patient's angles to the target angles.
# - Identify any deviations from the target angles.
# - Provide specific feedback to the patient on how to adjust their posture or movements to achieve the correct angles.
#     """


async def stream_tts(text, websocket):
    
    tts_start_time = time.time()
    # Create the gTTS object to convert text-to-speech
    tts = gTTS(text=text, lang="en")

    # Create a BytesIO buffer to hold the mp3 data in memory
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)

    # Reset the buffer's pointer to the beginning
    audio_fp.seek(0)
    # Convertir en Base64
    audio_base64 = base64.b64encode(audio_fp.read()).decode("utf-8")

    # Envoyer l'audio au frontend
    await websocket.send_text(json.dumps({"audio": audio_base64}))

    tts_duration = time.time() - tts_start_time
    print(f"TIME: Text-to-speech: {tts_duration:.2f} seconds.")

    # Load the audio data into an AudioSegment (specifying that the format is mp3)
    # audio = AudioSegment.from_file(audio_fp, format="mp3")

    # Play the audio segment (this call blocks until playback is complete)
    # play(audio)
    # tts_duration = time.time() - tts_start_time
    # print(f"TIME: Text-to-speech: {tts_duration:.2f} seconds.")
 
async def llm(frames, gt, websocket, model="gpt-4o"):  # ✅ Ajout d'async
    USER_INSTRUCTIONS = f"""The feedback needs to help the patient to correct their movement. You absolutly cannot use the word "angles" in your answer and try to be a human as much as possible. \
            You will be provided with a JSON datasets:
      Patient's Angles JSON: Contains the patient's recorded angles for the same body parts during the exercise:
          {frames}
      Instructions:
      Check the angles of patient inside the json file
      Identify any deviations
      Provide specific feedback to the patient on how to adjust their posture or movements to achieve the correct angles.
      """
    
    # ✅ Appel OpenAI LLM
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    llm_start = time.time()
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        {"role": "user", "content": USER_INSTRUCTIONS},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    llm_duration = time.time() - llm_start

    answer = response.choices[0].message.content
    print(f"🧠 Réponse LLM: {answer}")
    print(f"⏳ Temps de traitement LLM : {llm_duration:.2f} s.")

    # ✅ Correction : Attendre `stream_tts`
    await stream_tts(answer, websocket)
    # return answer

# text = llm()
# stream_tts(text)