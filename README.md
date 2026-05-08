# MCC VR + AI System

## Project Overview

**MCC VR + AI System** is a Unity-based virtual reality representation of NASA's Mission Control Center (MCC) integrated with an intelligent virtual agent powered by a Retrieval-Augmented Generation (RAG) pipeline. The system is designed to support astronaut and flight controller decision-making by combining immersive mission-operations visualization with context-aware voice interaction.

The repository contains the Unity application, project assets, scripts for speech and agent interaction, packaged builds, backend RAG server scripts, project knowledge PDFs, and supporting technical documentation.

## Background And Motivation

NASA mission operations depend on tightly coordinated teams managing spacecraft state, crew safety, timelines, anomalies, and communication across multiple disciplines. Within MCC, flight controllers monitor subsystem health, interpret telemetry, execute procedures, and advise the flight director under time-critical conditions.

This operating model creates several persistent challenges:

- High cognitive load caused by simultaneous monitoring, procedure recall, and anomaly response.
- Information fragmentation across flight rules, procedures, mission logs, subsystem references, and voice loops.
- Training overhead for new operators learning MCC roles, console workflows, and mission context.
- Communication constraints in deep space operations, where lunar and Mars missions introduce significant latency and reduced opportunities for real-time ground intervention.
- Growing need for onboard autonomy as crews operate farther from Earth with less immediate support.

The project explores how immersive simulation and AI-assisted retrieval can reduce operator burden, improve situational understanding, and provide a platform for future human-autonomy teaming in NASA operations.

## Problem Statement

Traditional mission support tools are effective for expert operators but often assume high familiarity with procedures, rapid context switching, and immediate access to distributed documentation. For future exploration missions, those assumptions become increasingly fragile.

The problem addressed by this project is:

> How can a virtual Mission Control environment, coupled with a context-aware AI assistant, improve mission understanding, reduce operator cognitive load, and provide timely procedural support for astronauts and flight controllers in both current and future NASA operations?

## System Description

### VR Environment

The frontend is a Unity application that recreates a NASA-inspired Mission Control environment for desktop and XR interaction. The environment is intended to support:

- Spatial understanding of MCC layout and console organization.
- Immersive familiarization for operators, trainees, and stakeholders.
- Voice-enabled interaction within a mission operations setting.

The repository includes both desktop and XR scenes under `NASA JSC/Assets/Scenes/NASA Scenes`.

### AI Agent

The AI assistant is designed to answer mission-relevant questions using a grounded response workflow:

1. Capture user speech.
2. Transcribe the utterance with Whisper-based speech-to-text.
3. Query a RAG endpoint for relevant contextual material.
4. Pass the question, retrieved context, and mission-specific prompt to an answer endpoint.
5. Convert the response to speech through a text-to-speech service.

The Unity client prompt structure emphasizes concise responses, NASA flight operations principles, and operational priorities such as crew safety, vehicle safety, and mission success.

### Interaction System

Interaction is voice-first. The current Unity implementation includes:

- Microphone capture with speech segmentation.
- Server-side transcription requests.
- RAG context retrieval before answer generation.
- Event-driven response playback through TTS.
- Desktop and XR scene support for immersive operation.

## System Architecture

The deployed system architecture is organized as follows:

```text
[User in Unity VR/Desktop]
          |
          v
[Unity Frontend]
  - VR/XR environment
  - Voice capture
  - Interaction logic
          |
          v
[FastAPI Backend on AWS]
  - /transcribe
  - /ask
  - /answer
  - /speak
          |
          +--> [Whisper STT]
          +--> [Vector Database / Embedding Retrieval]
          +--> [LLM Response Generation]
          +--> [TTS Service]
```

### Frontend

- **Unity 2022.3.14f1** application for desktop and XR deployment.
- Mission Control scene composition, UI, audio handling, and interaction logic.
- C# scripts for Whisper integration, RAG requests, AI orchestration, and speech playback.

### Backend

- **FastAPI** service architecture for orchestration of transcription, retrieval, generation, and speech synthesis.
- Hosted on **AWS EC2**, with the Unity scenes currently referencing remote HTTP endpoints.
- Backend files are located in `Backend Scripts/`.
- Supports modular AI services so retrieval and generation can evolve independently.

### Retrieval Layer

- An OpenAI **vector store** stores embedded mission documents, procedures, and reference material.
- Source PDFs for the current RAG corpus are located in `Backend Scripts/knowledge/`.
- Retrieval returns context relevant to the user's question before response generation.
- This reduces hallucination risk and grounds responses in operational content.

### Speech Services

- **Whisper STT** transcribes spoken user input.
- **TTS** converts generated responses into audio for immersive conversational interaction.

## Technical Stack

### Core Platforms

- Unity `2022.3.14f1`
- C#
- FastAPI
- AWS hosting

### AI And Speech

- Retrieval-Augmented Generation (RAG)
- Vector database for semantic retrieval
- Whisper speech-to-text
- Text-to-speech pipeline

### Unity Packages Observed In This Repository

- Meta XR SDK
- OpenAI Unity integration
- ElevenLabs Unity package
- Unity XR / Oculus support
- TextMeshPro
- Universal Render Pipeline

## Methodology

The system was developed using a human-centered engineering approach grounded in mission operations use cases.

### Subject Matter Expert Engagement

- Interviews and feedback sessions with SMEs informed the mission operations framing.
- MCC roles, operator workflows, and information demands guided the interaction model.
- The assistant behavior was scoped toward procedural support, rapid orientation, and contextual explanation rather than unrestricted conversation.

### Human-Centered Design

- The VR environment was designed to support intuitive orientation and recognizable mission-control interaction patterns.
- Voice interaction was prioritized to reduce manual interface burden in immersive settings.
- The RAG architecture was selected to improve trustworthiness by grounding outputs in retrieved reference data.

## Results And Evaluation

This project demonstrates a functional proof-of-concept for combining immersive mission operations simulation with AI-assisted support.

Observed outcomes include:

- A working Unity VR/Desktop experience representing a NASA-inspired MCC environment.
- End-to-end voice workflow from speech capture through transcription, retrieval, response generation, and spoken output.
- A system architecture aligned with future decision-support use cases for astronaut and flight controller assistance.
- A platform suitable for further usability testing, retrieval benchmarking, and operational scenario evaluation.

At the current repository stage, formal quantitative evaluation data is not packaged alongside the codebase. Future assessments should measure latency, retrieval precision, task completion support, user trust, and cognitive workload reduction.

## Applications To NASA Missions

### Artemis And Cis-Lunar Operations

- Support pre-mission and on-console training in mission operations environments.
- Provide fast access to procedures, system explanations, and mission context.
- Improve familiarization with distributed mission-support workflows.

### Lunar Surface Missions

- Assist crews operating with limited ground bandwidth and delayed support.
- Provide context-aware procedural guidance for habitat, EVA, and surface systems.
- Support just-in-time information retrieval in immersive training or rehearsal settings.

### Mars Autonomy

- Extend the concept toward onboard decision support where communication delay makes real-time MCC assistance impractical.
- Enable more autonomous crew operations supported by grounded AI retrieval.
- Serve as a prototype for future human-autonomy teaming concepts in deep space exploration.

## Future Work

- Integrate the companion FastAPI backend directly into this repository or as a linked submodule.
- Replace hard-coded service URLs with environment-based runtime configuration.
- Add authenticated service access and secure secret management.
- Expand the retrieval corpus with flight rules, procedures, anomaly playbooks, and mission timelines.
- Evaluate model behavior under off-nominal mission scenarios.
- Add telemetry dashboards, console-specific AI modes, and multi-user collaborative operation.
- Perform formal human factors studies focused on workload, trust, and mission effectiveness.

## Getting Started

### Prerequisites

- Git
- Unity Hub
- Unity Editor `2022.3.14f1`
- A running companion AI backend for STT, RAG, answer generation, and TTS
- Python `3.10+` for the backend service, if you are running your own FastAPI deployment
- An AWS account with EC2, IAM, and Systems Manager Parameter Store access
- An OpenAI API key
- An ElevenLabs API key and voice ID, if using the `/speak` endpoint

### 1. Clone The Repository

```bash
git clone https://github.com/ChawinMin/CGT411-IXL-APL.git
cd CGT411-IXL-APL
```

### 2. Review The AWS RAG Documentation

The full cloud setup is documented in:

- `Technical Documentation/RAG AWS Documentation.pdf`

Use that PDF if you need more detail on creating the AWS instance, connecting with SSH, storing the OpenAI key securely, creating the vector store, uploading PDFs, and running the backend continuously with `systemd`.

### 3. Start An AWS EC2 Server

Create an Ubuntu EC2 instance for the FastAPI backend.

Recommended settings from the project documentation:

- AMI: Ubuntu
- Instance type: `t3.micro`
- SSH key pair: required for server access
- Security group inbound rules:
  - TCP `22` for SSH
  - TCP `8000` for the FastAPI server used by Unity

Connect to the server with SSH.

Windows PowerShell example:

```powershell
ssh -i C:\Users\YourUsername\Downloads\IXL-Key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

macOS/Linux example:

```bash
chmod 400 ~/Downloads/IXL-Key.pem
ssh -i ~/Downloads/IXL-Key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 4. Configure AWS Parameter Store

The backend retrieves the OpenAI key from AWS Systems Manager Parameter Store instead of hard-coding it in `server.py`.

In AWS Systems Manager Parameter Store, create:

- Name: `/openai/api_key`
- Type: `SecureString`
- Data type: `text`
- Value: your OpenAI API key

Create an IAM role for EC2 with `AmazonSSMReadOnlyAccess`, then attach that role to the EC2 instance. The included backend code reads this parameter from region `us-east-2`.

You can verify access from the EC2 server with:

```bash
python3 test_key.py
```

### 5. Upload Backend Scripts And Knowledge Files To EC2

The backend implementation is in:

- `Backend Scripts/server.py`
- `Backend Scripts/create_vector_store.py`
- `Backend Scripts/upload_pdfs.py`
- `Backend Scripts/test_key.py`
- `Backend Scripts/requirements.txt`
- `Backend Scripts/knowledge/`

Create the remote project directory, then upload the contents of `Backend Scripts` to the EC2 server.

Windows PowerShell example from the repository root:

```powershell
ssh -i C:\Users\YourUsername\Downloads\IXL-Key.pem ubuntu@YOUR_EC2_PUBLIC_IP "mkdir -p ~/rag-server"
scp -i C:\Users\YourUsername\Downloads\IXL-Key.pem -r ".\Backend Scripts\*" ubuntu@YOUR_EC2_PUBLIC_IP:/home/ubuntu/rag-server/
```

macOS/Linux example from the repository root:

```bash
ssh -i ~/Downloads/IXL-Key.pem ubuntu@YOUR_EC2_PUBLIC_IP "mkdir -p ~/rag-server"
scp -i ~/Downloads/IXL-Key.pem -r "Backend Scripts/"* ubuntu@YOUR_EC2_PUBLIC_IP:/home/ubuntu/rag-server/
```

After connecting to the server, confirm the scripts and RAG PDFs are present:

```bash
cd ~/rag-server
ls
ls knowledge
```

The `knowledge` folder contains the source PDFs used by the RAG system, including role and MCC procedure documents.

### 6. Install Backend Dependencies

On the EC2 server:

```bash
sudo apt update
sudo apt install python3-pip -y
cd ~/rag-server
pip3 install -r requirements.txt
```

If the full requirements file is too broad for the EC2 environment, install the core server dependencies directly:

```bash
pip3 install fastapi uvicorn openai boto3 pydantic python-multipart elevenlabs
```

### 7. Create And Populate The Vector Store

The helper scripts `create_vector_store.py` and `upload_pdfs.py` use the OpenAI SDK's default authentication. Before running them, make sure the server shell has access to an OpenAI key:

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

Alternatively, update those scripts to retrieve `/openai/api_key` from AWS Parameter Store the same way `server.py` does.

Create a vector store:

```bash
python3 create_vector_store.py
```

Copy the printed vector store ID into:

- `VECTOR_STORE_ID` in `server.py`
- `VECTOR_STORE_ID` in `upload_pdfs.py`

Then upload the PDFs from `knowledge/` into the vector store:

```bash
python3 upload_pdfs.py
```

If you add more RAG source material later, place the PDFs in `Backend Scripts/knowledge/`, upload the updated folder to the EC2 server, and rerun `upload_pdfs.py`.

### 8. Configure Speech Keys

The current `server.py` also loads `auth.json` for the `/answer`, `/transcribe`, and `/speak` routes.

Make sure `auth.json` exists on the server with the expected keys:

```json
{
  "api_key": "your_openai_api_key",
  "ELEVEN_LABS_API_KEY": "your_elevenlabs_api_key"
}
```

Also replace the placeholder values in `server.py`:

- `REPLACE WITH YOUR STORE VECTOR ID`
- `REPLACE WITH ELEVENS LABS VOICE ID`

Do not commit real API keys to the repository.

### 9. Run The Backend

Example FastAPI startup command:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Expected API routes used by the Unity client:

- `POST /transcribe`
- `POST /ask`
- `POST /answer`
- `POST /speak`

Test the server in a browser:

```text
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

### 10. Run The Backend Continuously

For a persistent AWS deployment, create a `systemd` service on the EC2 server:

```bash
sudo nano /etc/systemd/system/rag-api.service
```

Service file:

```ini
[Unit]
Description=RAG FastAPI Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/rag-server
ExecStart=/usr/bin/python3 -m uvicorn server:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start rag-api
sudo systemctl enable rag-api
sudo systemctl status rag-api
```

### 11. Open The Unity Project

1. Open Unity Hub.
2. Add the project located at `NASA JSC/`.
3. Open the project with Unity `2022.3.14f1`.
4. Load one of the main scenes:
   - `NASA JSC/Assets/Scenes/NASA Scenes/Desktop - NASA JSC.unity`
   - `NASA JSC/Assets/Scenes/NASA Scenes/XR - NASA JSC.unity`
5. Confirm the backend endpoints are reachable before entering Play Mode.
6. If your EC2 public IP changed, update the Unity endpoint references to the current `http://YOUR_EC2_PUBLIC_IP:8000` backend URL.

## Folder Structure

```text
CGT411-IXL-APL/
|-- README.md
|-- .github/
|-- Addiitonal Information/
|   |-- APLPoster.pdf
|-- Backend Scripts/
|   |-- knowledge/
|   |   |-- Astronaut.pdf
|   |   |-- Engineer.pdf
|   |   |-- Flight Controller.pdf
|   |   |-- Flight Director.pdf
|   |   `-- MCC Procedures.pdf
|   |-- create_vector_store.py
|   |-- ingest.py
|   |-- requirements.txt
|   |-- server.py
|   |-- test_key.py
|   `-- upload_pdfs.py
|-- Build App (Desktop)/
|-- Build App (XR)/
|-- Build App (XR Android)/
|-- Technical Documentation/
|   `-- RAG AWS Documentation.pdf
`-- NASA JSC/
    |-- Assets/
    |   |-- Scenes/
    |   |-- Scripts/
    |   |   `-- AI/
    |   |       |-- AIManager.cs
    |   |       |-- RAG.cs
    |   |       |-- Whisper.cs
    |   |       `-- ElevenLabsManager.cs
    |   `-- ...
    |-- Packages/
    `-- ProjectSettings/
```

## Repository Notes

- The Unity client is the primary implementation contained in this repository.
- Packaged desktop, XR, and Android XR builds are included for demonstration and review.
- The AI backend scripts are included in `Backend Scripts/`, but deployment-specific values such as API keys, vector store IDs, EC2 IP addresses, and ElevenLabs voice IDs must be configured by each deployer.
- The RAG source documents are stored in `Backend Scripts/knowledge/`; update that folder and rerun the upload script when changing the knowledge base.
- For deeper AWS setup instructions, follow `Technical Documentation/RAG AWS Documentation.pdf`.

## Additional Resources

For additional resources, please refer to these GitHub repositories and NASA sources that helped us with the project.

- [Unity & OpenAI][repo1]
- [ElevenLabs][repo2]
- [MCC Tour][tour]
- [NASA Patches][patches]

[repo1]: https://github.com/srcnalt/OpenAI-Unity?tab=readme-ov-file
[repo2]: https://github.com/RageAgainstThePixel/com.rest.elevenlabs?tab=readme-ov-file#text-to-speech
[tour]: https://www.nasa.gov/johnson/virtual-tours/mission-control-center/
[patches]: https://www.nasa.gov/gallery/human-spaceflight-mission-patches/

## Team

<p align="center"><img src="Misc/TeamPhoto.jpeg" width="670"></p>

The top row from left to right is: **Ryan Ahn**, **Avery Delinger III**, **Chawin Mingsuwan**

The bottom row from left to right is: **Simon An**, **Russell Thomas**, **William Cromer**,**Salvador Ayala**