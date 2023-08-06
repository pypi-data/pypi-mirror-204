import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence

from .external_resources import ExternalResources


def make_pdf_in_tempdir(
    tex_file_content: str,
    external_resource_sequence: Sequence[ExternalResources],
    silent: bool = True,
) -> bytes:
    with tempfile.TemporaryDirectory() as work_dir:
        for ext_res in external_resource_sequence:
            ext_res.clone_into_directory(Path(work_dir))

        tex_file_path = tempfile.mkstemp(dir=work_dir, suffix=".tex")[1]
        pdf_file_path = os.path.splitext(tex_file_path)[0] + ".pdf"

        with open(tex_file_path, "w") as tex_file_fd:
            tex_file_fd.write(tex_file_content)

        run_xelatex(tex_file_path=tex_file_path, silent=silent)

        with open(pdf_file_path, "rb") as pdf_file:
            return pdf_file.read()


def run_xelatex(tex_file_path: str, rerun: bool = True, silent: bool = True) -> None:
    xelatex = shutil.which("xelatex")
    if not xelatex:
        raise RuntimeError("xelatex is not on path")

    work_dir = os.path.dirname(tex_file_path)

    subprocess.run([xelatex, tex_file_path], cwd=work_dir, check=True, capture_output=silent)

    if rerun:
        # For some things LaTeX needs a second pass, so we run it again (but don't log output).
        subprocess.run([xelatex, tex_file_path], cwd=work_dir, check=True, capture_output=silent)
