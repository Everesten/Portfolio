#include "Solver.hpp"

#include <cstddef>
#include <iostream>
#include <string>

const int DR[4] = { -1, 0, 1, 0 };
const int DC[4] = { 0, 1, 0, -1 };

Solver::Solver( const Maze& maze, SolveMode mode )
  : _maze( maze ),
    _mode( mode ),
    _rows( maze.rows() ),
    _cols( maze.cols() ),
    _visited( static_cast<std::size_t>( _rows ),
              std::vector<bool>( static_cast<std::size_t>( _cols ), false ) ),
    _frontier( static_cast<std::size_t>( _rows ),
               std::vector<bool>( static_cast<std::size_t>( _cols ), false ) ),
    _parent( static_cast<std::size_t>( _rows ),
             std::vector<std::pair<int, int>>( static_cast<std::size_t>( _cols ),
                                               { -1, -1 } ) ),
    _path( static_cast<std::size_t>( _rows ),
           std::vector<bool>( static_cast<std::size_t>( _cols ), false ) )
{
  const int sr = _maze.startRow();
  const int sc = _maze.startCol();

  const std::size_t rr = static_cast<std::size_t>( sr );
  const std::size_t cc = static_cast<std::size_t>( sc );

  if( _mode == SolveMode::BFS ) {
    _q.push( { sr, sc } );
  } else {
    _s.push( { sr, sc } );
  }

  _frontier.at( rr ).at( cc ) = true;
}

bool Solver::step()
{
  if( !_searching ) {
    return false;
  }

  std::pair<int, int> cur;

  if( _mode == SolveMode::BFS ) {
    if( _q.empty() ) {
      _searching = false;
      return false;
    }
    cur = _q.front();
    _q.pop();
  } else {
    if( _s.empty() ) {
      _searching = false;
      return false;
    }
    cur = _s.top();
    _s.pop();
  }

  const int r = cur.first;
  const int c = cur.second;

  const std::size_t rr = static_cast<std::size_t>( r );
  const std::size_t cc = static_cast<std::size_t>( c );

  if( _visited.at( rr ).at( cc ) ) {
    return true;
  }

  _visited.at( rr ).at( cc ) = true;
  _frontier.at( rr ).at( cc ) = false;

  if( _maze.at( r, c ) == 'E' ) {
    std::cout << "Reached the end!" << std::endl;
    _foundEnd = true;
    _searching = false;
    rebuildPath( r, c );
    return false;
  }

  for( int i = 0; i < 4; i++ ) {
    const int nr = r + DR[i];
    const int nc = c + DC[i];

    if( nr < 0 || nr >= _rows || nc < 0 || nc >= _cols ) {
      continue;
    }
    if( _maze.at( nr, nc ) == '#' ) {
      continue;
    }

    const std::size_t nrr = static_cast<std::size_t>( nr );
    const std::size_t ncc = static_cast<std::size_t>( nc );

    if( _visited.at( nrr ).at( ncc ) ) {
      continue;
    }
    if( _frontier.at( nrr ).at( ncc ) ) {
      continue;
    }

    _frontier.at( nrr ).at( ncc ) = true;
    _parent.at( nrr ).at( ncc ) = { r, c };

    if( _mode == SolveMode::BFS ) {
      _q.push( { nr, nc } );
    } else {
      _s.push( { nr, nc } );
    }
  }

  return true;
}

void Solver::rebuildPath( int r, int c )
{
  while( r >= 0 && c >= 0 ) {
    const std::size_t rr = static_cast<std::size_t>( r );
    const std::size_t cc = static_cast<std::size_t>( c );

    _path.at( rr ).at( cc ) = true;

    const std::pair<int, int> parent = _parent.at( rr ).at( cc );
    if( parent.first < 0 ) {
      break;
    }

    r = parent.first;
    c = parent.second;
  }
}
