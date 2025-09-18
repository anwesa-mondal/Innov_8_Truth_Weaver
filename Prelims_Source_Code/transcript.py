from pathlib import Path
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

def transcribe_and_merge(client, audio_files, output_file="transcript.txt"):
    with open(output_file, "w", encoding="utf-8") as outfile:
        for i, audio_file in enumerate(audio_files, start=1):
            try:
                print(f"[{i}/{len(audio_files)}] Processing: {audio_file}")
                audio_file_str = str(audio_file)
                with open(audio_file_str, "rb") as file:
                    transcription = client.audio.transcriptions.create(
                        file=(audio_file_str, file.read()),
                        model="whisper-large-v3-turbo",
                        response_format="verbose_json",
                    )

                transcript_text = transcription.text.strip()
                clean_name = Path(audio_file).stem + ".mp3"  # force .mp3 extension
                outfile.write(f"{clean_name}: {transcript_text}\n\n")

            except Exception as e:
                print(f"❌ Error processing {audio_file}: {e}")

    print(f"📄 All transcripts merged into {output_file}")


def main():
    client = Groq(api_key=groq_api_key)

    # Input folder containing audio files
    input_folder = r"eval_audios"

    # Get all audio files (mp3, wav, flac)
    audio_files = sorted(Path(input_folder).glob("*.*"))
    audio_files = [f for f in audio_files if f.suffix.lower() in [".mp3", ".wav", ".flac"]]

    if not audio_files:
        print(f"⚠️ No audio files found in {input_folder}")
        return

    # Transcribe and merge directly
    transcribe_and_merge(client, audio_files, output_file="transcript.txt")


if __name__ == "__main__":
    main()
