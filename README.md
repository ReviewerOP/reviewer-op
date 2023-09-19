Reviewer OP (Overpowered) ⚡️
===

Reviewer OP is an LLM-powered code review bot designed to automatically review Pull Requests (PRs).
It Harnesses the power of large language models for your code reviews and integrate them directly into your GitHub workflow.
Built on the robust FastAPI framework, it currently supports to be run as a GitHub App. 

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [Setup FastAPI server](#setup-fastapi-server)
  - [Expose your webhook using ngrok](#expose-your-webhook-using-ngrok)
- [Install GitHub App](#setting-up-github-app)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Features 🌟

- 🛡️ **Your Trusty Sidekick:** Think of reviewer-op as your coding buddy who’s got your back, ensuring that no code slips unchecked.
  
- 🚀 **Swift Reviews, Quicker Ships:** Prevent endless hours of code scrutiny. With reviewer-op, you'll flow through reviews and get to your launches faster.
  
- 🧠 **Wisdom of Tech Giants, Just for You:** It's like having a coffee chat about your code with a Principal Engineer from Google. Expert advice without the jitters!
  
- 🎨 **A Language God:** Whether you’re writing in Python or in JavaScript, reviewer-op is all ears (and eyes)!
  
- ❤️ **Celebrate the Wins, Learn from the Missteps:** It’s not just about pointing fingers. Reviewer-op gives high-five your coding wins and guide you gently through the oops moments.
  
- 💰 **Top-Tier Reviews, Wallet-Friendly:** GPT-4 powered code reviews without breaking the bank, starting at just $0.04 to $0.15 for a comprehensive 10-file review.

## Requirements
- Python 3.8+
- ngrok (to expose a webhook for Github App)
- Setup a Github App (It's Free)
- Get an OpenAI API Key from https://platform.openai.com/

## Getting Started

### Setup FastAPI server

1. **Clone the repository**
   ```
   git clone https://github.com/ReviewerOP/reviewer-op
   cd reviewer-op
   ```

2. **Set up a virtual environment (Optional but recommended)**
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages**
   ```
   pip install -r requirements.txt
   ```

4. **Create a .env file in the project root**
   ```python
   GITHUB_APP_ID= 12345 #Will be available after setting up GitHub App
   PEM_FILE_PATH= path/to/pem/file/of/github/app #Will be available after setting up GitHub App
   OPENAI_API_KEY= sk-*********** #Get this from OpenAI
   ```

4. **Run the FastAPI server**
   ```
   uvicorn main:app --reload
   ```

### Expose your webhook using ngrok

1. **Download and install ngrok**
   - Visit the [ngrok download page](https://ngrok.com/download) and follow the instructions to install.

2. **Expose your FastAPI server**
   ```
   ngrok http 8000
   ```

3. **Copy the HTTPS URL provided by ngrok** 
   - This URL will be used to set up the webhook for your GitHub app.

## Setting Up GitHub App

1. Go to GitHub Apps settings.
2. Create a new GitHub app. [Follow the Steps Given in Github's Guide](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app)
3. In the Webhook section, paste the HTTPS URL from ngrok and append the endpoint `/webhook` at the end of ngrok url
4. Setup GitHub App with these permissions-
   - Pull Request - *READ & WRITE*
   - Contents - *READ ONLY*
     
   <img width="727" alt="Screenshot 2023-09-19 at 9 06 56 PM" src="https://github.com/ReviewerOP/reviewer-op/assets/27367779/114886b6-7bfc-4c52-b3f2-2e0ee4e8d164">

   <img width="726" alt="Screenshot 2023-09-19 at 9 06 43 PM" src="https://github.com/ReviewerOP/reviewer-op/assets/27367779/88257c69-33c7-4f1f-83fc-fbf3ed7d8912">
5. `Subscribe to events` to be checked for *Pull request*
   
    <img width="391" alt="Screenshot 2023-09-19 at 9 10 41 PM" src="https://github.com/ReviewerOP/reviewer-op/assets/27367779/c1662bc2-ac3d-4538-bc74-a623da29038c">
6. Generate a Private Key from the GitHub App `General` section and save it locally (the path has to be put in `.env` file in python)
   
   <img width="758" alt="Screenshot 2023-09-19 at 9 15 07 PM" src="https://github.com/ReviewerOP/reviewer-op/assets/27367779/738f6dfe-6b3a-42e1-8158-8add5e1a0ed6">
7. Save the `App Id` given in `General` section of the newly created GitHub app. This will also be put in `.env` file in python



## Usage

1. If the Reviewer-OP App Created on your GitHub account has the permission to the target Repository
2. On Creating a New Pull Request or push a new commit to an Existing Pull Request (PR)
3. The Reviewer-OP bot will succesfully post comments on the Pull Request (PR)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License

DiceDB is open-sourced under [Apache License, Version 2.0](LICENSE.md).
