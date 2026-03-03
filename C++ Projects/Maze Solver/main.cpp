#include "Maze.hpp"
#include "Solver.hpp"

#include <SFML/Graphics.hpp>

#include <cstddef>
#include <iostream>
#include <string>

const int CELL_SIZE = 15;

sf::Color getCellColor( const Maze& maze, const Solver& solver, int r, int c )
{
  const char ch = maze.at( r, c );

  if( ch == '#' ) {
    return sf::Color::Black;
  }
  if( ch == 'S' ) {
    return sf::Color::Green;
  }
  if( ch == 'E' ) {
    return sf::Color::Red;
  }

  if( solver.foundEnd() &&
      solver.path().at( static_cast<std::size_t>( r ) )
                   .at( static_cast<std::size_t>( c ) ) ) {
    return sf::Color::Yellow;
  }

  if( solver.visited().at( static_cast<std::size_t>( r ) )
                       .at( static_cast<std::size_t>( c ) ) ) {
    return sf::Color( 255, 0, 255 );
  }

  if( solver.frontier().at( static_cast<std::size_t>( r ) )
                        .at( static_cast<std::size_t>( c ) ) ) {
    return sf::Color::Blue;
  }

  return sf::Color::White;
}

int main( int argc, char* argv[] )
{
  std::cout << "Solve maze using BFS or DFS? (B/D): ";
  char modeChar;
  std::cin >> modeChar;

  const SolveMode mode =
    ( modeChar == 'B' || modeChar == 'b' ) ? SolveMode::BFS : SolveMode::DFS;

  std::string filename;
  if( argc == 2 ) {
    filename = "mazePack/" + std::string( argv[1] );
  } else {
    std::cout << "Enter maze filename: ";
    std::cin >> filename;
    filename = "mazePack/" + filename;
  }

  Maze maze;
  if( !maze.load( filename ) ) {
    std::cerr << "Error: Failed to load maze '" << filename << "'" << std::endl;
    return 1;
  }

  Solver solver( maze, mode );

  const sf::Vector2u windowSize(
    static_cast<unsigned int>( maze.cols() * CELL_SIZE ),
    static_cast<unsigned int>( maze.rows() * CELL_SIZE ) );

  sf::VideoMode videoMode( windowSize, 32 );
  sf::RenderWindow window(
    videoMode,
    mode == SolveMode::BFS ? "Maze Runner (BFS)" : "Maze Runner (DFS)" );

  while( window.isOpen() ) {

    while( auto event = window.pollEvent() ) {
      if( event->is<sf::Event::Closed>() ) {
        window.close();
      }
    }

    solver.step();

    window.clear();

    for( int r = 0; r < maze.rows(); r++ ) {
      for( int c = 0; c < maze.cols(); c++ ) {

        sf::RectangleShape cell(
          sf::Vector2f(
            static_cast<float>( CELL_SIZE ),
            static_cast<float>( CELL_SIZE ) ) );

        cell.setPosition(
          sf::Vector2f(
            static_cast<float>( c * CELL_SIZE ),
            static_cast<float>( r * CELL_SIZE ) ) );

        cell.setFillColor( getCellColor( maze, solver, r, c ) );
        window.draw( cell );
      }
    }

    window.display();
    sf::sleep( sf::milliseconds( 50 ) );
  }

  return 0;
}