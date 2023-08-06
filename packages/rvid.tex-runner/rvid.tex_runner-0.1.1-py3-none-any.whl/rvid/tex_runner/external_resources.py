import os
import shutil
from dataclasses import dataclass, field
from logging import getLogger
from pathlib import Path
from typing import List, Optional, Pattern, Union

log = getLogger(__name__)


@dataclass
class ExternalResources:
    """
    Represent one or more external file that is referenced from a tex-file.

    The files may be directly next to the tex-file or in a sub-directory next
    to the tex-file. You cannot have a relative path above the tex-file in the
    filesystem hierarchy.

    The basedir attribute represents the name of the subdirectory where the
    files, which are listed in the "files" attribute, are to be copied.

    Use basedir value "." to place files next to the tex-file.
    """

    basedir: str
    files: List[Path] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.basedir.startswith("."):
            raise ValueError("Basedir for resources can't be above the tex-file itself")
        if self.basedir.startswith("/") or self.basedir.startswith("\\"):
            raise ValueError("Basedir must be a relative path")

    def clone_into_directory(self, target: Path) -> None:
        target_directory = os.path.join(target, self.basedir)
        os.makedirs(target_directory, exist_ok=True)
        for external_path in self.files:
            final_path = os.path.join(target_directory, os.path.basename(external_path))
            if os.path.isfile(final_path):
                raise IOError(f"File is already created by other ExternalResource: {final_path}")
            shutil.copy(external_path, final_path)


def make_external_resource_library(
    source_directory: Union[Path, str],
    relative_target_directory: str,
    file_include_filter: Optional[Pattern[str]] = None,
    file_exclude_filter: Optional[Pattern[str]] = None,
) -> ExternalResources:
    """
    Automatically generate an ExternalResources object from a directory.

    The `relative_target_directory` is the base of relative paths as used in the .tex file (e.g.
    "images" for the complete path "images/ape.png"). All *files* below the `source_directory`
    will be copied into the relative_target_directory. *Sub-directories* in the source directory
    will be ignored.

    You can optionally exclude/include files using compiled regexes.
    """
    if not os.path.isdir(source_directory):
        raise IOError("Source directory must exist")

    library_path = os.path.abspath(source_directory)

    paths_in_library = []

    for dir_entry in os.listdir(library_path):
        if os.path.isdir(os.path.join(library_path, dir_entry)):
            continue

        if file_include_filter and not file_include_filter.match(dir_entry):
            continue

        if file_exclude_filter and file_exclude_filter.match(dir_entry):
            continue

        fpath = os.path.join(library_path, dir_entry)
        paths_in_library.append(Path(fpath))

    if not paths_in_library:
        log.warning(
            f"Created external resource library without any files in it for: {source_directory}"
        )

    return ExternalResources(basedir=relative_target_directory, files=paths_in_library)
