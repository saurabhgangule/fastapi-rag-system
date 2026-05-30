import os
from dotenv import load_dotenv
from groq import Groq
import logging
import datetime

load_dotenv()

logger = logging.getLogger(__name__)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GroqService:

    def get_summary_prompt(self, user_name: str, articles_content: str) -> str:
        prompt = f"""
        Summarize the following news articles in 130 to 200 words.

        Keep in mind:
        - maintain key events
        - maintain important entities
        - factual accuracy
        - no opinions
        - no repetition
        - no hallucinations
        - no false information
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        Always start with a good morning greeting and end with a thank you message.
        for example:
        Good morning, [User's Name]! Here's today's news summary:
        [Summary]
        Thank you for listening! Have a great day!

        User's Name: {user_name}

        News Articles:
        {articles_content}
        """
        return prompt

    def summarize_text(self, user_name: str, articles_content: str) -> str:

        prompt = self.get_summary_prompt(user_name, articles_content)
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return None

        summary = response.choices[0].message.content
        logger.info(f"LLM Generated Summary: {summary}")
        return summary


    def convert_summary_to_mp3(self, summary: str) -> str | None:
    
        file_path = os.path.join(
            os.getenv("BROADCASTED_MP3_FILE_PATH"),
            f"{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.wav"
        )

        try:
            response = groq_client.audio.speech.create(
                model="canopylabs/orpheus-v1-english",
                voice="autumn",
                response_format="wav",
                input=summary
            )

            with open(file_path, "wb") as f:
                f.write(response.read())  # or response.content

            logger.info(f"Audio saved to: {file_path}")

            return file_path

        except Exception as e:
            logger.error(f"Error converting summary to audio: {e}")
            return None