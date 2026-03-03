#ifndef MAZE_HPP
#define MAZE_HPP

#include <cstddef>
#include <string>
#include <vector>

class Maze {
public:
  bool load( const std::string& filename );

  int rows() const { return _rows; }
  int cols() const { return _cols; }

  char at( int r, int c ) const
  {
    return _grid.at( static_cast<std::size_t>( r ) )
               .at( static_cast<std::size_t>( c ) );
  }

  char& at( int r, int c )
  {
    return _grid.at( static_cast<std::size_t>( r ) )
               .at( static_cast<std::size_t>( c ) );
  }

  int startRow() const { return _startRow; }
  int startCol() const { return _startCol; }

private:
  int _rows = 0;
  int _cols = 0;

  int _startRow = -1;
  int _startCol = -1;

  std::vector<std::vector<char>> _grid;
};

#endif // MAZE_HPP

