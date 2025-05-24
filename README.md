# Counterpoint

## Project Overview

This project is a Python program designed to generate counterpoint melodies for a given musical line (cantus firmus). It focuses on applying the principles of strict counterpoint within the framework of 12-tone equal temperament. The core functionality involves constructing a graph data structure to explore and store all valid counterpoint solutions based on the specified rules. The goal is to provide a tool for exploring the possibilities within strict counterpoint and potentially serve as a foundation for further musical generation or analysis.

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)

This project aims to generate counterpoint melodies for a given cantus firmus (a pre-existing melody). It focuses on generating all valid counterpoint solutions based on the rules of strict counterpoint, specifically using 12-tone equal temperament and avoiding the concept of scale degrees to maintain consistency with pitch and interval classes. The core data structure used is a graph, which efficiently stores and manages the potentially large number of possible valid counter-melodies.

## Getting Started

To run this project locally, follow these steps:

1. Clone the repository:



## Features

### 12 Tone Equal Temperament

This program uses 12 tone equal temperament, which is the most common tuning system in Western music. This means that the octave is divided into 12 equal parts. I am only using it because it cuts out a lot of complexity, not becuase it is the ideal.

For reasons against using this temperament system, see [this forum](https://modwiggler.com/forum/viewtopic.php?t=260593) and (ironically) [this video](https://www.youtube.com/watch?v=FY74AFQl2qQ)

### No Scale Degrees

This program does not use scale degrees. This is because the numbering of scale is inconsistent with the pitch and interval classes that this program uses.

### Completeness

This program finds every valid counterpoint solution.

<!-- ### Fitness Score

Inspired by the Foox repository, which aims to accomplish the same task as this one, each solution is scored according to certain features including how leaps are handled, the peak or low point,  -->

### Graph Data Structure

In order to find and store the huge number of valid counter-melodies for a given line, the possible melodies are store in a graph. This is ideal because any note could have many notes it could move to and many notes that it has moved from. So a linnear data structure would be wildly ineffieiccent because a new list would be needed for each possible line, and in a tree data structure, a node can't have more than one parent. I use the framework [NetworkX](https://networkx.org/documentation/stable/index.html) to create and manage the graphs used for the different species.