# Pythonanywhere-Free-Tier-CICD
Emulate a CICD pipeline using Pythonanywhere api for seamless deployments for FREE TIER

## Overview
This project demonstrates how to set up a Continuous Integration and Continuous Deployment (CICD) pipeline using the PythonAnywhere API. It is specifically designed for users on the free tier of PythonAnywhere, enabling seamless deployments without additional costs.

## Features
- **Automated Deployments**: Push your code changes to a repository and deploy them automatically to PythonAnywhere.
- **Free Tier Compatibility**: Works within the constraints of the PythonAnywhere free tier.
- **Simple Configuration**: Easy-to-follow setup process with minimal dependencies.
- **Customizable**: Adaptable to various project requirements.

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/DavidTimi1/Pythonanywhere-Free-Tier-CICD.git
    cd Pythonanywhere-Free-Tier-CICD
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Configure your PythonAnywhere API token:
    - Log in to your PythonAnywhere account.
    - Navigate to the "Account" page and generate an API token if you don't already have one.
    - Save the token in a `.env` file:
      ```
      PYTHONANYWHERE_API_TOKEN=your_pythonanywhere_api_token
      PYTHONANYWHERE_USERNAME=your_pythonanywhere_username
      ```

3. Trigger the deployment:
    ```bash
    python script.py
    ```

## How It Works
1. The script fetches your latest code from the repository.
2. It uses the PythonAnywhere API to sync the code to your web app directory.
3. The web app is reloaded on-premises to reflect the changes.

## Limitations
- The free tier has resource constraints, such as no SSH support, limited CPU time and storage.
- Only supports Python-based web apps.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [PythonAnywhere API Documentation](https://help.pythonanywhere.com/pages/API/)
- Open-source contributors who made this project possible.

#### Don't forget to star 🌟 the repo if you find it useful ❤
