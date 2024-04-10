"""
Assignment 2: Trees for Treemap

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
import random
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._expanded = False

        self._colour = (random.randint(0, 255), random.randint(0, 255),
                        random.randint(0, 255))
        if len(subtrees) == 0:
            self.data_size = data_size
        else:
            self.data_size = 0
            for sub in self._subtrees:
                self.data_size = self.data_size + sub.data_size

            for sub1 in self._subtrees:
                sub1._parent_tree = self

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        self.rect = rect
        x, y, w, h = rect
        totalsize = 0
        for i in self._subtrees:
            totalsize += i.data_size
        tempx, tempy = x, y
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        if totalsize == 0:
            for subtree in self._subtrees:
                subtree.rect = (0, 0, 0, 0)
            return
        elif w > h:
            for i in range(len(self._subtrees)):
                subtree = self._subtrees[i]
                width = math.floor(subtree.data_size / totalsize * w)
                if i == len(self._subtrees) - 1:
                    width = w + x - tempx
                subtree.update_rectangles((tempx, y, width, h))
                tempx += width
        else:
            for i in range(len(self._subtrees)):
                subtree = self._subtrees[i]
                height = math.floor(subtree.data_size / totalsize * h)
                if i == len(self._subtrees) - 1:
                    height = h + y - tempy
                subtree.update_rectangles((x, tempy, w, height))
                tempy += height

    def get_rectangles(self) -> (
            List)[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if (self.is_empty()
                or self.data_size == 0):
            return []
        elif not self._expanded:
            return [(self.rect, self._colour)]
        else:
            main = []
            for subtree in self._subtrees:
                main += subtree.get_rectangles()
            return main

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        # if the cordinate is 0,0 then we should get the right pos
        # rx, ry, w, h = self.rect
        # x, y = pos
        # if rx <= x <= rx + w and ry <= y <= ry + h:
        #     if not self._expanded:
        #         return self
        #     else:
        #         for subtrees in self._subtrees:
        #             a = subtrees.get_tree_at_position(pos)
        #             if a:
        #                 return a
        # else:
        #     return None
        rx, ry, rw, rh = self.rect
        x, y = pos

        if rx <= x <= rx + rw and ry <= y <= ry + rh:
            if not self._expanded or not self._subtrees:
                return self
            for subtree in self._subtrees:
                subtree_at_pos = subtree.get_tree_at_position(pos)
                if subtree_at_pos:
                    return subtree_at_pos
        return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.
        >>> g1 = TMTree('g1', [], 45)
        >>> g2 = TMTree('g2', [], 20)
        >>> new_tree = TMTree('new_tree', [g1, g2], 0)
        >>> new_tree._subtrees.remove(g1)
        >>> len(new_tree._subtrees)
        1
        >>> new_tree.update_data_sizes()
        20
        """
        if not self._subtrees:
            return self.data_size
        else:
            self.data_size = sum(subtree.update_data_sizes()
                                 for subtree in
                                 self._subtrees)
            return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if (not self._subtrees and self._parent_tree
                and destination._subtrees != []):
            if self._parent_tree:
                self._parent_tree._subtrees.remove(self)
                self._parent_tree._correctsize()
            destination._subtrees.append(self)
            self._parent_tree = destination
            destination._correctsize()

    def _correctsize(self) -> None:
        self.data_size = sum(subtree.data_size for subtree in self._subtrees)
        if self._parent_tree:
            self._parent_tree._correctsize()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if not self._subtrees and not self.is_empty():
            if factor * self.data_size > 0:
                self.data_size += math.ceil(factor * self.data_size)
            else:
                if self.data_size + math.floor(factor * self.data_size) < 1:
                    self.data_size = 1
                else:
                    self.data_size += math.floor(factor * self.data_size)
            if self._parent_tree:
                self._parent_tree._correctsize()

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        # >>> leaf = TMTree('Leaf' , [], 10)
        # >>> a1 = TMTree('A1' , [], 55)
        # >>> b1 = TMTree('B1' , [], 45)
        # >>> leaf2 = TMTree('Leaf2' , [a1, b1], 0)
        # >>> parent = TMTree('Parent', [leaf, leaf2], 0)
        # >>> random1 = TMTree("r1", [], 125)
        # >>> random2 = TMTree("r2", [], 125)
        # >>> Des = TMTree('des', [random1, random2], 0)
        # >>> leaf.delete_self()
        # True
        # >>> parent._subtrees.__len__()
        # 1
        # >>> leaf._parent_tree == parent
        # True
        # >>> parent.data_size
        # 100
        # >>> b1.delete_self()
        # True
        # >>> leaf2._subtrees.__len__() == 1
        # True
        # >>> parent.data_size
        # 55
        # >>> leaf2.data_size
        # 55
        >>> g1 = TMTree('g1', [], 45)
        >>> g2 = TMTree('g2', [], 20)
        >>> new_tree = TMTree('new_tree', [g1], 0)
        >>> new_tree.delete_self()
        False
        >>> new_tree.data_size
        45
        >>> g1.delete_self()
        True
        >>> new_tree._subtrees.__len__() == 0
        True
        >>> new_tree.data_size
        0
        """
        if self._parent_tree:
            self._parent_tree._subtrees.remove(self)
            self._parent_tree._correctsize()
            return True
        return False

    def expand(self) -> None:
        """
        Expands the current tree node if it has subtrees.

        Sets the '_expanded' attribute to True if the current node has at least
        one subtree, otherwise sets it to False.
        """
        if self._subtrees is not None and self._subtrees:
            self._expanded = True
        else:
            self._expanded = False

    def expand_all(self) -> None:
        """
        Recursively expands the current tree node and all its subtrees.

        First, expands the current node by calling 'expand'. Then, for each
        subtree, if it is not None, recursively calls 'expand_all' to ensure
        all levels of subtrees are expanded.
        """
        if self._subtrees is not None:
            self.expand()
            for subtree in self._subtrees:
                if subtree is not None:
                    subtree.expand_all()

    def collapse(self) -> None:
        """
        Collapses the current tree node if it's not empty and has a parent tree.

        Sets the '_expanded' attribute of the current node to False and calls
        '_collapse_subtrees' to collapse all subtrees of the current node.
         Additionally, collapses all subtrees of the parent tree.
        """
        if not self.is_empty() and self._parent_tree:
            self._expanded = False
            self._collapse_subtrees()
            self._parent_tree._collapse_subtrees()

    def _collapse_subtrees(self) -> None:
        """
        Helper method to recursively collapse all subtrees of the current tree
        node.

        Sets the '_expanded' attribute of the current node to False and
        recursively calls '_collapse_subtrees' for each subtree, ensuring the
         entire subtree structure under the current node is collapsed.
        """
        self._expanded = False
        for subtree in self._subtrees:
            subtree._collapse_subtrees()

    def collapse_all(self) -> None:
        """
        Recursively collapses all subtrees of the current tree node
        and its parent trees.

        Calls '_collapse_subtrees' to collapse all subtrees of the current node.
        If the current node has a parent tree and the parent has subtrees, it
        recursively calls 'collapse_all' on the parent tree to ensure all levels
        are collapsed.
        """
        if self:
            self._collapse_subtrees()
        if self._parent_tree is not None:
            if self._parent_tree._subtrees:
                self._parent_tree.collapse_all()

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        if os.path.isdir(path):
            super().__init__(name=os.path.basename(path), subtrees=[],
                             data_size=0)
            for subtree in os.listdir(path):
                extended_path = os.path.join(path, subtree)
                node = FileSystemTree(extended_path)
                self.data_size += node.data_size
                self._subtrees.append(node)
            for i in self._subtrees:
                i._parent_tree = self
        else:
            size = os.path.getsize(path)
            super().__init__(name=os.path.basename(path), subtrees=[],
                             data_size=size)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
