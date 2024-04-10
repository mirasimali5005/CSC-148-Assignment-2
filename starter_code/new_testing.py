import os

from hypothesis import given
from hypothesis.strategies import integers

from tm_trees import TMTree, FileSystemTree

import math
import os
from typing import Tuple


# def test_single_file():
#     file_path = os.path.join(os.getcwd(), 'main_testing', 'dir_1', 'file1.txt')
#     tree = FileSystemTree(file_path)
#     assert tree._name == 'file1.txt'
#     assert tree._subtrees == []
#     assert tree._parent_tree is None
#     assert tree.data_size == 500  # Assuming the size is 500 bytes as per setup_test_directory
#
# def test_activities_folder():
#     dir_path = os.path.join(os.getcwd(), 'main_testing', 'dir_2', 'subdir_2_1')
#     tree = FileSystemTree(dir_path)
#     assert tree._name == 'subdir_2_1'
#     assert tree._parent_tree is None  # FileSystemTree doesn't automatically set _parent_tree
#     assert tree.data_size == 15000  # Sum of file sizes in subdir_2_1 (file10.png and file11.jpg)
#     assert len(tree._subtrees) == 2  # Contains file10.png and file11.jpg
#
#
# def test_deleting():
#     import tempfile
#     import shutil
#
#     # Create a temporary directory within main_testing to simulate deletion
#     temp_dir_path = os.path.join(os.getcwd(), 'main_testing', 'temp_dir')
#     os.makedirs(temp_dir_path, exist_ok=True)
#     temp_file_path = os.path.join(temp_dir_path, 'tempfile.txt')
#
#     # Create a temporary file
#     with open(temp_file_path, 'w') as f:
#         f.write('Hello, world!')
#
#     tree = FileSystemTree(temp_dir_path)
#     # Your deletion logic here, depending on FileSystemTree's implementation
#     # Verify deletion and directory size update
#
#     # Cleanup the temporary directory after the test
#     shutil.rmtree(temp_dir_path)
#
# def test_decrease_leaf_size():
#     leaf_path = os.path.join(os.getcwd(), 'main_testing', 'dir_1', 'file2.txt')
#     leaf_tree = FileSystemTree(leaf_path)
#     initial_size = leaf_tree.data_size
#
#     # Conceptually decrease the file size
#     decrease_amount = 2  # Assume we somehow removed 2 bytes
#     leaf_tree.change_size(-0.001)
#     print(f"Simulating a decrease of {decrease_amount} bytes in {leaf_path}")
#
#     # Assuming FileSystemTree can update or refresh to reflect this change
#     # For this example, we manually check the expected decreased size
#     assert leaf_tree.data_size == initial_size - decrease_amount


# def test_move_leaf_to_new_parent():
#     root = FileSystemTree(os.path.join(os.getcwd(), 'main_testing'))
#
#     # Locate 'file1.txt' in 'dir_1'
#     dir1 = next(
#         subtree for subtree in root._subtrees if subtree._name == 'dir_1')
#     file1 = next(
#         subtree for subtree in dir1._subtrees if subtree._name == 'file1.txt')
#
#     # Locate 'dir_2' to move 'file1.txt' into
#     dir2 = next(
#         subtree for subtree in root._subtrees if subtree._name == 'dir_2')
#
#     # Move 'file1.txt' from 'dir_1' to 'dir_2'
#     file1.move(dir2)
#
#     # Assertions
#     assert file1 not in dir1._subtrees
#     assert file1 in dir2._subtrees
#     assert file1._parent_tree == dir2

def test_decrease_leaf_size():
    root = FileSystemTree(os.path.join(os.getcwd(), 'main_testing'))
    root.update_rectangles((0, 0, 1200, 700))
    root.expand_all()

    # Assuming file2.txt is in dir_1
    dir1_pos = root.get_tree_at_position((1, 1)).rect[:2]  # Top-left corner
    dir1 = root.get_tree_at_position(dir1_pos)
    file2_pos = dir1.get_tree_at_position((1, 101)).rect[:2]  # Slightly down from the top-left corner
    file2 = dir1.get_tree_at_position(file2_pos)

    # Decrease the size of file2.txt by 20%
    original_size = file2.data_size
    file2.change_size(-0.20)

    # Check if the size of file2.txt has decreased by 20%
    expected_size = max(1, math.floor(original_size * 0.80))
    assert file2.data_size == expected_size

def test_increase_leaf_size():
    root = FileSystemTree(os.path.join(os.getcwd(), 'main_testing'))
    root.update_rectangles((0, 0, 1200, 700))
    root.expand_all()

    # Assuming file1.txt is in dir_1
    file1_pos = root.get_tree_at_position((1, 1)).rect[:2]  # Top-left corner
    file1 = root.get_tree_at_position(file1_pos)

    # Increase the size of file1.txt by 25%
    original_size = file1.data_size
    file1.change_size(0.25)

    # Check if the size of file1.txt has increased by 25%
    assert file1.data_size == math.ceil(original_size * 1.25)

def test_update_data_sizes_after_removal():
    root = FileSystemTree(os.path.join(os.getcwd(), 'main_testing'))
    root.update_rectangles((0, 0, 1200, 700))
    root.expand_all()

    # Assuming file12.txt is in dir_3
    dir3_pos = root.get_tree_at_position((1, 351)).rect[:2]  # Just below the top third

    dir3 = root.get_tree_at_position(dir3_pos)

    # Get file12.txt from dir_3
    file12_pos = dir3.get_tree_at_position((1, 1)).rect[:2]
    file12 = dir3.get_tree_at_position(file12_pos)

    # Remove file12.txt
    file12.delete_self()

    # Refresh the tree to reflect the changes
    root.update_rectangles((0, 0, 1200, 700))
    root.expand_all()

    # Assertions
    dir3_after = root.get_tree_at_position(dir3_pos)
    assert 'file12.txt' not in [subtree._name for subtree in dir3_after._subtrees]


def true_always():
    assert True

##############################################################################
# Helpers
##############################################################################


# def is_valid_colour(colour: tuple[int, int, int]) -> bool:
#     """Return True iff <colour> is a valid colour. That is, if all of its
#     values are between 0 and 255, inclusive.
#     """
#     for i in range(3):
#         if not 0 <= colour[i] <= 255:
#             return False
#     return True
#
#
def _sort_subtrees(tree: TMTree) -> None:
    """Sort the subtrees of <tree> in alphabetical order.
    THIS IS FOR THE PURPOSES OF THE SAMPLE TEST ONLY; YOU SHOULD NOT SORT
    YOUR SUBTREES IN THIS WAY. This allows the sample test to run on different
    operating systems.

    This is recursive, and affects all levels of the tree.
    """
    if not tree.is_empty():
        for subtree in tree._subtrees:
            _sort_subtrees(subtree)

        tree._subtrees.sort(key=lambda t: t._name)


if __name__ == '__main__':
    import pytest

    pytest.main(['new_testing.py'])
