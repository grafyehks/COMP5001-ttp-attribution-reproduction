# How we reproduced the analysis

Tested on a 2020 Intel MacBook Air (8 GB RAM) with VS Code.

1. Use Python 3.11-3.13. The locked numpy 2.1.3 has no installer for Python 3.14,
   so `poetry install` fails there. With Anaconda:
       conda create -y -n p3 python=3.12
       conda activate p3
2. Inside the `code/` folder:
       poetry env use python
       poetry install --no-root
3. Register the environment so the notebook can find it:
       poetry run python -m ipykernel install --user --name p3-venv --display-name "P3 (.venv)"
4. In VS Code: Select Kernel > Jupyter Kernel > "P3 (.venv)", then Run All.
   If an import fails with "CPU dispatcher tracer already initialized", restart the kernel.

Suggested fix for pyproject.toml (stops Poetry from picking an unsupported Python):
    python = ">=3.11,<3.14"
