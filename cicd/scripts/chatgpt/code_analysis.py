import openai
import os
import sys

exit_code = 0

def chatgpt_code_analysis(directory_path, filename, reports_path):
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
                        with open(f"{reports_path}/{file_name}_{filename}", 'w') as f:
                            global exit_code
                            exit_code = 1
                            f.write(suggestions)

if(len(sys.argv) == 3):
    openai.api_key = sys.argv[3]
    reports_path = sys.argv[2]
    directory_path = sys.argv[1]
else:
    print("usage <script_name> <code_path> <reports_path> <api_key>")



print("----------------Starting analyze script----------------------")
filename = "report.txt"
chatgpt_code_analysis(directory_path, filename, reports_path)
print("----------------------Analyzing done----------------------")
if exit_code == 1:
    print("Vulnerabilities found, see report")
sys.exit(exit_code)