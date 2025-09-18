import os
from groq import Groq
from pathlib import Path
import logging
import json
import re
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TruthWeaver:
    def __init__(self, groq_api_key: str = None):
        self.groq_client = Groq(api_key=groq_api_key)

    def extract_truth(self, transcript_text: str, shadow_id: str) -> str:
        """Ask LLM to analyze and extract truth from combined sessions."""
        prompt = f"""You are the Truth Weaver, an AI detective.

        ANALYSIS TARGET: {shadow_id}

        INSTRUCTIONS:
        - Analyze all sessions (Session 1–5) carefully
        - Detect contradictions, exaggerations, and fabrications
        - Extract the most likely truth
        - List deception patterns with evidence

        TRANSCRIPT DATA:
        {transcript_text}

        Return ONLY valid JSON in this formal structure. Fill with actual extracted data from transcripts.

        FORMAL STRUCTURE (TEMPLATE):
        {{
        "shadow_id": "string",
        "revealed_truth": {{
            "programming_experience": "string",
            "programming_language": "string",
            "skill_mastery": "string",
            "leadership_claims": "string",
            "team_experience": "string",
            "skills and other keywords": ["string", "..."]
        }} ,
        "deception_patterns": [
            {{
            "lie_type": "string",
            "contradictory_claims": ["string", "..."]
            }},
            ...
        ]
        }}

        EXAMPLE:
        {{
        "shadow_id": "selene_6",
        "revealed_truth": {{
            "programming_experience": "limited",
            "programming_language": "Ruby",
            "skill_mastery": "beginner",
            "leadership_claims": "exaggerated",
            "team_experience": "individual contributor",
            "skills and other keywords": ["Ruby on Rails", "data", "AI", "machine learning", "big data"]
        }},
        "deception_patterns": [
            {{
            "lie_type": "experience_inflation",
            "contradictory_claims": ["I'm a seasoned Ruby on Rails developer, proficient across the modern data stack", "I'm comfortable deploying models using frameworks like TensorFlow or PyTorch", "I only took a weekend workshop on this stuff"]
            }},
            {{
            "lie_type": "skill_exaggeration",
            "contradictory_claims": ["I'm proficient across the modern data stack, AI, machine learning, and big data", "I typically work with a data scientist who handles that part", "I don't know any of it"]
            }},
            {{
            "lie_type": "leadership_exaggeration",
            "contradictory_claims": ["I'm ready to build your next predictive engine", "My role is more about the big picture and the Rails integration", "Just ask me about Rails, please"]
            }}
        ]
        }}
        """

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert AI detective. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return "{}"

    def process_transcript_file(self, transcript_file: str, output_file: str):
        """
        Process all sessions in a single transcript.txt file.
        Save results into a single JSON file.
        """
        try:
            with open(transcript_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Cannot read {transcript_file}: {e}")
            return {}

        # Split into individual sessions using regex (filename: content)
        session_matches = re.findall(r"(\S+\.mp3):\s*(.*?)(?=\n\S+\.mp3:|\Z)", content, re.DOTALL)
        if not session_matches:
            logger.error(f"No sessions found in {transcript_file}")
            return {}

        results = {}
        # Group every 5 sessions into one shadow_id
        for i in range(0, len(session_matches), 5):
            chunk = session_matches[i:i+5]
            if len(chunk) < 5:
                logger.warning(f"Skipping incomplete set: {[s[0] for s in chunk]}")
                continue

            shadow_id = chunk[0][0].split("_")[0] + f"_{i//5 + 1}"
            combined_text = ""
            for j, (filename, transcript) in enumerate(chunk, start=1):
                combined_text += f"Session {j}:\n{transcript.strip()}\n\n"

            truth_json = self.extract_truth(combined_text, shadow_id)
            

            truth_json = truth_json.strip()

            # Remove Markdown code fences if present
            truth_json = re.sub(r"^```json|^```|\s*```$", "", truth_json, flags=re.MULTILINE).strip()

            try:
                results[shadow_id] = json.loads(truth_json)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decoding failed for {shadow_id}: {e}")
                logger.error(f"Raw LLM output after cleanup: {truth_json}")
                results[shadow_id] = {"raw_output": truth_json}

        # Save all results in one JSON file
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            logger.info(f"Saved all analysis to {output_file}")
        except Exception as e:
            logger.error(f"Error saving {output_file}: {e}")

        return results


def main():
    transcript_file = "transcript.txt"  # the input file with all sessions
    output_file = "submission.json"      # single JSON output

    truth_weaver = TruthWeaver(groq_api_key=api_key)
    results = truth_weaver.process_transcript_file(transcript_file, output_file)



if __name__ == "__main__":
    main()
