"""
Assignment 2 - Sample Tests

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains sample tests for Assignment 2, Tasks 1 and 2.
The tests use the provided example-directory, so make sure you have downloaded
and extracted it into the same place as this test file.
This test suite is very small. You should plan to add to it significantly to
thoroughly test your code.

IMPORTANT NOTES:
    - If using PyCharm, go into your Settings window, and go to
      Editor -> General.
      Make sure the "Ensure line feed at file end on Save" is NOT checked.
      Then, make sure none of the example files have a blank line at the end.
      (If they do, the data size will be off.)

    - os.listdir behaves differently on different
      operating systems.  These tests expect the outcomes that one gets
      when running on the *Teaching Lab machines*.
      Please run all of your tests there - otherwise,
      you might get inaccurate test failures!

    - Depending on your operating system or other system settings, you
      may end up with other files in your example-directory that will cause
      inaccurate test failures. That will not happen on the Teachin Lab
      machines.  This is a second reason why you should run this test module
      there.
"""
import os

from hypothesis import given
from hypothesis.strategies import integers

from tm_trees import TMTree, FileSystemTree
from papers import PaperTree

EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')


def test_single_file() -> None:
    """Test a tree with a single file.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    assert tree._name == 'draft.pptx'
    assert tree._subtrees == []
    assert tree._parent_tree is None
    assert tree.data_size == 58
    assert is_valid_colour(tree._colour)


new_path = os.path.join(os.getcwd())

'''
testing for update_rectangle
'''


def test_tree_zero_data_empty_subtrees():
    """
    Test that a FileSystemTree with no data and no subtrees results in a
    rectangle with zero size when `update_rectangles` is called.
    """
    file = FileSystemTree(os.path.join(new_path, 'testfolder'))
    file.update_rectangles((0, 0, 100, 100))
    file.expand()
    assert file.rect == (0, 0, 0, 0)


def test_tree_zero_data_nonempty_subtrees() -> None:
    """
    Test that a FileSystemTree with no data but with non-empty subtrees results
    in a rectangle with zero size, and that each subtree also has a rectangle
    with zero size.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'activities', 'images'))
    tree.update_rectangles((0, 0, 0, 0))
    assert tree.rect == (0, 0, 0, 0)
    for subtree in tree._subtrees:
        assert subtree.rect == (0, 0, 0, 0)


def test_tree_rect_zero_width() -> None:
    """
    Test that a FileSystemTree has a rectangle with zero width when updated with
    zero width dimensions.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 0, 100))
    assert tree.rect == (0, 0, 0, 100)


def test_tree_rect_zero_height() -> None:
    """
    Test that a FileSystemTree has a rectangle with zero height when updated
    with zero height dimensions.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 100, 0))
    assert tree.rect == (0, 0, 100, 0)


def test_tree_rect_negative_width() -> None:
    """
    Test that a FileSystemTree allows for negative width in
    the rectangle dimensions,
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, -100, 100))
    assert tree.rect == (0, 0, -100, 100)


def test_tree_rect_negative_height() -> None:
    """
    Test that a FileSystemTree allows for negative height in
    the rectangle dimensions,
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 100, -100))
    assert tree.rect == (0, 0, 100, -100)


'''
testcase for get_rectangles
'''

path = os.path.join(os.getcwd(), 'testfolder')


def test_tree_data_size_zero() -> None:
    """
    Test that an empty list of rectangles is returned for a tree with zero
    data size and no subtrees, which means it's a leaf with size 0.
    """
    tree = FileSystemTree(os.path.join(path, 'empty.txt'))
    rects = tree.get_rectangles()
    assert rects == []


def test_tree_not_expanded_data_size_zero() -> None:
    """
    Test that an empty list of rectangles is returned for a tree that is not
    expanded and has a data size of 0.
    """
    tree = FileSystemTree(path)
    assert not tree._expanded
    rects = tree.get_rectangles()
    assert not rects


path2 = os.path.join(os.getcwd(), 'testfolder2')


def test_subtrees_not_expanded_data_size_zero_except_two() -> None:
    """
    Test that a list with a double rectangle is returned when all subtrees but
    two have a data size of 0. The two subtree with data
    should be represented.
    """
    tree = FileSystemTree(path2)
    assert len(
        tree.get_rectangles()) == 1  # not expanded, the parent is displayed
    tree.expand_all()
    rects = tree.get_rectangles()
    assert len(
        rects) == 2  # now the two files with 1 data size should be displayed
    #  ignoring the empty file
    assert tree.data_size == 2


'''
test cases for get_tree_at_position
'''

path3 = os.path.join(os.getcwd(), 'example-directory', 'workshop')
draftpath = os.path.join(path3, 'draft.pptx')


def test_get_tree_at_position_leaf_contains_pos() -> None:
    """
    Test that the method returns the leaf in the displayed tree whose rectangle
    contains the given position.
    """
    tree = FileSystemTree(draftpath)
    tree.update_rectangles((10, 10, 100, 100))
    result = tree.get_tree_at_position((20, 20))
    assert result is tree


def test_get_tree_at_position_outside_rect() -> None:
    """
    Test that the method returns None if the position is outside of this tree's
    rectangle.
    """
    tree = FileSystemTree(draftpath)
    tree.update_rectangles((10, 10, 100, 100))
    result = tree.get_tree_at_position((200, 200))
    assert result is None


def test_get_tree_at_position_on_shared_edge() -> None:
    """
    Test that the method returns the leftmost and topmost rectangle if the
    position is on the shared edge between two or more rectangles.
    """
    tree = FileSystemTree(path3)
    tree.update_rectangles((10, 10, 50, 100))
    rectangles_occupied = tree.get_rectangles()
    assert len(rectangles_occupied) == 1
    # after expanding it should display 3 rectangles
    tree.expand()
    rectangles_occupied = tree.get_rectangles()
    assert len(rectangles_occupied) == 3
    first, second, third = [rectangle[0] for rectangle in rectangles_occupied]
    #  first = (10, 10, 50, 14)
    #  second = (10, 24, 50, 38)
    #  first and second share the same coordinate
    f, s, t = [subtree for subtree in tree._subtrees]
    assert s.get_rectangles()[0][0] == second  # making sure correct coordinate
    assert f.get_rectangles()[0][0] == first  # making sure correct coordinate
    assert tree.get_tree_at_position((10, 24)) == f
    assert tree.get_tree_at_position((10, 24)) != s


def test_get_tree_at_position_multiple_leaves() -> None:
    """
    Test that the method returns the correct leaf when there are multiple leaves
    in the displayed tree.
    """
    tree = FileSystemTree(path3)
    tree.update_rectangles((0, 0, 100, 100))
    tree.expand()
    result = tree.get_tree_at_position((50, 50))
    assert isinstance(result, FileSystemTree)


def test_get_tree_at_position_pos_on_border() -> None:
    """
    Test that the method returns None when the position is on the border of the
    rectangle but not inside it.
    """
    tree = FileSystemTree(path3)
    tree.update_rectangles((10, 10, 100, 100))
    result = tree.get_tree_at_position((10, 10))  # Border case
    assert result == tree


def test_get_tree_at_position_pos_on_corner() -> None:
    """
    Test that the method returns None when the position is on the corner of the
    rectangle but not inside it.
    """
    tree = FileSystemTree(path3)
    tree.update_rectangles((10, 10, 100, 100))
    result = tree.get_tree_at_position((10, 110))  # Corner case
    assert result is tree


# def test_get_tree_at_position_empty_tree() -> None:
#     """
#     Test that the method returns None when the tree is empty.
#     """
#     tree = FileSystemTree(os.path.join(path2, 'empty.txt'))  # An empty tree
#     tree.update_rectangles((0, 0, 100, 100))
#     result = tree.get_tree_at_position((50, 50))
#     assert result is None


'''happy cases and edge cases for update_data_sizes
'''


def test_tree_no_subtrees() -> None:
    """
    Test that the data_size is correct for a tree with no subtrees.
    """
    tree = FileSystemTree(draftpath)
    #  assuming the ._DSstore files are included since thats
    #  the only way codetierlist will pass
    assert tree.update_data_sizes() == 58


def test_tree_one_subtree() -> None:
    """
    Test that the data_size is correct for a tree with one subtree.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'prep', 'images'))
    assert tree.update_data_sizes() == sum(
        subtree.data_size for subtree in tree._subtrees)


def test_tree_multiple_subtrees() -> None:
    """
    Test that the data_size is correct for a tree with multiple subtrees.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'activities', 'images'))
    assert tree.update_data_sizes() == sum(
        subtree.data_size for subtree in tree._subtrees)


def test_empty_tree() -> None:
    """
    Test that the data_size is 0 for an empty tree.
    """
    tree = FileSystemTree(
        os.path.join(path2, 'empty.txt'))  # Create an empty tree
    assert tree.update_data_sizes() == 0


def test_tree_nested_subtrees() -> None:
    """
    Test that the data_size is correct for a tree with nested subtrees.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree.update_data_sizes() == sum(
        subtree.update_data_sizes() for subtree in tree._subtrees)


path1 = os.path.join(os.getcwd(), 'testfolder')


def test_tree_one_subtree_0_data() -> None:
    """
    Test that the data_size is correct for a tree with only one subtree and 0 data_size.
    """
    tree = FileSystemTree(path1)
    assert tree.update_data_sizes() == sum(
        subtree.data_size for subtree in tree._subtrees)


def test_tree_no_leaves_no_data() -> None:
    """
    Test that the data_size is 0 for a tree with no leaves and no data_size.
    """
    tree = FileSystemTree(os.path.join(path1, 'empty.txt'))
    assert tree.update_data_sizes() == 0


'''happy and edge cases for move function'''


def test_move_leaf_to_non_leaf_destination() -> None:
    """
    Test moving a leaf to a non-leaf destination.
    """
    leaf = FileSystemTree(EXAMPLE_PATH)
    leaf.update_rectangles((0, 0, 1200, 700))
    leaf.expand()
    a = leaf.get_rectangles()
    assert len(a) == 3
    #  randomly pick a leaf
    to_move = leaf.get_tree_at_position((600, 0))
    destination = leaf.get_tree_at_position((0, 0))
    #  this means it's a leaf draft.pptx
    assert to_move.data_size == 58
    to_move.move(destination)
    #  confirm that the leaf has been moved successfully
    assert to_move.get_parent() == destination


def test_move_leaf_to_leaf_destination() -> None:
    """
    Test moving a leaf to a leaf destination (should not move since destination is also a leaf).
    """
    # Set up the initial tree with two leaves
    leaf = FileSystemTree(EXAMPLE_PATH)
    leaf.update_rectangles((0, 0, 1200, 700))
    leaf.expand_all()
    to_move = leaf.get_tree_at_position((0, 0))
    destination = leaf.get_tree_at_position((1200, 700))
    #  both to_move and destination are leaf since we did expand_all()
    to_move.move(destination)
    assert to_move.get_parent() != destination


def test_move_non_leaf_to_destination() -> None:
    """
    Test moving a non-leaf to a destination (should not move because it's not a leaf).
    """
    leaf = FileSystemTree(EXAMPLE_PATH)
    leaf.update_rectangles((0, 0, 1200, 700))
    leaf.expand()
    a = leaf.get_rectangles()
    assert len(a) == 3
    #  randomly pick a leaf
    destination = leaf.get_tree_at_position((600, 0))
    to_move = leaf.get_tree_at_position((0, 0))
    to_move.expand()
    #  this shows that when expanding a to_move its not a leaf
    #  since the number of rectangles increased meaning it had subtrees
    assert len(leaf.get_rectangles()) > 3
    to_move.collapse()
    to_move.move(destination)
    assert to_move.get_parent() != destination


def test_move_leaf_to_itself() -> None:
    """
    Test moving a leaf to itself (should not move).
    """
    # Setup
    leaf = FileSystemTree(EXAMPLE_PATH)
    leaf.update_rectangles((0, 0, 1200, 700))
    leaf.expand()
    assert len(leaf.get_rectangles()) == 3
    to_move = leaf.get_tree_at_position((600, 0))
    to_move.move(to_move)
    assert to_move.get_parent() == leaf


def test_move_leaf_to_empty_tree() -> None:
    """
    Test moving a leaf to an empty tree (should not move).
    The empty tree is percieved as a leaf
    """
    # Setup
    leaf = FileSystemTree(EXAMPLE_PATH)
    leaf.update_rectangles((0, 0, 1200, 700))
    leaf.expand()
    a = leaf.get_rectangles()
    assert len(a) == 3
    #  randomly pick a leaf
    to_move = leaf.get_tree_at_position((600, 0))
    destination = leaf.get_tree_at_position((0, 0))
    destination.expand_all()
    assert len(leaf.get_rectangles()) > 3
    #  now destination is completely expanded
    destination = leaf.get_tree_at_position((0, 0))
    to_move.move(destination)
    assert to_move.get_parent() != destination


def test_move_leaf_to_tree_with_no_data() -> None:
    """
    Test moving a leaf to a tree with no data (should not move).
    """
    # Setup has 2 one byte files and an empty file
    to_move = FileSystemTree(path2)
    to_move.update_rectangles((0, 0, 100, 100))
    to_move.expand()
    a = to_move.get_tree_at_position((100, 100))
    #  this has data size 0
    destination = FileSystemTree(os.path.join(path2, 'empty.txt'))
    a.move(destination)
    #  it should not move since destination has data size 0
    assert to_move.get_parent() != destination


'''happy cases and edge cases for change_size'''


def test_change_size_positive_factor() -> None:
    """
    Test that the data_size of a tree is correctly increased by positive factor
    """
    # Setup
    tree = FileSystemTree(draftpath)  # Replace with the correct file path
    original_size = tree.data_size
    factor = 2  # Use an appropriate positive factor
    tree.change_size(factor)
    assert tree.data_size == 3 * original_size


def test_change_size_negative_factor() -> None:
    tree = FileSystemTree(draftpath)  # Replace with the correct file path
    original_size = tree.data_size
    factor = -0.5  # Use an appropriate positive factor
    tree.change_size(factor)
    assert tree.data_size == 0.5 * original_size


def test_change_size_zero_factor() -> None:
    tree = FileSystemTree(draftpath)  # Replace with the correct file path
    original_size = tree.data_size
    factor = 0  # Use an appropriate positive factor
    tree.change_size(factor)
    #  the size should remain unchanged
    assert tree.data_size == original_size


def test_change_size_one_factor() -> None:
    tree = FileSystemTree(draftpath)  # Replace with the correct file path
    original_size = tree.data_size
    factor = 1  # Use an appropriate positive factor
    tree.change_size(factor)
    assert tree.data_size == 2 * original_size


def test_change_size_negative_one_factor() -> None:
    tree = FileSystemTree(draftpath)  # Replace with the correct file path
    factor = -1  # Use an appropriate positive factor
    tree.change_size(factor)
    #  since a factor of -1 would mean the data size should be 0
    #  but the size could never go below 1 so the data size should
    #  be capped at 1
    assert tree.data_size == 1


import math

odd_size_path = os.path.join(EXAMPLE_PATH, 'activities', 'images', 'Q3.pdf')
even_size_path = draftpath


def test_change_size_half_factor_odd_data() -> None:
    """
    Test changing the data_size by a factor of 0.5 when data_size is known to be odd.
    """
    # Setup for an odd data_size
    tree = FileSystemTree(odd_size_path)  # Replace with the correct file path
    factor = 0.5
    expected_size = tree.data_size + math.ceil(tree.data_size * factor)
    tree.change_size(factor)
    assert tree.data_size == expected_size


def test_change_size_half_negative_factor_odd_data() -> None:
    """
    Test changing the data_size by a factor of -0.5 when data_size is known to be odd.
    """
    # Setup for an odd data_size
    tree = FileSystemTree(odd_size_path)  # Replace with the correct file path
    factor = -0.5
    expected_size = max(1, tree.data_size + math.floor(tree.data_size * factor))
    tree.change_size(factor)
    assert tree.data_size == expected_size


def test_change_size_half_factor_even_data() -> None:
    """
    Test changing the data_size by a factor of 0.5 when data_size is known to be even.
    """
    # Setup for an even data_size
    tree = FileSystemTree(even_size_path)  # Replace with the correct file path
    factor = 0.5
    expected_size = math.ceil(tree.data_size * (1 + factor))
    tree.change_size(factor)
    assert tree.data_size == expected_size


def test_change_size_half_negative_factor_even_data() -> None:
    """
    Test changing the data_size by a factor of -0.5 when data_size is known to be even.
    """
    # Setup for an even data_size
    tree = FileSystemTree(even_size_path)  # Replace with the correct file path
    factor = -0.5
    expected_size = max(1, tree.data_size + math.floor(tree.data_size * factor))
    tree.change_size(factor)
    assert tree.data_size == expected_size


def test_change_size_one_and_half_factor_odd_data() -> None:
    """
    Test changing the data_size by a factor of 1.5 when data_size is known to be odd.
    """
    # Setup for an odd data_size
    tree = FileSystemTree(odd_size_path)  # Replace with the correct file path
    factor = 1.5
    expected_size = math.ceil(tree.data_size * (1 + factor))
    tree.change_size(factor)
    assert tree.data_size == expected_size


def test_change_size_negative_one_and_half_factor_odd_data() -> None:
    """
    Test changing the data_size by a factor of -1.5 when data_size is known to be odd.
    """
    # Setup for an odd data_size
    tree = FileSystemTree(odd_size_path)  # Replace with the correct file path
    factor = -1.5
    expected_size = max(1, tree.data_size + math.floor(tree.data_size * factor))
    tree.change_size(factor)
    assert tree.data_size == expected_size


def test_change_size_one_and_half_factor_even_data() -> None:
    """
    Test changing the data_size by a factor of 1.5 when data_size is known to be even.
    """
    # Setup for an even data_size
    tree = FileSystemTree(even_size_path)  # Replace with the correct file path
    factor = 1.5
    expected_size = math.ceil(tree.data_size * (1 + factor))
    tree.change_size(factor)
    assert tree.data_size == expected_size


def test_change_size_negative_one_and_half_factor_even_data() -> None:
    """
    Test changing the data_size by a factor of -1.5 when data_size is known to be even.
    """
    # Setup for an even data_size
    tree = FileSystemTree(even_size_path)  # Replace with the correct file path
    factor = -1.5
    expected_size = max(1, tree.data_size + math.floor(tree.data_size * factor))
    tree.change_size(factor)
    assert tree.data_size == expected_size


'''happy and edge cases for delete_self()'''


# path3 = os.path.join(os.getcwd(), 'testfolder3')
#
#
# def test_remove_leaf_parent_which_has_one_leaf() -> None:
#     """
#     Test removing a leaf node from a tree whose parent have one leaf.
#     """
#     parent = FileSystemTree(path3)
#     parent.update_rectangles((0, 0, 1200, 700))
#     parent.expand_all()
#     # this is a valid leaf with one parent
#     destination = parent.get_tree_at_position((0, 0))
#     destination.collapse()
#     # checking the amount of rectangles, and it also checks that this leaf
#     # is the only leaf for its parent
#     # assert len(parent.get_rectangles()) == 1
#     destination.expand()
#     destination.delete_self()
#     # now the amount of rectangles should be lesser after delete
#     # assert len(parent.get_rectangles()) == 0


def test_remove_leaf_parent_multiple_leafs() -> None:
    parent = FileSystemTree(path2)
    parent.update_rectangles((0, 0, 100, 100))
    parent.expand()
    #  meaning parent has 2 trees its visualizing on the screen right now
    assert len(parent.get_rectangles()) == 2
    to_delete = parent.get_tree_at_position((50, 50))
    to_delete.delete_self()
    #  one of the 2 trees is now removed hence only 1 is displayed
    assert len(parent.get_rectangles()) == 1


def test_remove_from_empty_tree() -> None:
    """
    Test removing a node from an empty tree.
    """
    empty_tree = FileSystemTree(path1)
    empty_tree.expand()
    assert not empty_tree.delete_self()


def test_remove_non_leaf() -> None:
    """
    Test attempting to remove a node that is not a leaf.
    """
    non_leaf_tree = FileSystemTree(EXAMPLE_PATH)
    non_leaf_tree.update_rectangles((0, 0, 100, 100))
    # to_delete is not a leaf since it has subtrees
    to_delete = non_leaf_tree.get_tree_at_position((100, 100))
    assert not to_delete.delete_self()


def test_remove_node_no_parent() -> None:
    """
    Test attempting to remove a node that has no parent
    """
    node = FileSystemTree(os.path.join(path1, 'empty.txt'))
    assert not node.delete_self()


def test_delete_self_does_not_remove_parent_link() -> None:
    node = FileSystemTree(path3)
    node.update_rectangles((0, 0, 100, 100))
    node.expand()
    to_delete = node.get_tree_at_position((20, 20))
    to_delete.delete_self()
    # deleting does not set parent tree to None
    assert to_delete.get_parent() is not None


'''
happy cases and edge cases for expand()'''


def test_expand_tree_with_multiple_subtrees() -> None:
    """
    Test expanding a tree that has multiple subtrees.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand()
    assert tree._expanded, "Tree should be expanded"


def test_expand_tree_with_no_subtrees() -> None:
    """
    Test expanding a tree that has no subtrees.
    """
    tree = FileSystemTree(draftpath)
    tree.expand()
    assert not tree._expanded, "Tree with no subtrees should not expand"


def test_expand_tree_with_one_subtree() -> None:
    """
    Test expanding a tree that has exactly one subtree.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'prep', 'images'))
    tree.expand()
    assert tree._expanded


def test_expand_tree_with_parent() -> None:
    """
    Test expanding a tree that has a parent.
    """
    main_parent = FileSystemTree(EXAMPLE_PATH)
    main_parent.expand()
    # this should be expanded
    main_parent.expand()
    assert main_parent._expanded, "Tree with a parent should be expanded"


def test_expand_empty_tree() -> None:
    """
    Test expanding an empty tree.
    """
    # Represents an empty tree
    tree = FileSystemTree(path1)
    tree.expand()
    assert tree._expanded, "Empty tree should not expand"


def test_expand_tree_with_none_subtrees() -> None:
    """
    Test expanding a tree that is initialized with None subtrees.
    """
    tree = FileSystemTree(os.path.join(path2, 'one_byte.txt'))
    tree.expand()
    assert not tree._expanded, "Tree with None subtrees should not expand"


def test_expand_tree_with_empty_subtrees() -> None:
    """
    Test expanding a tree that has empty subtrees.
    """
    tree = FileSystemTree(os.path.join(path2, 'another_one_byte.txt'))
    tree.expand()
    assert not tree._expanded, "Tree with empty subtrees should not expand"


def test_expand_tree_with_zero_data_size() -> None:
    """
    Test expanding a tree that has a zero data_size.
    """
    tree = FileSystemTree(os.path.join(path1, 'empty.txt'))
    tree.expand()
    assert not tree._expanded, "Tree with zero data_size should still expand"


'''happy cases and edge cases for expand_all()'''


def test_expand_all_subtrees_not_none() -> None:
    """
    Test expand_all method on a tree where all subtrees are not None.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    assert tree._expanded


path4 = os.path.join(os.getcwd(), 'testfolder3')


def test_expand_all_subtrees_some_none() -> None:
    """
    Test expand_all method on a tree where some subtrees have data size 0.
    """
    tree = FileSystemTree(path4)
    tree.expand_all()
    assert len(tree.get_rectangles()) == 1


def test_expand_all_no_subtrees() -> None:
    """
    Test expand_all method on a tree with no subtrees.
    """
    tree = FileSystemTree(os.path.join(path4, 'empty.txt'))
    tree.expand_all()
    assert not tree._expanded, "Tree with no subtrees should not expand"


# Edge cases
def test_expand_all_empty_tree() -> None:
    """
    Test expand_all method on an empty tree.
    """
    tree = FileSystemTree(os.path.join(path4, 'empty.txt'))
    tree.expand_all()
    assert not tree._expanded, "Empty tree should not expand"


def test_expand_all_tree_no_subtrees() -> None:
    """
    Test expand_all method on a tree with no subtrees.
    """
    tree = FileSystemTree(path1)
    tree.expand_all()
    assert tree._expanded


def test_expand_all_subtrees_already_expanded() -> None:
    """
    Test expand_all method does nothing if all subtrees are already expanded.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 100, 100))
    tree.expand_all()
    assert not tree.get_tree_at_position((50, 50))._expanded
    node = tree.get_tree_at_position((50, 50))
    node.expand_all()
    assert not node._expanded


'''
happy cases and edge cases for collapse()'''


def test_collapse_leaf_node_with_multiple_siblings():
    """
    Test collapsing a leaf node that has siblings.
    """
    parent = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(parent)
    leaf = parent._subtrees[0]
    parent.expand_all()
    assert leaf._expanded
    leaf.collapse()
    assert not leaf._expanded


def test_collapse_leaf_node_with_single_sibling():
    """
    Test collapsing a leaf node that has only one sibling.
    """
    parent_path = os.path.join(EXAMPLE_PATH, 'activities')
    parent = FileSystemTree(parent_path)
    _sort_subtrees(parent)
    leaf = parent._subtrees[0]
    parent.expand_all()
    assert parent._expanded
    leaf.collapse()
    assert not leaf._expanded


def test_collapse_node_with_no_children():
    """
    Test collapsing a leaf node (node with no children).
    """
    leaf_path = os.path.join(EXAMPLE_PATH, 'draft.pptx')
    leaf = FileSystemTree(leaf_path)
    assert not leaf._expanded
    leaf.collapse()
    assert not leaf._expanded  # Still shouldn't be expanded


def test_collapse_node_already_collapsed():
    """
    Test collapsing a node that is already collapsed.
    """
    node_path = os.path.join(EXAMPLE_PATH, 'activities')
    node = FileSystemTree(node_path)
    assert not node._expanded
    node.collapse()  # Should still be collapsed after this
    assert not node._expanded


def test_collapse_empty_tree():
    """
    Test collapsing an empty tree.
    """
    empty_tree = FileSystemTree(os.path.join(path1))
    empty_tree.data_size = 0
    empty_tree.collapse()
    assert not empty_tree._expanded


def test_collapse_leaf_node_no_parent():
    """
    Test collapsing a leaf node with no parent.
    """
    leaf_path = os.path.join(draftpath)
    leaf = FileSystemTree(leaf_path)
    leaf.collapse()
    assert not leaf._expanded


def test_collapse_node_zero_data_size():
    """
    Test collapsing a node with zero data size.
    """
    node_path = os.path.join(
        os.path.join(path2, 'empty.txt'))  # Assume 'empty' is an empty folder
    node = FileSystemTree(node_path)
    node.collapse()
    assert not node._expanded


def test_collapse_node_with_parent_not_expanded():
    """
    Test collapsing a node where its parent is not expanded.
    """
    parent_path = os.path.join(EXAMPLE_PATH)
    parent = FileSystemTree(parent_path)
    _sort_subtrees(parent)
    node = parent._subtrees[1]  # Assuming this is a node with multiple children
    assert not parent._expanded  # Parent not expanded
    node.collapse()
    assert not node._expanded  # Node should remain collapsed


'''
happy cases and edge cases for collapse_all()'''


def test_collapse_all_subtrees():
    """
    Test collapsing all subtrees of a given tree.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    tree.collapse_all()
    assert not tree._expanded


def test_collapse_all_subtrees_recursively():
    """
    Test recursively collapsing all subtrees of a given tree.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    tree.collapse_all()
    for subtree in tree._subtrees:
        assert not subtree._expanded


def test_collapse_all_empty_tree():
    """
    Test that collapsing an empty tree does nothing.
    """
    tree = FileSystemTree(os.path.join(path2, 'empty.txt'))
    tree.collapse_all()
    assert not tree._expanded


def test_collapse_all_leaf_node():
    """
    Test that collapsing subtrees of a leaf node does nothing.
    """
    leaf = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    leaf.collapse_all()
    assert not leaf._expanded


def test_collapse_all_tree_no_subtrees():
    """
    Test collapsing a tree with no subtrees.
    """
    tree = FileSystemTree(os.path.join(path2))
    tree.collapse_all()
    assert not tree._expanded  # Tree with no subtrees should not be expanded


def test_collapse_all_tree_one_subtree():
    """
    Test collapsing subtrees of a tree with only one subtree.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH,
                                       'prep', 'images'))
    tree.expand_all()
    tree.collapse_all()
    assert not tree._expanded


def test_collapse_all_tree_multiple_subtrees():
    """
    Test collapsing subtrees of a tree with multiple subtrees.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    tree.collapse_all()
    for subtree in tree._subtrees:
        assert not subtree._expanded


def test_collapse_all_tree_multiple_levels_subtrees():
    """
    Test collapsing subtrees of a tree with multiple levels of subtrees.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.expand_all()
    tree.collapse_all()

    # Check all subtrees recursively
    def check_collapsed(t):
        assert not t._expanded
        for st in t._subtrees:
            check_collapsed(st)

    check_collapsed(tree)


# Edge Cases
def test_collapse_all_tree_no_data_size():
    """
    Test collapsing subtrees of a tree with no data_size.
    """
    tree = FileSystemTree(os.path.join(path1))
    assert tree.data_size == 0
    tree.collapse_all()
    assert not tree._expanded


def test_collapse_all_tree_no_rect():
    """
    Test collapsing subtrees of a tree with no rect.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    # Assume rect is not yet set
    tree.collapse_all()
    assert not tree._expanded


def test_collapse_all_tree_no_parent_tree():
    """
    Test collapsing subtrees of a tree with no parent_tree.
    """
    # A root tree has no parent_tree
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.collapse_all()
    assert not tree._expanded


"""testing for task 6
"""


def test_paper_tree_years() -> None:
    """testing the amount of years in cs1_papers.csv"""
    paper = PaperTree('CS1', [], all_papers=True, by_year=True)
    paper.update_rectangles((0, 0, 100, 100))
    paper.expand()
    years = paper.get_rectangles()
    assert len(years) == 45


def test_paper_tree_number_total_papers():
    """testing the total amount of papers in the entire csv"""
    paper = PaperTree('CS1', [], all_papers=True, by_year=True)
    paper.update_rectangles((0, 0, 100, 100))
    paper.expand_all()
    pages = paper.get_rectangles()
    assert len(pages) == 428


def test_paper_tree_2018_papers():
    """since there is only 1 paper in the csv for 2018
    having the citation 1 and others 0 hence there should
    only be one paper displaying in the 2018 category"""
    paper = PaperTree('CS1', [], all_papers=True, by_year=True)
    paper.update_rectangles((0, 0, 100, 100))
    paper.expand()
    # since 2018 is the last year in the csv
    a2018 = paper.get_tree_at_position((100, 100))
    a2018.expand()
    assert len(a2018.get_rectangles()) == 1


def test_paper_tree_number_of_categories():
    """since there are only 9 categories that should be correct"""
    # since we want to know the categories and not the year
    # by_year will be False
    paper = PaperTree('CS1', [], all_papers=True, by_year=False)
    paper.update_rectangles((0, 0, 100, 100))
    paper.expand()
    categories = paper.get_rectangles()
    assert len(categories) == 9


def test_paper_tree_paper_number_same():
    """the number of total papers should be the same
    with by_year as True and False"""
    paper1 = PaperTree('CS1', [], all_papers=True, by_year=False)
    paper2 = PaperTree('CS1', [], all_papers=True, by_year=True)
    paper1.expand_all()
    paper2.expand_all()
    a = paper1.get_rectangles()
    b = paper2.get_rectangles()
    assert len(a) == len(b)


##############################################################################
# Helpers
##############################################################################


def is_valid_colour(colour: tuple[int, int, int]) -> bool:
    """Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


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

    pytest.main(['a2_sample_test.py'])
