from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Azure OpenAI credentials
AZURE_OPENAI_ENDPOINT = "https://c0933-m1tlmiv9-eastus.openai.azure.com"  # e.g., https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY = "7570e8dafab14081be41e3bc89e75a2c"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-35-turbo"  # e.g., gpt-35-turbo

# Simple healthcare keyword list for filtering queries
HEALTHCARE_KEYWORDS = ['symptoms', 'treatment', 'disease', 'medicine', 'diagnosis', 'health', 'doctor', 'patient']

# Function to check if a query is healthcare-related
def is_healthcare_query(prompt):
    prompt_lower = prompt.lower()
    for keyword in HEALTHCARE_KEYWORDS:
        if keyword in prompt_lower:
            return True
    return False

# Function to call Azure OpenAI API
def get_gpt_response(prompt):
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/completions?api-version=2023-03-15-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    data = {
        "prompt": f"You are a healthcare assistant. Only respond to healthcare-related queries.\n\n{prompt}",
        "max_tokens": 150,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# API route for healthcare GPT queries
@app.route('/api/healthcare-gpt', methods=['POST'])
def healthcare_gpt():
    try:
        # Get the prompt (query) from the request body
        data = request.json
        prompt = data.get("prompt")
        print(prompt)
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Check if the query is healthcare-related
        if not is_healthcare_query(prompt):
            return jsonify({"error": "This query is not healthcare-related. Please ask about healthcare topics."}), 400

        # Call Azure OpenAI API for healthcare queries
        gpt_response = get_gpt_response(prompt)
        return jsonify({"response": gpt_response['choices'][0]['text'].strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
