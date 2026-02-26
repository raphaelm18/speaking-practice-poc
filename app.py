from dotenv import load_dotenv
load_dotenv()


import os
import streamlit as st



def analyze_speaking_sample(transcript_text: str, task_context: str) -> str:
    """
    Takes a student speaking transcript and returns a
    teacher-readable summary and rubric snapshot.
    
    Returns analysis in ≤12 lines total, using LLM with
    explicit guardrails against overclaiming.
    """
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
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
     Key elements are missing, leaving the listener unsure what the student fully means.
     Example patterns: naming a topic without explanation; stating an opinion without clarification.
   - Developing: Expresses the main idea clearly enough that the response feels complete,
     even if simple or brief. Covers the core of the task without obvious gaps.
     Example patterns: describing the main elements of a scene; stating an opinion with one reason.
   - Strong: Fully expresses the main idea with integrated details.
     The response feels finished and intentional, not cut off.
     Example patterns: describing elements and how they relate; supporting an opinion with multiple connected reasons.
   * Completeness is NOT about length. A short response can be complete.

2. Topic Coherence: Whether the student stays focused on the task prompt.

Definition of "on topic":
The student's statements relate directly to the task context and subject being described.
- Beginning: Includes clear off-topic content or shifts away from the task.
  Example patterns: unrelated personal stories; responding to a different subject or activity.
- Developing: Stays on topic but includes minor tangents or loosely related ideas
  that slightly distract from the main focus.
- Strong: Fully stays on topic throughout the response.
  All ideas relate directly to the task context or subject being described.
Rules:
- If the student is responding to the task and describing the subject shown in the task context,
  topic coherence should be Strong.
- Do NOT lower topic coherence due to brevity, simplicity, or limited detail.
- Do NOT use phrases like "could connect ideas more clearly" when the response stays on topic.

3. Elaboration: The extent to which the student adds meaningful detail beyond naming or listing.
   - Beginning: States ideas with little or no added detail.
     Example patterns: naming actions without explanation.
   - Developing: Adds at least one meaningful layer of detail, such as actions, feelings,
     reasons, or relationships.
     Example patterns: explaining why something is happening; adding how someone feels.
   - Strong: Adds multiple relevant details that deepen understanding.
     May include cause and effect, inference ("I think... because..."), comparison, or explanation of relationships.
   * Elaboration is about TYPES of details, not word count.

4. Vocabulary Use: How effectively word choice supports clarity and meaning.
   - Beginning: Very limited or repetitive word choice; relies on generic words.
     Example patterns: repeated use of words like "big," "thing," "stuff," "good."
   - Developing: Word choice is appropriate and understandable, with some variation.
     Example patterns: task-relevant words like "spraying," "chasing," "happy," "because."
   - Strong: Uses more specific or descriptive words that add clarity.
     Example patterns: precise verbs or descriptors that help the listener picture the idea.
   * Vocabulary is judged on usefulness and clarity, not academic level.

LEVELS (use these exact terms only):
- Beginning
- Developing
- Strong

NON-SCORED:
- Guidance needed: Specific area where teacher support would help (if any).

GUARDRAILS (CRITICAL):
- Every observation MUST cite specific words or phrases from the student's speech.
- Use conservative language. Avoid definitive claims.
- If the transcript is brief or ambiguous, explicitly acknowledge this limitation.
- When uncertain, prefer Beginning or Developing.
- Only analyze what is present in the transcript. Do not infer missing ideas.
- If evidence is limited, state that clearly.
- Use the task context only to interpret relevance and completeness. Do NOT grade factual accuracy against the picture description.

LANGUAGE RULES:
- Refer to the student as "the student". Do not refer to "the transcript".
- Do NOT use the words "presents", "suggesting", "suggests", or "indicates".
- Anchor each observation in what the student says.
  Include a short quoted phrase from the transcript for each dimension.

GUIDANCE NEEDED:
- Provide exactly ONE concrete teacher move (a specific prompt or sentence starter).
- Avoid generic advice.
- If no specific guidance is needed, explicitly state "None observed".

OUTPUT FORMAT (MUST be ≤12 lines total):
- Lines 1–2: Summary (exactly 2 sentences). Each sentence must reference what the student says.
- Lines 3–12: Compact rubric snapshot, one line per dimension:
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
            model="gpt-4o-mini",  # Cost-effective for POC
            messages=[
                {"role": "system", "content": "You are a careful, evidence-based ELL speaking analyst. You always cite specific transcript evidence and use conservative language."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent, conservative outputs
            max_tokens=300  # Limit to help enforce 12-line constraint
        )
        
        analysis = response.choices[0].message.content.strip()
        
        # Post-process to enforce constraints
        lines = analysis.split('\n')
        # Remove empty lines and keep only first 12 non-empty lines
        non_empty_lines = [line for line in lines if line.strip()]
        if len(non_empty_lines) > 12:
            analysis = '\n'.join(non_empty_lines[:12])
            analysis += "\n[Output truncated to 12 lines]"
        
        return analysis
        
    except Exception as e:
        return f"Error generating analysis: {str(e)}\n\nPlease check your OPENAI_API_KEY environment variable."



task_context = """
The student is describing a picture. The picture shows two elephants in a zoo enclosure.
One larger elephant is spraying water up with its trunk, and the water splashes down.
A smaller elephant is standing nearby and appears to be getting sprayed.
The ground looks wet, and the elephants may be cooling off.
The main focus is the elephants and the water.
""".strip()

sample_transcript = """
   I see two elephants at the zoo. One elephant is spraying water.
The other elephant is smaller and standing near it.
They look like they are having fun.
    """
if __name__ == "__main__":


    result = analyze_speaking_sample(sample_transcript)
    print(result)