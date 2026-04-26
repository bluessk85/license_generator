import os
import sys
from pathlib import Path


def _use_project_venv():
    """Re-run with the project .venv when the shell is using another venv."""
    venv_dir = Path(__file__).resolve().parent / ".venv"
    venv_python = venv_dir / "bin" / "python"
    if not venv_python.exists():
        return

    if Path(sys.prefix).resolve() != venv_dir.resolve():
        os.execv(str(venv_python), [str(venv_python), *sys.argv])


_use_project_venv()

import uvicorn

if __name__ == "__main__":
    uvicorn.run("license_api:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=True) 
