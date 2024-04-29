# Whatcom Coders Website Backend

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.x or newer //todo
- pip (Python package installer)
- gcloud sdk

### Installing Google Cloud CLI

Before you start, you need to install the Google Cloud CLI (gcloud CLI), which is essential for managing resources on Google Cloud Platform (GCP).

#### Quick Installation Guide

1. **Download and Install:**

   - Visit the [Google Cloud SDK page](https://cloud.google.com/sdk/docs/install) for download links and installation instructions specific to your operating system (Windows, macOS, or Linux).

2. **Initialize the SDK:**
   - After installation, open a terminal or command prompt and run `gcloud init` to authenticate and set up your default project configuration.

For detailed installation steps and troubleshooting, refer to the [official Google Cloud SDK documentation](https://cloud.google.com/sdk/docs/).

#### Verifying Installation

Check the installation by running `gcloud version` in your command prompt or terminal. This command should display the installed version of the gcloud CLI.

### 🔧 Installing

To set up your local development environment, please follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/WhatcomCodersDev/whatcomcoders_alumnidirectory
   cd backend
   ```
2. Create python virtual environment called `env` and install the required packages:

   Windows:

   ```powershell
   python -m venv env
   pip  install -r  .\requirements.txt

   ```

3. Environment variables - Please contact the developers to access environment variables. That is 4 files

- .env
- .env.staging
- .env.development
- .env.prod

4. To run locally:

   Windows:

   ```powershell
   python .\app.py
   ```

# ☁️ Deployment

[April 28th] For now, please contact Whatcom Coders Devs for service account keys, we are in the process of migrating to gcloud secrets. If you have access to the project, you will need to download two service accounts keys and put them in the root directory with the respective names

1. client_secrets.json - ((Keys Creation)[https://console.cloud.google.com/apis/credentials/oauthclient/525864173897-6ssad1t2va8dcc568je7vpt83s8tnns3.apps.googleusercontent.com?hl=en&project=gothic-sled-375305]) This is the used for google sign-in authentication

2. gcloud_secrets.json - ((Keys Creation)[https://console.cloud.google.com/iam-admin/serviceaccounts/details/100907456739208038106?hl=en&project=gothic-sled-375305]) This is the API keys for the service account that interacts with Google APIs

### Deploy to Prod

GCP Project: (gothic-sled-375305)[https://console.cloud.google.com/appengine/versions?serviceId=default&versionId=20240206t212035&hl=en&project=gothic-sled-375305]

1. Run `npm run build`
2. Run `firebase deploy`

### Deploy to Staging

GCP Project: (whatcomcoders-prod)[https://console.cloud.google.com/appengine/versions?serviceId=default&versionId=20240206t212035&hl=en&project=whatcomcoders-prod] (yes I know thats confusing, we can't change it now...)

1. Run `gcloud app deploy`
