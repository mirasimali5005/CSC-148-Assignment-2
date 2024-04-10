# Treemaps Visualization Tool

Welcome to my Treemaps Visualization project! This tool is designed to visually represent hierarchical data through the concept of treemaps, allowing for interactive exploration of complex structures such as file systems and academic paper categorizations.

## Project Objectives

Through this project, I aimed to achieve the following:

- Model real-world hierarchical data using tree structures.
- Implement recursive tree operations, covering both non-mutating and mutating types.
- Develop a treemap algorithm for generating geometric tree visualizations.
- Interface with the computer's file system using the `os` library.
- Apply inheritance in class design to adhere to a common interface for diverse data types.

### Important Deadlines

This project was submitted on April 3, ahead of the semester's close on April 8. It's designed with a robust testing and version control workflow to ensure reliability and maintainability.

## Overview

Treemaps serve as an effective tool for representing hierarchical data. In this project, trees represent data models where leaves are data points and internal nodes are groupings or categories. The visualization aspect, a treemap, scales rectangles to demonstrate the weight or size of these data points, allowing for intuitive analysis and exploration.

## Getting Started

Included in this project:

- `print_dirs.py`: A demonstration script showcasing how to leverage the `os` module for file system interactions.
- `treemap_visualiser.py`: The main script that ties together the visualization logic.
- `tm_trees.py`: Contains the foundational classes for tree structure and treemap generation.
- `a2_sample_test.py`: A suite of tests ensuring the integrity of core functionalities.

I recommend starting with `tm_trees.py` to understand the data structures and then progressing to `treemap_visualiser.py` for visualization aspects.

## Project Components

### Data Modeller

The heart of this project lies in the `TMTree` class, which outlines a standard interface for any hierarchical data set ready for visualization. By extending this class, I've enabled the tool to support various data types, starting with file systems and academic research papers.

### Visualiser

The visualisation component is an interactive graphical interface that allows users to navigate through the treemap, offering functionalities such as node expansion/collapse and detailed views of selected data points.

## Development Journey

The project is structured into six key tasks, each building upon the last to gradually introduce complexity and functionality:

1. **Setup and Preliminaries**: Establishing the project structure and familiarizing myself with the provided starter code.
2. **File System Representation**: Crafting the `FileSystemTree` class to model file system data as a hierarchical tree.
3. **Treemap Algorithm Implementation**: Embedding the core logic within `TMTree` to calculate and update treemap rectangles.
4. **Tree Selection**: Enabling interactive selection of tree nodes within the treemap.
5. **Displayed-Tree Functionality**: Enhancing user interaction with expand/collapse capabilities to navigate large datasets efficiently.
6. **New Data Set Modeling**: Introducing a new data model, `PaperTree`, to demonstrate the tool's adaptability to different hierarchical data types.

## Conclusion and Submission

This project is a testament to the power of data visualization in simplifying the understanding of complex structures. It was meticulously tested and validated on DH lab machines to ensure compatibility and reliability.

I hope this tool proves useful for your data exploration needs and provides insights into the fascinating world of treemaps.

Happy exploring!
