# Coqui TTS Voice Cloner

This project provides a voice cloning Python application that compiles to an executable. It is designed to be generic, allowing for different "agents" (voices) to be used for text-to-speech generation.

## Configuration

The project uses a `config.json` file to define the executable name and potentially other settings.

```json
{
  "executable_name": "agent-server.exe"
}
```

## Usage

1.  **Agents**: Place your reference audio files (mp3) in the `agents` folder. The filename (without extension) will be the agent's name.
2.  **Running**: Run the generated executable or the `voice_server.py` script, server runs at localhost:5005
3.  **API**: The server exposes a `/speak` endpoint.
    - **Method**: POST
    - **Body**:
      ```json
      {
        "agent": "agent_name",
        "text": "Text to speak",
        "language": "en"
      }
      ```

## Performance Notes

- **CPU Only**: This version of the project is optimized for CPU usage.
- **Size**: The executable size is kept reasonable by excluding heavy GPU dependencies.
- **GPU Support**: A separate branch exists that supports CPU/CUDA GPU, but the resulting executable size is significantly larger.

## Setup

1.  **Create Virtual Environment**: Create a Python 3.11 virtual environment named `env311`:

    ```bat
    python -m venv env311
    ```

2.  **Activate Environment**:

    ```bat
    env311\Scripts\activate.bat
    ```

3.  **Install Dependencies**:
    ```bat
    pip install -r requirements.txt
    ```

## Building

To build the executable, activate your virtual environment and run:

```bat
python -O -m PyInstaller voice_server.spec
```

This command uses PyInstaller with the `voice_server.spec` file, which reads configuration from `config.json`.
