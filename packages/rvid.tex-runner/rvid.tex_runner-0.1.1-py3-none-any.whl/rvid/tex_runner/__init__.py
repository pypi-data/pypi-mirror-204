from pathlib import Path
from typing import Sequence

from .external_resources import ExternalResources, make_external_resource_library


def make_pdf_at_path(
    tex_content: str,
    ext_res_seq: Sequence[ExternalResources],
    target_path: Path,
    silent: bool = True,
) -> None:
    from .latex import make_pdf_in_tempdir

    pdf_data = make_pdf_in_tempdir(
        tex_file_content=tex_content, external_resource_sequence=ext_res_seq, silent=silent
    )

    with open(target_path, "wb") as outfile:
        outfile.write(pdf_data)


def make_pdf_as_bytestream(
    tex_file_content: str,
    external_resource_sequence: Sequence[ExternalResources],
    silent: bool = True,
) -> bytes:
    from .latex import make_pdf_in_tempdir

    return make_pdf_in_tempdir(
        tex_file_content=tex_file_content,
        external_resource_sequence=external_resource_sequence,
        silent=silent,
    )


__all__ = [
    "ExternalResources",
    "make_external_resource_library",
    "make_pdf_as_bytestream",
    "make_pdf_at_path",
]
