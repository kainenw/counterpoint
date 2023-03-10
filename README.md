# Counterpoint

A program for generating counter-melodies for melodies

## Features

### Completeness

This program finds every possible valid counterpoint solution.

### Fitness Score

Inspired by the Foox repository, which aims to accomplish the same task as this one, each solution is scored according to certain features including how leaps are handled, the peak or low point, 

### Graph Data Structure

In order to find and store the huge number of valid counter-melodies for a given line, the possible melodies are store in a graph. This is ideal because any note could have many notes it could move to and many notes that it has moved from. So a linnear data structure would be wildly ineffieiccent because a new list would be needed for each possible line, and a tree wouldn't be ideal because you would need a new tree each time 2 or more notes lead to only one note. and a tree structure are ill-suited make and it could have many  I use the framework [NetworkX](https://networkx.org/documentation/stable/index.html) to create and manage the graphs used for the different species.

