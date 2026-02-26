from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from openai import OpenAI


def analyze_speaking_sample(transcript_text: str, task_context: str) -> str:
    """
    Takes a student speaking transcript and returns a
    teacher-readable summary and rubric snapshot.

    Returns analysis in <=12 lines total, using LLM with
    explicit guardrails against overclaiming.
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    # Clean transcript
    transcript_clean = transcript_text.strip()

    # Construct prompt with rubric definitions and guardrails
    prompt = f"""You are analyzing an ELL student's speaking transcript for a teacher.

TASK CONTEXT (what the student was asked to respond to):

{task_context}

RUBRIC DIMENSIONS (scored):

1. Idea Completeness: Whether the student has fully expressed a whole response to the task.
   - Beginning: Mentions an idea related to the task, but the response feels partial or unfinished.
   - Developing: Expresses the main idea clearly enough that the response feels complete.
   - Strong: Fully expresses the main idea with integrated details.

2. Topic Coherence: Whether the student stays focused on the task prompt.
   - Beginning: Includes clear off-topic content or shifts away from the task.
   - Developing: Stays on topic but includes minor tangents.
   - Strong: Fully stays on topic throughout the response.

3. Elaboration: The extent to which the student adds meaningful detail beyond naming or listing.
   - Beginning: States ideas with little or no added detail.
   - Developing: Adds at least one meaningful layer of detail.
   - Strong: Adds multiple relevant details that deepen understanding.

4. Vocabulary Use: How effectively word choice supports clarity and meaning.
   - Beginning: Very limited or repetitive word choice.
   - Developing: Word choice is appropriate and understandable, with some variation.
   - Strong: Uses more specific or descriptive words that add clarity.

LEVELS (use these exact terms only): Beginning, Developing, Strong

GUARDRAILS:
- Every observation MUST cite specific words or phrases from the student's speech.
- Use conservative language. Avoid definitive claims.
- Only analyze what is present in the transcript.

OUTPUT FORMAT (MUST be <=12 lines total):
- Lines 1-2: Summary (exactly 2 sentences referencing what the student says).
- Lines 3-7: Compact rubric snapshot:
  * Idea completeness: [Level] — [brief evidence]
  * Topic coherence: [Level] — [brief evidence]
  * Elaboration: [Level] — [brief evidence]
  * Vocabulary use: [Level] — [brief evidence]
  * Guidance needed: [specific area or "None observed"]

TRANSCRIPT TO ANALYZE:
{transcript_clean}

Begin your analysis:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a careful, evidence-based ELL speaking analyst. You always cite specific transcript evidence and use conservative language."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )

        analysis = response.choices[0].message.content.strip()

        # Enforce 12-line max
        lines = analysis.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        if len(non_empty_lines) > 12:
            analysis = '\n'.join(non_empty_lines[:12])
            analysis += "\n[Output truncated to 12 lines]"

        return analysis

    except Exception as e:
        return f"Error generating analysis: {str(e)}\n\nPlease check your OPENAI_API_KEY."


if __name__ == "__main__":
    task_context = "The student is describing a picture of two elephants near water. One is spraying water with its trunk."
    sample_transcript = "I see two elephants at the zoo. One elephant is spraying water. The other elephant is smaller."
    result = analyze_speaking_sample(sample_transcript, task_context)
    print(result)