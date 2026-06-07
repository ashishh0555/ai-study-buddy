import google.generativeai as genai
import time

from datetime import datetime

genai.configure(api_key="GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

history = []

total_words = 0
total_queries = 0

while True:

  print("Choose Response Style")
  print("1. Beginner friendly")
  print("2. Professional")

  style = input("Choose style: ")

  if style == "1":
    style_instruction = "Explain simply."

  elif style == "2":
    style_instruction = "Use professional terminology."

  else:
    style_instruction = ""

  print("What would you like to do?")

  print("1. Explain a Concept")
  print("2. Summarize Text")
  print("3. Generate Quiz Questions")
  print("4. Translate Text")
  print("5. View History")
  print("6. Exit")


  choice = input("Choose an option: ")

  if choice == "6":
    print("Goodbye!")
    break

  user_input = input("Enter your text: ")

  languages = {
    "1": "English",
    "2": "Hindi",
    "3": "Japanese",
    "4": "French",
    "5": "Kannada",
    "6": "Telugu"
  }

  print("\nChoose Output Language")

  for key, value in languages.items():
    print(f"{key}. {value}")

  language_choice = input("Choose language: ")

  language = languages.get(language_choice, "English")

  if user_input.strip() == "":
    print("Please enter some text!")
    continue

  if choice == "1":
    prompt = f"""Act as an expert educator. Explain the following concept to a beginner with no prior background in the field: {user_input}.
    Respond completely in {language}.
    keep it {style_instruction}


    Adhere to these constraints:
    1. Core Idea: Start with a one-sentence summary of what the concept is.
    2. Analogy: Use a relatable, real-world analogy to explain how it works.
    3. Breakdown: Explain 2-3 key components using plain language. Avoid jargon; if a technical term is necessary, define it immediately.
    4. Formatting: Use bullet points and bold text for scannability. Keep the total response under 200 words."""

  elif choice == "2":
    prompt = f"""You are an expert analyst. Provide a concise, highly scannable summary of the text provided below.
    Respond completely in {language}.
    keep it {style_instruction}
    Structure your response exactly as follows:
    - Executive Summary: A single, high-impact sentence capturing the main thesis or purpose of the text.
    - Key Takeaways: 3 to 5 bullet points highlighting the most critical facts, arguments, or data points.
    - Action Items / Conclusion: A final sentence stating the ultimate conclusion or next steps implied by the text (if applicable).

    Constraints:
    - Use plain, direct language. 
    - Do not introduce external information or assumptions.
    - Total length must not exceed 150 words.

    Text to summarize: {user_input}"""

  elif choice == "3":
    prompt = f"""
 You are a university professor in engineering. Generate exactly 5 challenging, application-based quiz questions on the topic of "{user_input}" specifically designed for upper-level engineering students.
Respond completely in {language}.
keep it {style_instruction}
For each question, provide the following fields in order:
1. Scenario/Problem Statement: Set up a realistic engineering context, design challenge, or system failure. Include relevant technical parameters or constraints where applicable.
2. Question: Ask a precise question requiring analytical thinking, calculation, or critical design trade-off evaluation.
3. Correct Answer: State the correct technical answer clearly and concisely.
4. Engineering Rationale: Provide a 2-3 sentence technical justification for why this answer is correct based on first principles, governing equations, or engineering standards. Explain why a common misconception would fail.

Constraints:
- Avoid basic definition questions (e.g., do not ask "What is X?"). 
- Focus on system behavior, optimization, constraint analysis, or failure modes.
- Maintain a formal, professional academic tone.
"""
    
  elif choice == "4":
      source_language = input("Enter the source language: ")
      target_language = input("Enter the target language: ")
      prompt = f"""
      You are a professional technical translator specializing in Engineering and Technology. Translate the text provided below from {source_language} to {target_language}.

Adhere to these strict requirements:
1. Technical Accuracy: Prioritize the correct technical terminology for the specific field (e.g., Mechatronics, Robotics, Electronics). Do not use literal translations for industry-standard terms.
2. Tone & Style: Maintain a [Formal/Professional/Casual] tone that matches the original intent of the author. 
3. Preservation: Keep all formatting, variables, code snippets, or mathematical formulas exactly as they appear in the source text.
4. Natural Flow: Ensure the output sounds like it was written by a native speaker in the target language, avoiding awkward phrasing common in direct translations.

Text to translate:"{user_input}" """
      
  elif choice == "5":

    if len(history) == 0:
        print("No history available.")

    else:
        print("\n=== History ===\n")

        for i, item in enumerate(history, start=1):

            print(f"\nQuery {i}")
            print(f"Time: {item['time']}")
            print(f"Feature: {item['feature']}")
            print(f"Input: {item['input']}")
            print(f"Response: {item['response'][:100]}...")
            print("-" * 40)

    continue


  else:
    print("Invalid choice")
    continue
  
  

  print("Thinking", end="")

  for _ in range(3):
    print(".", end="", flush=True)
    time.sleep(0.5)

  print()

  try:
    response = model.generate_content(prompt)
    print("\nResponse:\n")
    print(response.text)

  except Exception as e:
    print(f"Error: {e}")

  current_time = datetime.now()

  with open("history.txt", "a", encoding="utf-8") as file:
    file.write(f"\nFeature: {choice}\n")
    file.write(f"Input: {user_input}\n")
    file.write(f"Response: {response.text}\n")
    file.write(f"Time: {current_time}\n")
    file.write("-" * 50 + "\n")

  history.append({
    "time": current_time,
    "feature": choice,
    "input": user_input,
    "response": response.text
  })
  
  word_count = len(response.text.split())
  total_words += word_count

  print(f"\nWord Count: {word_count}")
  print(f"Total Words Generated: {total_words}")


  save = input("Save response? (y/n): ") 

  if save.lower() == "y":

    with open("response.md", "w", encoding="utf-8") as file:
     file.write(response.text)

    print("Saved!")

  total_queries += 1
  print(f"Total Queries: {total_queries}")
  print(f"History Size: {len(history)}")

  