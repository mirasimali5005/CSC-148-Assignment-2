import unittest
import os
from tm_trees import TMTree, FileSystemTree


def repr_tree(tree: TMTree):
    parent_name = "None" if tree._parent_tree is None else tree._parent_tree._name
    if is_leaf(tree):
        return [(tree._name, tree.data_size, parent_name)]
    else:
        temp = []
        for sub in tree._subtrees:
            temp.extend(repr_tree(sub))
        temp += [(tree._name, tree.data_size, parent_name)]
        return temp


def is_leaf(tree):
    return not tree.is_empty() and tree._subtrees == []


def set_expanded(tree):
    tree.expand()


def set_size(tree, size):
    if is_leaf(tree):
        tree.data_size = size
    else:
        for sub in tree._subtrees:
            set_size(sub, size)
        tree.data_size = sum([sub.data_size for sub in tree._subtrees])


class a2_test_task2(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join('example-directory', "workshop")
        self.FileTree = FileSystemTree(self.path)

    def test_single_leaf(self):
        leaf = TMTree("leaf", [], 30)
        rect = (0, 0, 100, 100)
        leaf.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, rect,
                              "The leaf should have the exact rect as given")

    def test_one_level_tree(self):
        leaf = TMTree("leaf", [], 30)
        root = TMTree("root", [leaf], 40)
        rect = (0, 0, 100, 100)
        root.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, rect, "")
        self.assertCountEqual(root.rect, rect,
                              "Since the tree only contains a leaf so the root's rect should be same with leaf")

    def test_two_leaves(self):
        leaf = TMTree("leaf", [], 30)
        leaf2 = TMTree("leaf", [], 70)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 1000, 100)
        set_expanded(root)
        root.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, (0, 0, 300, 100),
                              "You should calculate the correct proportion of the leaf")
        self.assertCountEqual(leaf2.rect, (300, 0, 700, 100),
                              "You should calculate the correct proportion of the leaf")
        self.assertCountEqual(root.rect, rect,
                              "The root's rect should be exact same with the given argument")

    def test_two_leaves_round(self):
        leaf = TMTree("leaf", [], 30)
        leaf2 = TMTree("leaf", [], 69)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 200, 100)
        root.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, (0, 0, 60, 100),
                              "Round down the proportion of the leaf")
        self.assertCountEqual(leaf2.rect, (60, 0, 140, 100),
                              "Round down the proportion of the leaf")
        self.assertCountEqual(root.rect, rect,
                              "The root's rect should be exact same with the given argument")

    def test_two_leaves_round2(self):
        leaf = TMTree("leaf", [], 29)
        leaf2 = TMTree("leaf", [], 70)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 100, 200)
        root.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, (0, 0, 100, 58),
                              "You should calculate the correct proportion of the leaf")
        self.assertCountEqual(leaf2.rect, (0, 58, 100, 142),
                              "You should calculate the correct proportion of the leaf")
        self.assertCountEqual(root.rect, rect,
                              "The root's rect should be exact same with the given argument")

    def test_different_direction(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 30)
        leaf3 = TMTree("leaf3", [], 70)
        internal = TMTree("internal", [leaf2, leaf3], 0)
        root = TMTree("root", [internal, leaf], 0)
        rect = (0, 0, 210, 160)
        set_expanded(root)
        root.update_rectangles(rect)
        self.assertEqual(root.rect, rect,
                         "Root's size should be same with the given argument")
        self.assertEqual(internal.rect, (0, 0, 140, 160),
                         "internal's width takes the 2/3 of the given argument")
        self.assertEqual(leaf.rect, (140, 0, 70, 160),
                         "leaf's width should take 1/3 of the given argument")
        self.assertEqual(leaf2.rect, (0, 0, 140, 48),
                         "leaf 2 (The first leaf of internal)'s height should take 3/10 of INTERNAL'S HEIGHT")
        self.assertEqual(leaf3.rect, (0, 48, 140, 112),
                         "leaf3 (The second leaf of internal)'s height should take 7/10 of INTERNAL'S HEIGHT")

    def test_two_qual_height_tree(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        leaf3 = TMTree("leaf3", [], 50)
        leaf4 = TMTree("leaf4", [], 50)
        internal1 = TMTree("internal1", [leaf, leaf2], 0)
        internal2 = TMTree("internal2", [leaf3, leaf4], 0)
        root = TMTree("root", [internal1, internal2], 0)
        rect = (0, 0, 100, 100)
        set_expanded(root)
        root.update_rectangles(rect)
        self.assertEqual(root.rect, rect,
                         "Root's size should be same with the given argument")
        self.assertEqual(internal1.rect, (0, 0, 100, 50),
                         "internal1's height should take half of the root")
        self.assertEqual(internal2.rect, (0, 50, 100, 50),
                         "internal2's height should take half of the root")
        self.assertEqual(leaf.rect, (0, 0, 50, 50),
                         "leaf(the first leaf of internal1)'s weight should take half of the internal1")
        self.assertEqual(leaf2.rect, (50, 0, 50, 50),
                         "leaf2(the second leaf of internal1)'s weight should take second half of the internal1")
        self.assertEqual(leaf3.rect, (0, 50, 50, 50),
                         "leaf3(the first leaf of internal2)'s weight shoudl take half of the internal2's weight")
        self.assertEqual(leaf4.rect, (50, 50, 50, 50),
                         "leaf4(the second leaf of internal2)'s weight should take half of the internal2's weight")

    def test_complicate(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK = TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN = TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        set_expanded(root)
        rect = (0, 0, 210, 60)
        root.update_rectangles(rect)
        self.assertEqual(root.rect, rect,
                         "Root's rectangle should be same with given argument")
        self.assertEqual(folderA.rect, (0, 0, 70, 60),
                         "folderA(The first internal node of root)'s width should be 1/3 of the given argument")
        self.assertEqual(folderB.rect, (70, 0, 60, 60),
                         "folderB(The second internal node of root)'s width should be 6/21 of the given argument")
        self.assertEqual(folderC.rect, (130, 0, 80, 60),
                         "folderC(The third internal node of root)'s width should be 8/21 of the given argument")
        self.assertEqual(folderD.rect, (0, 0, 35, 60),
                         "folderD(The first internal node of folderA)'s width should be 1/2 of folderA's width")
        self.assertEqual(leafE.rect, (35, 0, 35, 60),
                         "leafE(The second element of folderA)'s width should take second half of folderA's width")
        self.assertEqual(leafI.rect, (0, 0, 35, 34),
                         "leafI(The first leaf of folderD)'s height should be 20/35 of the folderD's height")
        self.assertEqual(leafJ.rect, (0, 34, 35, 26),
                         "leafJ(The second leaf of folderD)'s height should be 15/35 of the folderD's height")
        self.assertEqual(folderF.rect, (70, 0, 60, 50),
                         "folderF(The first child of folderB)'s height should be 5/6 of the folderB's height")
        self.assertEqual(leafG.rect, (70, 50, 60, 10),
                         "leafG(The second child of folderB)'s height should be 1/6 of the folderB's hegiht")
        self.assertEqual(leafK.rect, (70, 0, 48, 50),
                         "leafK(The first child of folderF)'s width should be 4/5 of the folderF's width")
        self.assertEqual(leafL.rect, (118, 0, 12, 50),
                         "leafL(The second child of folderF)'s width should be 1/5 of the folderF's width")
        self.assertEqual(folderH.rect, (130, 0, 80, 60),
                         "folderH(The only child of folderC)'s rect should be same with folderC")
        self.assertEqual(folderM.rect, (130, 0, 40, 60),
                         "folderM(The first child of folderH)'s width should be half of the folderH's width")
        self.assertEqual(leafN.rect, (170, 0, 40, 60),
                         "leafN(The second child of folderH)'s width should be the second half of the folderH")
        self.assertEqual(leafO.rect, (130, 0, 40, 30),
                         "leafO(The first child of folderM)'s height should be the half of the folderM's height")
        self.assertEqual(leafP.rect, (130, 30, 40, 30),
                         "leafP(The second child of folderM)'s height should be the half of the folderM's height")

    def test_get_rectangle_task2(self):
        leaf = TMTree("leaf", [], 30)
        root = TMTree("root", [leaf], 40)
        rect = (0, 0, 100, 100)
        root.update_rectangles(rect)
        set_expanded(root)
        act = root.get_rectangles()
        assert len(act) == 1
        self.assertEqual(act[0][0], rect,
                         "For task 2 you should return every leaf of the DATA tree")

    def test_get_rectangle_task5(self):
        leaf = TMTree("leaf", [], 30)
        root = TMTree("root", [leaf], 40)
        rect = (0, 0, 100, 100)
        root.update_rectangles(rect)
        act = root.get_rectangles()
        assert len(act) == 1
        self.assertEqual(act[0][0], rect,
                         "For task 5 you should return every leaf of the DISPLAYED tree")

    # def test_two_leaves_task2(self):
    #     leaf = TMTree("leaf", [], 30)
    #     leaf2 = TMTree("leaf", [], 70)
    #     root = TMTree("root", [leaf, leaf2], 0)
    #     rect = (0, 0, 1000, 100)
    #     set_expanded(root)
    #     root.update_rectangles(rect)
    #     temp = root.get_rectangles()
    #     assert len(temp) == 2
    #     exp = [(0,0,300,100), (300,0,700,100)]
    #     act = [sub[0] for sub in temp]
    #     self.assertCountEqual(act, exp, "For task 2 you should return every leaf of the data tree")

    def test_two_leaves_task5(self):
        leaf = TMTree("leaf", [], 30)
        leaf2 = TMTree("leaf", [], 70)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 1000, 100)
        root.update_rectangles(rect)
        temp = root.get_rectangles()
        assert len(temp) == 1
        exp = [rect]
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should return every leaf of the displayed tree")

    # def test_different_direction_task2(self):
    #     leaf = TMTree("leaf", [], 50)
    #     leaf2 = TMTree("leaf2", [], 30)
    #     leaf3 = TMTree("leaf3", [], 70)
    #     internal = TMTree("internal", [leaf2, leaf3], 0)
    #     root = TMTree("root", [internal, leaf], 0)
    #     rect = (0, 0, 210, 160)
    #     exp = [(140, 0, 70, 160), (0,0, 140, 48),(0,48, 140, 112)]
    #     set_expanded(root)
    #     root.update_rectangles(rect)
    #     temp = root.get_rectangles()
    #     assert len(temp) == 3
    #     act = [sub[0] for sub in temp]
    #     self.assertCountEqual(act, exp, "For task2 you should return every leaf of the data tree")

    def test_different_direction_task5(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 30)
        leaf3 = TMTree("leaf3", [], 70)
        internal = TMTree("internal", [leaf2, leaf3], 0)
        root = TMTree("root", [internal, leaf], 0)
        rect = (0, 0, 210, 160)
        exp = [(0, 0, 140, 160), (140, 0, 70, 160)]
        root._expanded = True
        root.update_rectangles(rect)
        temp = root.get_rectangles()
        assert len(temp) == 2
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task5 you should return every leaf of the displayed tree")

    # def test_two_qual_height_tree_task2(self):
    #     leaf = TMTree("leaf", [], 50)
    #     leaf2 = TMTree("leaf2", [], 50)
    #     leaf3 = TMTree("leaf3", [], 50)
    #     leaf4 = TMTree("leaf4", [], 50)
    #     internal1 = TMTree("internal1", [leaf, leaf2], 0)
    #     internal2 = TMTree("internal2", [leaf3, leaf4], 0)
    #     root = TMTree("root", [internal1, internal2], 0)
    #     rect = (0,0,100,100)
    #     set_expanded(root)
    #     root.update_rectangles(rect)
    #     exp = [(0, 0, 50, 50), (50, 0, 50, 50), (0, 50, 50, 50), (50, 50, 50, 50)]
    #     temp = root.get_rectangles()
    #     assert len(temp) == 4
    #     act = [sub[0] for sub in temp]
    #     self.assertCountEqual(act, exp, "For task 2 you should return every leaf in the DATA tree")

    def test_two_qual_height_tree_task5(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        leaf3 = TMTree("leaf3", [], 50)
        leaf4 = TMTree("leaf4", [], 50)
        internal1 = TMTree("internal1", [leaf, leaf2], 0)
        internal2 = TMTree("internal2", [leaf3, leaf4], 0)
        root = TMTree("root", [internal1, internal2], 0)
        rect = (0, 0, 100, 100)
        root._expanded = True
        root.update_rectangles(rect)
        exp = [(0, 0, 100, 50), (0, 50, 100, 50)]
        temp = root.get_rectangles()
        assert len(temp) == 2
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should only return leaf in the DISPLAY tree")

    def test_two_qual_height_tree_task5_2(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        leaf3 = TMTree("leaf3", [], 50)
        leaf4 = TMTree("leaf4", [], 50)
        internal1 = TMTree("internal1", [leaf, leaf2], 0)
        internal2 = TMTree("internal2", [leaf3, leaf4], 0)
        root = TMTree("root", [internal1, internal2], 0)
        rect = (0, 0, 100, 100)
        root._expanded = True
        internal2._expanded = True
        root.update_rectangles(rect)
        exp = [(0, 0, 100, 50), (0, 50, 50, 50), (50, 50, 50, 50)]
        temp = root.get_rectangles()
        assert len(temp) == 3
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should only return leaf in the DISPLAY tree")

    # def test_complicate_task2(self):
    #     leafI = TMTree("leaf", [], 20)
    #     leafJ = TMTree("leaf2", [], 15)
    #     folderD = TMTree("folderD", [leafI, leafJ], 50)
    #     leafE = TMTree("leaf3", [], 35)
    #     folderA = TMTree("folderA", [folderD, leafE], 0)
    #     leafK = TMTree("leafK", [], 40)
    #     leafL = TMTree("leafL", [], 10)
    #     folderF = TMTree("folderF", [leafK, leafL], 0)
    #     leafG = TMTree("leafG", [], 10)
    #     folderB = TMTree("folderB", [folderF, leafG], 0)
    #     leafO = TMTree("leafO", [], 20)
    #     leafP = TMTree("leafP", [], 20)
    #     folderM = TMTree("leafM", [leafO, leafP], 40)
    #     leafN = TMTree("leafN", [], 40)
    #     folderH = TMTree("folderH", [folderM, leafN], 0)
    #     folderC = TMTree("folderC", [folderH], 0)
    #     root = TMTree("root", [folderA, folderB, folderC], 0)
    #     set_expanded(root)
    #     rect = (0, 0, 210, 60)
    #     set_expanded(root)
    #     root.update_rectangles(rect)
    #     exp = [(35, 0, 35, 60), (0, 0, 35, 34), (0, 34, 35, 26),
    #            (70, 50, 60, 10), (70, 0, 48, 50), (118, 0, 12, 50),
    #            (170, 0, 40, 60), (130, 0, 40, 30), (130, 30, 40, 30)]
    #     temp = root.get_rectangles()
    #     # assert len(temp) == 20
    #     act = [sub[0] for sub in temp]
    #     self.assertCountEqual(act, exp,
    #                           "For task 2 you should return every leaf in the DATA tree")

    def test_complicate_task5(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK = TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN = TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        root._expanded = True
        rect = (0, 0, 210, 60)
        root.update_rectangles(rect)
        exp = [(0, 0, 70, 60), (70, 0, 60, 60), (130, 0, 80, 60)]
        temp = root.get_rectangles()
        assert len(temp) == 3
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should return every leaf in the DISPLAYED tree")

    def test_complicate_task5_2(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK = TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN = TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        root._expanded = True
        folderC._expanded = True
        rect = (0, 0, 210, 60)
        root.update_rectangles(rect)
        exp = [(0, 0, 70, 60), (70, 0, 60, 60), (130, 0, 80, 60)]
        temp = root.get_rectangles()
        assert len(temp) == 3
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should return every leaf in the DISPLAYED tree")

    def test_complicate_task5_3(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK = TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN = TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        root._expanded = True
        folderA._expanded = True
        folderB._expanded = True
        folderC._expanded = True
        rect = (0, 0, 210, 60)
        root.update_rectangles(rect)
        exp = [(0, 0, 35, 60), (35, 0, 35, 60), (70, 0, 60, 50),
               (70, 50, 60, 10), (130, 0, 80, 60)]
        temp = root.get_rectangles()
        assert len(temp) == 5
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should return every leaf in the DISPLAYED tree")


unittest.main(exit=False)

import unittest
from tm_trees import *


def eq_tree(tree1, tree2):
    return tree1._name == tree2._name


class a2_test_task3(unittest.TestCase):
    def test_single_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 10, 20))
        self.assertEqual(leaf.get_tree_at_position((20, 30)), None,
                         "This is out of boundary None")

    def test_out_of_boundary(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 10, 20))
        self.assertEqual(leaf.get_tree_at_position((10, 30)), None,
                         "This is out of boundary None")

    def test_out_of_boundary2(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 10, 20))
        self.assertEqual(leaf.get_tree_at_position((0, 30)), None,
                         "This is out of boundary None")

    def test_single_leaf2(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 10, 20))
        self.assertEqual(leaf.get_tree_at_position((0, 5)), leaf,
                         "There is only one leaf in the displayed tree stasitied the condition thus you must return the leaf")

    def test_left_corner_no_expanded(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 10, 20))
        act = root.get_tree_at_position((0, 0))
        self.assertEqual(act, root,
                         "The root is the only leaf in the DISPLAYED Tree" " YOUR RESULT IS " + act._name)

    def test_left_corner_expanded(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0,0,10,20))
        root.expand()
        act = root.get_tree_at_position((0,0))
        self.assertEqual(act, leaf)
        a = root.get_tree_at_position((5,0))
        self.assertEqual(a, leaf)

    def test_vertical_bottom(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 10, 20))
        root.expand_all()
        act = root.get_tree_at_position((10, 20))
        self.assertEqual(act, leaf2,
                         "The leaf2 is the only qualified leaf in the DISPLAYED Tree"+ " YOUR RESULT IS " + act._name)

    def test_vertical_intersection(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 10, 20))
        root.expand()
        act = (root.get_tree_at_position((5, 10)))
        self.assertEqual(act, leaf)
        #                  "The leaf is the only qualified leaf in the DISPLAYED Tree"+ " YOUR RESULT IS " + act._name)

    # def test_horizontal_intersection(self):
    #     leaf = TMTree("leaf", [], 10)
    #     leaf2 = TMTree("leaf2", [], 50)
    #     root = TMTree("root", [leaf, leaf2], 0)
    #     root.update_rectangles((0, 0, 20, 10))
    #     root.expand()
    #     act = root.get_tree_at_position((3, 10))
    #     self.assertEqual(act, leaf)
    # #                      "The leaf is the only qualified leaf in the DISPLAYED Tree"+ " YOUR RESULT IS " + act._name)

    # def test_two_leaf_left(self):
    #     leaf = TMTree("leaf", [], 10)
    #     leaf2 = TMTree("leaf2", [], 50)
    #     root = TMTree("root", [leaf, leaf2], 0)
    #     root.update_rectangles((0, 0, 20, 10))
    #     set_expanded(root)
    #     act = root.get_tree_at_position((3, 10))
    #     self.assertEqual(act, leaf,
    #                      "The leaf is the only qualified leaf in the DISPLAYED Tree" + " YOUR RESULT IS " + act._name)

    def test_two_rectangle_left(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [folderA, leaf3], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        exp = folderA
        act = root.get_tree_at_position((3, 10))
        self.assertEqual(act, exp,
                         "The folderA is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    def test_three_rectangle_horizontal(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [folderA, leaf3], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        folderA._expanded = True
        exp = leaf2
        act = root.get_tree_at_position((3, 10))
        self.assertEqual(act, exp,
                         "The leaf2 is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    def test_three_rectangle_intersection(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [folderA, leaf3], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        folderA._expanded = True
        exp = leaf
        act = root.get_tree_at_position((5, 2))
        self.assertEqual(act, exp,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    def test_three_rectangle_intersection_2(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [folderA, leaf3], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        folderA._expanded = True
        exp = leaf
        act = root.get_tree_at_position((10, 2))
        self.assertEqual(act, exp,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    def test_three_rectangle_intersection_3(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [leaf3, folderA], 0)
        root.update_rectangles((0, 0, 10, 18))
        root._expanded = True
        folderA._expanded = True
        exp = leaf3
        act = root.get_tree_at_position((9, 2))
        self.assertEqual(act, exp,
                         "The leaf3 is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    # def test_four_square_intersection(self):
    #     leaf = TMTree("leaf", [], 50)
    #     leaf2 = TMTree("leaf2", [], 50)
    #     leaf3 = TMTree("leaf3", [], 50)
    #     leaf4 = TMTree("leaf4", [], 50)
    #     internal1 = TMTree("internal1", [leaf, leaf2], 0)
    #     internal2 = TMTree("internal2", [leaf3, leaf4], 0)
    #     root = TMTree("root", [internal1, internal2], 0)
    #     rect = (0, 0, 100, 100)
    #     set_expanded(root)
    #     root.update_rectangles(rect)
    #     exp = leaf
    #     act = root.get_tree_at_position((10, 2))
    #     self.assertEqual(act, exp,
    #                      "The leaf is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)
    #


unittest.main(exit=False)

import unittest
from tm_trees import *


class a2_test_update_size(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(0.1)
        exp = 55
        act = leaf.update_data_sizes()
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_folder(self):
        leaf = TMTree("leaf", [], 50)
        folder = TMTree("root", [leaf], 0)
        leaf.data_size = 55
        exp = 55
        act = folder.update_data_sizes()
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_folder2(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        leaf.data_size = 60
        leaf2.data_size = 70
        exp = 130
        act = root.update_data_sizes()
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_folder3(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        folderA = TMTree("folder", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 70)
        leaf4 = TMTree("leaf4", [], 80)
        folderB = TMTree("folder", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        leaf.data_size = 60
        leaf2.data_size = 70
        exp = 130
        act = folderA.update_data_sizes()
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))
        self.assertNotEqual(root.data_size, 280,
                            "You should not change the data size of parent tree")

    def test_folder4(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        folderA = TMTree("folder", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 70)
        leaf4 = TMTree("leaf4", [], 80)
        folderB = TMTree("folder", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        leaf.data_size = 60
        leaf2.data_size = 70
        exp = 280
        act = root.update_data_sizes()
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))
        self.assertEqual(root.data_size, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))
        self.assertEqual(folderA.data_size, 130,
                         "You should also update the data size of folderA")


class a2_test_change_size(unittest.TestCase):
    def test_up(self):
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(0.1)
        leaf.update_data_sizes()
        exp = 55
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_up2(self):
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(0.99)
        leaf.update_data_sizes()
        exp = 100
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_down(self):
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(-0.1)
        leaf.update_data_sizes()
        exp = 45
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_down2(self):
        leaf = TMTree("leaf", [], 50)
        leaf.change_size(-0.99)
        leaf.update_data_sizes()
        exp = 1
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_change_folder(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        root.change_size(0.01)
        root.update_data_sizes()
        self.assertEqual(root.data_size, 110,
                         "You cannot change the size of a folder")

    def test_change_folder2(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        leaf.change_size(0.1)
        root.update_data_sizes()
        exp = 55
        act = leaf.data_size
        self.assertEqual(act, 55,
                         "Expected " + str(exp) + " Your result is " + str(act))
        self.assertEqual(root.data_size, 115,
                         "When you change the size of a leaf you should also update its parent")

    def test_change_folder3(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        leaf.change_size(-0.1)
        root.update_data_sizes()
        exp = 45
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(
                             act))
        self.assertEqual(root.data_size, 105,
                         "When you change the size of a leaf you should update its parent also")

    def test_change_folder4(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        leaf.change_size(-0.1)
        root.update_data_sizes()
        exp = 45
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(
                             act))
        self.assertEqual(root.data_size, 105,
                         "When you change the size of a leaf you should update its parent also")


class a2_test_move(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        dest = TMTree("leaf", [], 60)
        leaf.move(dest)
        self.assertListEqual(leaf._subtrees, [],
                             "You cannot move a leaf to a leaf")

    def test_leaf2(self):
        leaf = TMTree("leaf", [], 60)
        leaf2 = TMTree("leaf2", [], 60)
        dest = TMTree("dest", [leaf2], 0)
        root = TMTree("dest", [dest, leaf], 0)
        leaf.move(dest)
        root.update_data_sizes()
        assert len(dest._subtrees) == 2
        self.assertEqual(dest._subtrees[-1], leaf,
                         "You should add leaf as the last element of dest's subtrees")
        self.assertEqual(leaf._parent_tree, dest,
                         "You should connect leaf to the proper parent tree after you move it")
        self.assertEqual(dest.data_size, 120,
                         "You should also update the data size of dest")

    def test_move_to_folder(self):
        leaf = TMTree("leaf", [], 60)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 60)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        folderA.move(folderB)
        root.update_data_sizes()
        self.assertEqual(folderA.data_size, 60, "Nothing should change")
        self.assertEqual(folderB.data_size, 60, "Nothing should change")
        self.assertEqual(len(folderA._subtrees), 1, "Nothing should change")
        self.assertEqual(len(folderB._subtrees), 1, "Nothing should change")

    def test_move_to_folder2(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 20)
        leaf3 = TMTree("leaf3", [], 30)
        folderA = TMTree("folderA", [leaf, leaf2, leaf3], 0)
        leaf4 = TMTree("leaf3", [], 60)
        leaf5 = TMTree("leaf4", [], 60)
        folderB = TMTree("folderB", [leaf4, leaf5], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root._expanded = True
        folderA._expanded = True
        folderB._expanded = True
        leaf2.move(folderB)
        root.update_data_sizes()
        root.update_rectangles((0, 0, 100, 100))

        assert len(folderA._subtrees) == 2 and len(folderB._subtrees) == 3
        self.assertEqual(leaf2._parent_tree, folderB,
                         "You should move to the correct parent tree")
        self.assertEqual(folderA.data_size, 40,
                         "You should update folderA's datasize")
        self.assertEqual(folderB.data_size, 140,
                         "You should update folderB's datasize")
        self.assertEqual(folderA.rect, (0, 0, 100, 22),
                         "You should update the rect of folderA")
        self.assertEqual(folderB.rect, (0, 22, 100, 78),
                         "You should update the rect of folderB")

    def test_move_to_folder3(self):
        leaf = TMTree("leaf", [], 60)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 60)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        folderA._expanded = True
        folderB._expanded = True
        root._expanded = True
        root.update_rectangles((0, 0, 100, 100))
        leaf.move(folderB)
        root.update_data_sizes()
        root.update_rectangles((0, 0, 100, 100))

        assert len(folderB._subtrees) == 2
        self.assertEqual(folderB._subtrees[-1], leaf,
                         "You should add leaf as the last element of folderB")
        self.assertEqual(leaf._parent_tree, folderB,
                         "You should point to the correct parent")
        self.assertEqual(folderB.data_size, 120,
                         "You should update the data size of folderB")
        self.assertEqual(folderA.data_size, 0,
                         "You should update the data size of folderA")
        self.assertEqual(root.data_size, 120,
                         "The root size remain same here since you did make so many change")
        self.assertEqual(folderA.rect, (0, 0, 0, 0),
                         "You should also update the rectangle of folderA")
        self.assertEqual(folderB.rect, (0, 0, 100, 100),
                         "You should also update the rectangle of folderB")


unittest.main(exit=False)

import unittest
from tm_trees import *


def set_expanded(tree):
    if is_leaf(tree):
        return [tree._expanded == False]
    else:
        temp = []
        temp.append(tree._expanded)
        for sub in tree._subtrees:
            temp.extend(set_expanded(sub))
        return temp


def set_collapse(tree):
    if is_leaf(tree):
        return [tree._expanded == False]
    else:
        temp = []
        temp.append(not tree._expanded)
        for sub in tree._subtrees:
            temp.extend(set_collapse(sub))
        return temp


class a2_task5_set_expanded(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 100, 100))
        leaf.expand()
        self.assertCountEqual([rect[0] for rect in leaf.get_rectangles()],
                              [(0, 0, 100, 100)])
        self.assertEqual(leaf._expanded, False,
                         "You cannot expanded a leaf(A single File)")

    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folder = TMTree("folder", [leaf], 50)
        folder.expand()
        self.assertEqual(folder._expanded, True,
                         "You can only expanded a folder")

    def test_multiple_folder(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 100, 50), (0, 50, 100, 50)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()],
                              [(0, 0, 100, 50)])
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderA")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderA to be True")
        self.assertEqual(folderB._expanded, False,
                         "You should not change the sibling of folderA")

    def test_multiple_folder2(self):
        leaf = TMTree("leaf", [], 40)
        leaf3 = TMTree("leaf3", [], 20)
        folderC = TMTree("folderC", [leaf, leaf3], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        folderC.expand()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 66, 60), (66, 0, 34, 60),
                               (0, 60, 100, 40)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()],
                              [(0, 0, 66, 60), (66, 0, 34, 60)])
        self.assertCountEqual([rect[0] for rect in folderC.get_rectangles()],
                              [(0, 0, 66, 60), (66, 0, 34, 60)])
        self.assertEqual(folderC._expanded, True,
                         "You should change the expaned of folderC")
        self.assertEqual(folderB._expanded, False,
                         "You should not change the sibiling of folderA")

    def test_multiple_folder3(self):
        leaf = TMTree("leaf", [], 40)
        folderC = TMTree("folderC", [leaf], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root._expanded = True
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderB.expand()
        root.get_rectangles()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 100, 50), (0, 50, 100, 50)])
        self.assertCountEqual([rect[0] for rect in folderB.get_rectangles()],
                              [(0, 50, 100, 50)])
        self.assertEqual(folderB._expanded, True,
                         "You should change the expanded of folderB")
        self.assertEqual(leaf2._expanded, False,
                         "You should not modifided the child of folderB")
        self.assertEqual(folderA._expanded, False,
                         "You should not change the sibiling of folderB")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderB to be True")
        self.assertEqual(folderC._expanded, False,
                         "You should not change the expanded of fodlerC")

    def test_multiple_folder4(self):
        leaf = TMTree("leaf", [], 40)
        leaf3 = TMTree("leaf3", [], 40)
        folderC = TMTree("folderC", [leaf, leaf3], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 120, 100))
        root.expand()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 80, 100), (80, 0, 40, 100)])

    def test_multiple_folder6(self):
        leaf = TMTree("leaf", [], 40)
        leaf3 = TMTree("leaf3", [], 20)
        folderC = TMTree("folderC", [leaf, leaf3], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root._expanded = True
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()],
                              [(0, 0, 100, 60)])
        folderC.expand()
        self.assertCountEqual([rect[0] for rect in folderC.get_rectangles()],
                              [(0, 0, 66, 60), (66, 0, 34, 60)])
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 66, 60), (66, 0, 34, 60),
                               (0, 60, 100, 40)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()],
                              [(0, 0, 66, 60), (66, 0, 34, 60)])
        self.assertEqual(folderC._expanded, True,
                         "You should not change the expaned of folderC")
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderC's parent")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderA to be True")
        self.assertEqual(folderB._expanded, False,
                         "You should not change the sibiling of folderA")

    def test_multiple_folder5(self):
        leaf = TMTree("leaf", [], 40)
        leaf3 = TMTree("leaf3", [], 20)
        folderC = TMTree("folderC", [leaf, leaf3], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root._expanded = True
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 100, 60), (0, 60, 100, 40)])
        self.assertEqual(folderC._expanded, False,
                         "You should not change the expaned of folderC")
        self.assertEqual(all(set_collapse(folderC)), True,
                         "You should not modify node under folderA")
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderC's parent")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderA to be True")
        self.assertEqual(folderB._expanded, False,
                         "You should not change the sibiling of folderA")


class a2_task5_test_expand_all(unittest.TestCase):
    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folder = TMTree("folder", [leaf], 50)
        folder.expand_all()
        act = all(set_expanded(folder))
        folder.update_rectangles((0, 0, 100, 100))
        rec = [rect[0] for rect in folder.get_rectangles()]
        self.assertCountEqual(rec, [(0, 0, 100, 100)])
        self.assertEqual(act, True,
                         "You should change every internal node under folder")

    def test_internal_node(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root._expanded = True
        root.expand()
        folderA.expand_all()
        temp = set_expanded(folderA)
        temp.pop(0)
        act = all(temp)
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()],
                              [(0, 0, 100, 50)])
        self.assertCountEqual(rec, [(0, 0, 100, 50), (0, 50, 100, 50)])
        self.assertEqual(act, True,
                         "You should change every internal under folderA")
        self.assertEqual(root._expanded, True,
                         "You should change root's expaned to be True")
        self.assertEqual(folderB._expanded, False,
                         "You should not modified folderB's expanded")

    def test_internal_node2(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root._expanded = True
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderB.expand_all()
        act = all(set_expanded(folderB))
        self.assertEqual(act, True,
                         "You should change the expanded of folderB")
        self.assertEqual(folderA._expanded, False,
                         "You should not modified folderA")
        self.assertCountEqual([rect[0] for rect in folderB.get_rectangles()],
                              [(0, 50, 100, 50)])
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 100, 50), (0, 50, 100, 50)])

    def test_internal_node3(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderC = TMTree("folderC", [leaf, leaf2], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand_all()
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(rec, [(0, 0, 50, 50), (50, 0, 50, 50),
                                    (0, 50, 100, 50)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()],
                              [(0, 0, 50, 50), (50, 0, 50, 50)])
        self.assertEqual(folderC._expanded, True,
                         "You should change the expaned of folderC")
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderC's parent")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderA to be True")
        self.assertEqual(folderB._expanded, False,
                         "You should not change the sibiling of folderA")

    def test_internal_node4(self):
        leaf = TMTree("leaf", [], 40)
        folderC = TMTree("folderC", [leaf], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 20)
        folderB = TMTree("folderB", [leaf2, leaf3], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        folderC.expand_all()
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(rec, [(0, 0, 100, 40), (0, 40, 100, 60)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()],
                              [(0, 0, 100, 40)])
        self.assertCountEqual([rect[0] for rect in folderC.get_rectangles()],
                              [(0, 0, 100, 40)])
        self.assertEqual(folderC._expanded, True,
                         "You should change the expaned of folderC")
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderC's parent")
        self.assertEqual(folderB._expanded, False,
                         "You should not change the sibiling of folderA")

    def test_root(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand_all()
        act = all(set_expanded(root))
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertEqual(act, True,
                         "You should change every internal node under root to be True")
        self.assertCountEqual(rec,
                              [(0, 0, 50, 50), (50, 0, 50, 50), (0, 50, 50, 50),
                               (50, 50, 50, 50)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()],
                              [(0, 0, 50, 50), (50, 0, 50, 50)])
        self.assertCountEqual([rect[0] for rect in folderB.get_rectangles()],
                              [(0, 50, 50, 50), (50, 50, 50, 50)])


class a2_task5_test_collapseall(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.collapse_all()
        self.assertEqual(leaf._expanded, False,
                         "You should not change the leaf")

    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        leaf.collapse_all()
        self.assertEqual(folderA._expanded, False,
                         "This should change the expanded of folderA to False")
        self.assertEqual(root._expanded, False, "This should change the root")
        self.assertCountEqual(folderA.get_rectangles()[0][0], (0, 0, 100, 100))

    def test_single_folder2(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.collapse_all()
        self.assertEqual(root._expanded, False,
                         "This has not effect on the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0, 0, 100, 100))

    def test_folder(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderB.expand()
        leaf2.collapse_all()
        self.assertEqual(root._expanded, False,
                         "You should set _expanded of every thing under root to False")
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(rec, [(0, 0, 100, 100)])

    def test_multiple_folder(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        folderB.expand()
        leaf2.collapse_all()
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(rec, [(0, 0, 100, 100)])
        self.assertEqual(root._expanded, False, "You should not modified root")


class a2_test_task5_collapse(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.collapse()
        self.assertEqual(leaf._expanded, False,
                         "You should not change the leaf")

    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        leaf.collapse()
        self.assertEqual(folderA._expanded, False,
                         "This should change the expanded of folderA to False")
        self.assertEqual(root._expanded, True, "This should change the root")
        self.assertCountEqual(folderA.get_rectangles()[0][0], (0, 0, 100, 100))

    def test_single_folder2(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.collapse()
        self.assertEqual(folderA._expanded, False,
                         "This has not effect on the folderA")
        self.assertEqual(root._expanded, False,
                         "This has not effect on the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0, 0, 100, 100))

    def test_folder(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderB.expand()
        leaf2.collapse()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 100, 50), (0, 50, 100, 50)])
        self.assertEqual(root._expanded, True,
                         "You should set _expanded of every thing under root to False")
        rec = [rect[0] for rect in folderB.get_rectangles()]
        self.assertCountEqual(rec, [(0, 50, 100, 50)])

    def test_multiple_folder(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        folderB.expand()
        leaf.collapse()
        rec = [rect[0] for rect in root.get_rectangles()]
        act = all(set_collapse(folderA))
        self.assertCountEqual(rec, [(0, 0, 100, 50), (0, 50, 50, 50),
                                    (50, 50, 50, 50)])
        self.assertEqual(root._expanded, True, "You should not modified root")
        self.assertEqual(act, True,
                         "You should set expanded of every thing under folderA be False")


class a2_test_collapseall(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.collapse_all()
        leaf.update_data_sizes()
        self.assertEqual(leaf._expanded, False,
                         "You should not change the leaf")

    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        leaf.collapse_all()
        self.assertEqual(folderA._expanded, False,
                         "This should change the expanded of folderA to False")
        self.assertEqual(root._expanded, False, "This should change the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0, 0, 100, 100))

    def test_single_folder2(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.collapse_all()
        self.assertEqual(folderA._expanded, False,
                         "This has not effect on the folderA")
        self.assertEqual(root._expanded, False,
                         "This has not effect on the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0, 0, 100, 100))

    def test_folder(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderB.expand()
        leaf2.collapse_all()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],
                              [(0, 0, 100, 100)])
        self.assertEqual(root._expanded, False,
                         "You should set _expanded of every thing under root to False")

    def test_multiple_folder(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        folderB.expand()
        leaf.collapse_all()
        rec = [rect[0] for rect in root.get_rectangles()]
        act = all(set_collapse(folderA))
        self.assertCountEqual(rec, [(0, 0, 100, 100)])
        self.assertEqual(root._expanded, False, "You should not modified root")


unittest.main(exit=False)
