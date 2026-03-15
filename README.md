# Bertie Project

An interactive puppet system for creating and manipulating digital characters.

## Overview

This project contains:
- Interactive HTML canvas for puppet manipulation
- Python scripts for processing puppet parts and joints
- Asset management system for puppet components

## Files

- `canvas.html` - Main interactive interface
- `create_joint_system.py` - Script for creating joint definitions
- `process_bertie_parts.py` - Processes puppet parts
- `process_bertie_precise.py` - Precise processing of puppet components
- `Bertie Assets/` - Contains joint definitions, bone mappings, and assembly instructions

## Getting Started

1. Open `canvas.html` in a web browser to use the interactive interface
2. Run Python scripts to process or modify puppet components
3. Check `Bertie Assets/` for configuration files

## Local Setup (Recommended)

1. Create a virtual environment: `python3 -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the dev server: `python3 server.py`
5. Open: `http://127.0.0.1:8000/canvas.html`

Notes:
- The server disables caching for fast iteration.
- You can change the port with `python3 server.py --port 5173`.
- One-command start: `./dev` (creates venv, installs deps, runs server, auto-opens the browser).

## CodeRabbit Integration

This project uses CodeRabbit for AI-powered code reviews. CodeRabbit will automatically review pull requests and provide feedback on code quality, style, and potential improvements.

### Setting up CodeRabbit

1. Install the CodeRabbit GitHub App: https://coderabbit.ai
2. Add your `CODERABBIT_API_KEY` as a repository secret in GitHub Settings
3. Create pull requests to trigger AI code reviews

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request for CodeRabbit review

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Bradley Geiser

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
