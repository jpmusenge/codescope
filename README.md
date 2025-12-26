# CodeScope
> Side Project...

This is a project I started working on while learning about AI agents and agentic workflows. It started while reading Andrew Ng's article in The Batch newsletter about building simple agents using aisuite. CodeScope is an AI agent that analyzes codebases for
dead-code and technical debt, and generates actionable reports.

I delved deeper into the "simple recipe" and approach shared in the newsletter and wanted to build something that solved a problem I was facing and is safe to use. CodeScope is **read-only by design**. It:
- Only reads files, never modifies them
- Uses MCP filesystem tools with controlled access
- Generates reports outside your codebase
- Requires human review before any changes

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## How It Works

1. CodeScope uses MCP filesystem tools to safely read your codebase
2. An LLM analyzes the code for technical debt patterns
3. Findings are rated by confidence level
4. A formatted report is generated

## Features

- **Multi-model support** - Works with Claude, GPT-4, and Gemini
- **Confidence-rated findings** - Issues ranked by how likely they are to be real debt
- **Read-only by design** - Analyzes but never modifies your code
- **Beautiful reports** - HTML and Markdown output

## Get Started
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/codescope.git
cd codescope

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your API key(s) to .env
cp .env.example .env
# Edit .env with your keys

# Run analysis
python main.py ./path/to/your/project
```

## Usage
```bash
# Basic usage
python main.py ./my-project

# Use a specific model
python main.py ./my-project --model gpt4-mini

# Focus on specific issues
python main.py ./my-project --focus "unused imports" "TODO comments"

# List available models
python main.py --list-models
```

## Sample Report

CodeScope generates detailed Markdown and HTML reports.

**[View Full Sample Report](reports/codebase_20251225_233848.md)**

<details>
<summary>Quick preview</summary>

### Sample findings from analyzing the demo codebase:

**High Confidence Issues**
- `main.py:3-4` - Unused imports: `json`, `datetime`
- `utils.py:2` - Unused import: `re`

**Medium Confidence Issues**  
- `utils.py:12` - Function `unused_function()` has no callers
- `orphan.py` - File not imported anywhere

**Low Confidence Issues**
- `main.py:7` - TODO comment: "add proper argument parsing"

</details>

## Resources

- [aisuite Repository](https://github.com/andrewyng/aisuite)
- [The Batch Newsletter](https://www.deeplearning.ai/the-batch/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
