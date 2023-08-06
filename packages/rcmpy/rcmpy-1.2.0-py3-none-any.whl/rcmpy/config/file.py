"""
A module implementing an interface for package-managed files.
"""

# built-in
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from shutil import copyfile
import sys
from typing import Set

# third-party
from vcorelib.logging import LoggerType
from vcorelib.paths import rel


@dataclass
class ManagedFile:
    """
    A data structure for managed files specified in the configuration data.
    """

    template: str
    extra_templates: Set[str]

    directory: Path
    name: str

    link: bool

    platforms: Set[str]

    @property
    def output(self) -> Path:
        """Get the full output path."""
        return self.directory.joinpath(self.name)

    @property
    def platform(self) -> bool:
        """Determine if the platform is correct for handling this file."""
        return not self.platforms or sys.platform in self.platforms

    def update_root(self, root: Path) -> None:
        """
        If the output directory is a relative path, update it to be an
        absolute one based on the provided root directory.
        """

        if not self.directory.is_absolute():
            self.directory = root.joinpath(self.directory)
            assert self.directory.is_absolute(), self.directory

    def update(self, source: Path, logger: LoggerType) -> None:
        """Update this managed file based on the provided source file."""

        output = self.output

        # At some point this could be skipped for existing symlinks.
        with suppress(FileNotFoundError):
            output.unlink()

        # Ensure the output directory exists.
        self.directory.mkdir(parents=True, exist_ok=True)

        if self.link:
            output.symlink_to(source)
        else:
            copyfile(source, output)

        logger.info("'%s' -> '%s'.", rel(source), rel(output))
