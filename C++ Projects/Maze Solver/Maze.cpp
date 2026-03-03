/* CSCI 200: A6 – Maze Solver
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 * Date: Dec 11th, 2025
 *
 * Description: Solves a maze either through BFS or DFS!
 */

#include "Maze.hpp"

#include <fstream>
#include <string>

bool Maze::load( const std::string& filename )
{
  std::ifstream fin( filename );
  if( !fin.is_open() ) {
    return false;
  }

  fin >> _rows >> _cols;
  if( !fin || _rows <= 0 || _cols <= 0 ) {
    return false;
  }

  const std::size_t R = static_cast<std::size_t>( _rows );
  const std::size_t C = static_cast<std::size_t>( _cols );

  _grid.assign( R, std::vector<char>( C ) );

  std::string line;
  for( int r = 0; r < _rows; r++ ) {
    fin >> line;
    if( !fin || line.size() != C ) {
      return false;
    }

    for( int c = 0; c < _cols; c++ ) {
      const std::size_t rr = static_cast<std::size_t>( r );
      const std::size_t cc = static_cast<std::size_t>( c );

      _grid.at( rr ).at( cc ) = line.at( cc );

      if( line.at( cc ) == 'S' ) {
        _startRow = r;
        _startCol = c;
      }
    }
  }

  return true;
}