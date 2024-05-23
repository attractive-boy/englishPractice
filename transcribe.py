from flask import Blueprint, request, jsonify, send_file
from iflytek_asr import upload_audio
import os
import time
from dotenv import load_dotenv

from iflytek_t2a import text_to_voice

# Load environment variables from .env file
load_dotenv()

# 配置 iFLYTEK API 的 app_id 和 secret_key
app_id = os.getenv('VOICE_TO_TEXT_API_ID', '')
secret_key = os.getenv('VOICE_TO_TEXT_API_SECRET_KEY', '')

transcribe_bp = Blueprint('transcribe', __name__)

@transcribe_bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio_file']
    file_name = audio_file.filename
    temp_file_path = os.path.join('tmp/', file_name)
    audio_file.save(temp_file_path)

    try:
        # 上传音频并获取订单 ID appid, secret_key, upload_file_path
        result = upload_audio(appid=app_id, secret_key=secret_key, upload_file_path=temp_file_path)
        transcription = result
        print('Transcription Result:', transcription)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(temp_file_path)  # 删除临时保存的音频文件

    return jsonify({"transcription": transcription}), 200

@transcribe_bp.route('/transcribeToVoice', methods=['POST'])
def transcribe():
    if 'text' not in request.form:
        return jsonify({"error": "No text provided"}), 400
    
    text = request.form['text']
    
    try:
        audio_data = text_to_voice(text)
        file_path = "output_audio.mp3"
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data)
        return send_file(file_path, mimetype='audio/mpeg', as_attachment=True, attachment_filename='output_audio.mp3')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
