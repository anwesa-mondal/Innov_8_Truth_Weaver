# Innov_8_Truth_Weaver

An AI pipeline for **truth extraction from speech**.  
This project transcribes evaluation audio files, analyzes them for contradictions and exaggerations, and produces both raw and cleaned transcripts.

---

Setup :

### 1. Clone this repo
```bash
git clone https://github.com/anwesa-mondal/Innov_8_Truth_Weaver.git
cd Innov_8_Truth_Weaver
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API key
Go to [Groq Console](https://console.groq.com/), create an API key, then create a `.env` file in the project root:

```
GROQ_API_KEY=your_api_key_here
```

---

## Step 1: Transcription

1. Put all your evaluation audio files (`.mp3`, `.wav`, `.flac`) into the folder:

```
eval_audios/
```

2. Run:

```bash
python transcript.py
```

- **Input**: `eval_audios/`  
- **Output**: `transcript.txt`

---

##  Step 2: Truth Analysis

Run:

```bash
python truth_analysis.py
```

- **Input**: `transcript.txt`  
- **Output**: `submission.json`

---

##  Step 3: Cleaned Transcripts

Run:

```bash
python clean_transcript.py
```

- **Input**: `transcript.txt` (you can rename  `transcript.txt` if you want to clean them)  
- **Output**: `cleaned_transcript.txt`  

The cleaned transcripts keep only **lowercase letters, spaces, and full stops**.

---

### Workflow Summary

1. Put audios in `eval_audios/`
2. Run `transcript.py` → generates `transcript.txt`
3. Run `truth_analysis.py` → generates `submission.json`
4. Run `clean_transcript.py` → generates `cleaned_transcript.txt`

---

### Notes

- Ensure `.env` is present with your Groq API key before running any script.  
- If you want to change input/output filenames, edit them inside the respective `.py` scripts.  
- Cleaning step strips everything except alphabets, spaces, and full stops.  

---
