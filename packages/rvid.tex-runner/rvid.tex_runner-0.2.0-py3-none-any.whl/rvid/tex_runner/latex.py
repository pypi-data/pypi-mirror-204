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

        success = run_xelatex(tex_file_path=tex_file_path, silent=silent)
        if not success:
            raise RuntimeError("Failure during XeLaTeX-run. Giving up. Logs above may not be "
                               "helpful. Try a manual run to get full context of what went wrong.")

        with open(pdf_file_path, "rb") as pdf_file:
            return pdf_file.read()


def run_xelatex(tex_file_path: str, rerun: bool = True, silent: bool = True) -> bool:
    xelatex = shutil.which("xelatex")
    if not xelatex:
        raise RuntimeError("xelatex is not on path")

    work_dir = os.path.dirname(tex_file_path)

    success = _do_run_run(xelatex=xelatex, tex_file_path=tex_file_path, work_dir=work_dir,
                          silent=silent)

    if rerun and success:
        # For some things LaTeX needs a second pass, so we run it again
        success = _do_run_run(xelatex=xelatex, tex_file_path=tex_file_path, work_dir=work_dir,
                              silent=silent)

    return success


def _do_run_run(xelatex, tex_file_path, work_dir, silent) -> bool:
    command_list = [xelatex, "-interaction=nonstopmode", tex_file_path]
    if silent:
        try:
            subprocess.check_output(command_list, cwd=work_dir)
        except subprocess.CalledProcessError as cpe:
            print(cpe.output)
            return False
    else:
        subprocess.run(command_list, cwd=work_dir, check=True)

    return True
