#ifndef SOLVER_HPP
#define SOLVER_HPP

#include "Maze.hpp"

#include <queue>
#include <stack>
#include <utility>
#include <vector>

enum class SolveMode { BFS, DFS };

class Solver {
public:
  Solver( const Maze& maze, SolveMode mode );

  bool step();

  bool foundEnd() const { return _foundEnd; }

  const std::vector<std::vector<bool>>& visited() const { return _visited; }
  const std::vector<std::vector<bool>>& frontier() const { return _frontier; }
  const std::vector<std::vector<bool>>& path() const { return _path; }

private:
  void rebuildPath( int r, int c );

  const Maze& _maze;
  SolveMode _mode;

  int _rows;
  int _cols;

  std::vector<std::vector<bool>> _visited;
  std::vector<std::vector<bool>> _frontier;
  std::vector<std::vector<std::pair<int, int>>> _parent;
  std::vector<std::vector<bool>> _path;

  std::queue<std::pair<int, int>> _q;
  std::stack<std::pair<int, int>> _s;

  bool _searching = true;
  bool _foundEnd = false;
};

#endif // SOLVER_HPP