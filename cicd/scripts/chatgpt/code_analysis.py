import openai
import os
import sys

openai.api_key = "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"
exit_code = 0

def chatgpt_code_analysis(directory_path, filename):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            print(file_name)
            if file_name.endswith('.java') or file_name.endswith('.yml'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    code = file.read()
                    prompt = f"Are there any vulnerabilities or code smells in the following code:\n\n{code}\n\n. if yes, respond with yes, followed by the description."
                    response = openai.Completion.create(
                        engine="text-davinci-002",
                        prompt=prompt,
                        max_tokens=100,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    )
                    suggestions = response.choices[0].text.strip()
                    if suggestions.startswith("Yes") or suggestions.startswith("yes"):
                        with open(f"./reports/{file_name}_{filename}", 'w') as f:
                            global exit_code
                            exit_code = 1
                            f.write(suggestions)

print("----------------Starting analyze script----------------------")
directory_path = "../../../src/main"
filename = "report.txt"
chatgpt_code_analysis(directory_path, filename)
print("----------------------Analyzing done----------------------")
if exit_code == 1:
    print("Vulnerabilities found, see report")
sys.exit(exit_code)