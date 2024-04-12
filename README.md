# Treemaps Visualization Tool

Welcome to the Treemaps Visualization project! This tool is designed to visually represent hierarchical data through the concept of treemaps, enabling interactive exploration of complex structures such as file systems and academic paper categorizations.

## Project Objectives

- **Model Real-World Hierarchical Data**: Use tree structures to effectively represent complex, hierarchical data.
- **Implement Recursive Tree Operations**: Cover both non-mutating and mutating tree operations through recursion.
- **Develop a Treemap Algorithm**: Generate and manage treemap visualizations that depict the weight and structure of data points.
- **Interface with File Systems**: Utilize the `os` library for detailed file system interactions and representations.
- **Apply Inheritance in Class Design**: Use inheritance to ensure a common interface for diverse data types, enhancing the tool's modularity and flexibility.

## Getting Started

To begin using the Treemaps Visualization tool, explore the following components:

- **`tm_trees.py`**: Contains the foundational classes for tree structure and treemap generation.
- **`treemap_visualiser.py`**: Manages the visualization logic and user interface.
- **`print_dirs.py`**: Demonstrates file system interactions using the `os` module.
- **`a2_sample_test.py`**: Provides a suite of tests to ensure functionality and integrity of core components.

## Project Components

### Data Modeller

Central to this project is the `TMTree` class, designed to serve as a standard interface for any hierarchical data set intended for visualization. This class can be extended to support various data types, starting with file systems and potentially including academic research papers.

### Visualiser

This component is an interactive graphical interface that allows users to navigate the treemap, offering functionalities such as node expansion/collapse and detailed views of selected data points.

## Development Journey

The development was structured into six key tasks, each building upon the last to gradually introduce complexity and functionality:

1. **Setup and Preliminaries**: Establish the project structure and familiarize with the provided starter code.
2. **File System Representation**: Create the `FileSystemTree` class to model file system data as a hierarchical tree.
3. **Treemap Algorithm Implementation**: Integrate the core logic within `TMTree` to calculate and update treemap rectangles.
4. **Tree Selection**: Enable interactive selection of tree nodes within the treemap.
5. **Displayed-Tree Functionality**: Enhance user interaction with expand/collapse capabilities to efficiently navigate large datasets.
6. **New Data Set Modeling**: Introduce a new data model, `PaperTree`, to demonstrate the tool's adaptability to different hierarchical data types.

## Ethical Usage

This Treemaps Visualization Tool is provided for educational and personal use to foster understanding and exploration of hierarchical data through visual representation. **It is important to note that this tool and any part of its associated code, documentation, or conceptual design are not intended for plagiarism or any unethical use**. Users are encouraged to utilize this tool to enhance their own learning and for legitimate academic or personal projects.

By using this tool, you agree to adhere to the highest standards of academic integrity and respect intellectual property rights. This tool is meant to inspire and educate, not to facilitate copying or academic dishonesty.

## Conclusion and Submission

This project is a testament to the power of data visualization in simplifying the understanding of complex structures. It was meticulously tested and validated on DH lab machines to ensure compatibility and reliability.

Enjoy exploring the fascinating world of treemaps with my tool!
