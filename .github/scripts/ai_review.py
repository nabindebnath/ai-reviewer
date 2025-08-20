import os
import openai
import subprocess

openai.api_key = os.getenv("OPENAI_API_KEY")

# Get the diff of the pull request
diff = subprocess.getoutput("git diff HEAD~1")

prompt = f"""
You are a senior software engineer reviewing a pull request.

Here is the code diff from multiple files:

{diff}

Please:
1. Group feedback by file name.
2. Flag potential bugs or logic issues.
3. Suggest improvements in readability, naming, and best practices.
4. Keep comments concise and actionable.
"""


response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

print("AI Review Comments:")
print(response["choices"][0]["message"]["content"])

