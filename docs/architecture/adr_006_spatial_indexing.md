# ADR-006: Spatial Hash Grid vs R-Tree Indexing

## Status
Accepted

## Context
High-frequency nearest parking lot queries required low memory overhead.

## Decision
Adopt 1km cell size Spatial Hash Grid for O(1) cell lookups and low garbage collection overhead.
