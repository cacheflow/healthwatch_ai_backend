from openai import OpenAI
from django.conf import settings

class MedicalDescriptionRefiner:
  def __init__(self):
      self.context = """"You are an advanced medical assistant tasked with converting inmate health concerns into concise, clinically relevant summaries for medical staff. Translate informal or layman descriptions into medical language that provides essential details for clinical assessment. Guidelines:
      - Assume descriptions are complete; do not ask for more information.
      - Use clear clinical terminology without excessive jargon.
      - Only provided the responses with no extra text. Example: Input: "I've been feeling really dizzy for the past few days, like the room is spinning."
        Output: "Patient reports persistent dizziness for several days, potentially indicative of vertigo. Recommended follow-up includes monitoring of blood pressure and hydration levels."""""
      
  def refine(self, text, education_level=1):
    client = OpenAI(
      api_key=settings.OPEN_API_KEY
    )
    education_mapping = {
      0: "Elementary",  
      1: "Middle School",
      2: "High School",
      3: "Some College",
      4: "College",
      5: "Advanced"
    }
    response = client.chat.completions.create(model='gpt-4o', messages=[{
      "role": "system",
      "content": self.context,
      },
      {
        "role": "user",
        "content": f"{text} Patient education level: ({education_mapping[education_level]})"
      }
    ])
    return response.choices[0].message.content