"""
Virtual working directory
=========================

Handles the complexities of working directory management and offers
minimalistic interface: file creation and file search, all from name
"""
import json
import uuid
from pathlib import Path
from typing import Generator, List, Optional, Union

from DRSlib.hash import get_temporary_dir_name

from .utils import assertTrue


class Node:
    """Data structure used to implement tree. It's serializable and has search functionnality"""

    def __init__(
        self,
        name: str,
        parent: Optional["Node"] = None,
        original_uuid: Optional[str] = None,
    ) -> None:
        self.uuid = uuid.uuid4() if uuid is None else uuid.UUID(original_uuid)
        self.name = name
        self.children: List["Node"] = []
        self.parent = parent
        self.depth: int = 0 if parent is None else parent.depth + 1

    @classmethod
    def from_json(cls, json_str: str) -> "Node":
        """Restores tree from the JSON-compliant string representation made by Node.to_json
        Returns root node; Depth-first algorithm
        """

        def dfs_recursively_load_nodes(
            node_dict: dict, parent_node: Optional["Node"] = None
        ) -> "Node":
            _node = Node(node_dict["name"], parent_node, node_dict["uuid"])
            _node.children = [
                dfs_recursively_load_nodes(c, _node)
                for c in node_dict.get("children", [])
            ]
            return _node

        return dfs_recursively_load_nodes(json.loads(json_str))

    def to_json(self, root_node: Optional["Node"] = None) -> Union[dict, str]:
        """Exports tree to JSON-compliant string representation; recursive; must be called on root
        Main call returns string representation, recursive calls return dict representation
        """
        assertTrue(
            root_node is not None or self.depth == 0, "Not executed on the root node"
        )
        _self_dict = {"uuid": self.uuid, "name": self.name}
        _root_node = self if root_node is None else root_node
        if not self.is_leaf:
            _self_dict["children"] = [c.to_json(_root_node) for c in self.children]
        return (
            json.dumps(_self_dict, indent=2, default=str)
            if root_node is None
            else _self_dict
        )

    @property
    def is_leaf(self) -> bool:
        """Only leaf nodes have no children"""
        return len(self.children) == 0

    def __str__(self) -> str:
        """String representation"""
        return (
            (str(self.parent.uuid) if self.parent is not None else "")
            + str(self.uuid)
            + self.name
        )

    def add_child(self, child: "Node") -> "Node":
        """Stores child and returns self so the call may be chained"""
        self.children.append(child)
        return self

    def search_uuid(self, target_uuid: uuid.UUID) -> Union["Node", None]:
        """Recursively searches for the node with given UUID"""
        if self.uuid == target_uuid:
            return self
        _child: "Node"
        for _child in self.children:
            found_node = _child.search_uuid(target_uuid)
            if found_node is not None:
                return found_node
        return None


class WorkingDirectory:
    """Organizes the working directory for a given file, abstracting away the complexities
    and providing useful functions"""

    INFO_FILE_PATH = lambda _dir: _dir / ".WD.json"

    def __init__(self, target_file: Path) -> None:
        assertTrue(
            target_file.exists() and target_file.is_file(),
            "Expected a valid target file, got '{}'",
            target_file,
        )
        self._file = target_file.resolve()
        self._cwd = Path(".").resolve()

        # determine working directory path
        self._dir: Path
        self._reserved = set()
        self.target_file_path, self.target_file_size = (
            self._file.as_posix(),
            self._file.stat().st_size,
        )
        for wd_path in self.generate_valid_paths(
            get_temporary_dir_name(self._file), directory=True
        ):
            # Case : available path => create it and choose it
            if not wd_path.exists():
                self._dir = wd_path.resolve()
                self._dir.mkdir()
                break

            # Case : path exists but isn't a WorkingDirectory
            _info_file: Path = WorkingDirectory.INFO_FILE_PATH(wd_path)
            if not (_info_file.exists() and _info_file.is_file()):
                continue

            # Case : path exists and is a WorkingDirectory but doesn't match target file info
            _existing_wd_info = json.loads(_info_file.read_text(encoding="utf8"))
            if not (
                _existing_wd_info.get("path") == self.target_file_path
                and _existing_wd_info.get("size") == self.target_file_size
            ):
                continue

            # Case : 'cache hit' on previously existing WorkingDirectory
            self._dir = wd_path.resolve()
            self._reserved = set(_existing_wd_info["reserved"])
            break

    @property
    def path(self) -> Path:
        """Absolute path of the working directory"""
        return self._dir

    def save_state(self) -> None:
        """Writes up to date info file"""
        WorkingDirectory.INFO_FILE_PATH(self.path).write_text(
            json.dumps(
                {
                    "path": self.target_file_path,
                    "size": self.target_file_size,
                    "reserved": self._reserved,
                }
            )
        )

    def generate_valid_paths(
        self, name: str, directory: bool = False, root: Optional[Path] = None
    ) -> Generator[Path, None, None]:
        """Yields candidate paths of a file or directory based on its name"""
        _dir = self.path if root is None else root
        _last_dot = name.rfind(".")
        yield _dir / name
        i = 0
        while True:
            i += 1
            yield _dir / (
                name + f" ({i})"
                if directory or _last_dot == -1
                else name[:_last_dot] + f" ({i})" + name[_last_dot:]
            )

    def new_file(self, filename: str) -> Path:
        """Returns an unused path for a new file in woking directory and marks it as reserved"""
        for _path in self.generate_valid_paths(filename):
            if not _path.exists():
                path_posix = _path.as_posix()
                if path_posix in self._reserved:
                    continue
                self._reserved.add(path_posix)
                self.save_state()
                return _path
        raise RuntimeError(
            f"Illegal state: Could not make a new path for file '{filename}'."
        )

    def get_file(self, name: str, relative_to_cwd: bool = False) -> Path:
        """Returns the path of a file that may or may not already exist in WorkingDirectory, which will NOT be reserved
        `relative_to_cwd` : absolute path if False, relative to cwd if True
        """
        _file_path: Path = self._dir / name
        return _file_path.relative_to(self._cwd) if relative_to_cwd else _file_path
