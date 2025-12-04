import os

os.environ["COQUI_TOS_AGREED"] = "1"
os.environ["TTS_HOME"] = os.path.join(os.getcwd())
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from TTS.api import TTS
import sys
import io
import tempfile
import uvicorn
import subprocess

print("============================================================")

try:
    print("[INFO] Checking for model files (this may trigger download)...")
    print("[INFO] If downloading, progress will appear below:")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    tts.to("cpu")
except Exception as e:
    print("[ERROR] Failed to load or download model:", e)
    print("============================================================")
    raise
print("============================================================\n")

app = FastAPI()


class SpeakRequest(BaseModel):
    agent: str
    text: str
    language: str = "en"


@app.post("/speak")
async def speak(req: SpeakRequest):
    agent_name = req.agent.lower()
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    agents_dir = os.path.join(base_dir, "agents")
    voice_path = os.path.join(agents_dir, f"{agent_name}.mp3")

    if not os.path.exists(voice_path):
        raise HTTPException(
            status_code=404, detail=f"Voice file not found for agent: {req.agent}"
        )

    # create temporary wav file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    # generate audio
    tts.tts_to_file(
        text=req.text,
        file_path=tmp_path,
        speaker_wav=voice_path,
        language=req.language,
    )

    mp3_io = io.BytesIO()

    # Determine ffmpeg path
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            ffmpeg_exe = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
        else:
            ffmpeg_exe = os.path.join(os.path.dirname(sys.executable), 'ffmpeg.exe')
    else:
        local_ffmpeg = os.path.join(base_dir, 'ffmpeg.exe')
        if os.path.exists(local_ffmpeg):
            ffmpeg_exe = local_ffmpeg
        else:
            ffmpeg_exe = "ffmpeg"

    ffmpeg_cmd = [
        ffmpeg_exe,
        "-y",
        "-i",
        tmp_path,
        "-vn",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-b:a",
        "192k",
        "-f",
        "mp3",
        "pipe:1",
    ]

    try:
        proc = subprocess.Popen(
            ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        mp3_data = proc.stdout.read()
        mp3_io.write(mp3_data)
        mp3_io.seek(0)
    finally:
        os.remove(tmp_path)

    return StreamingResponse(mp3_io, media_type="audio/mpeg")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5005)
