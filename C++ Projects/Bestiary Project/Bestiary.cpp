#include "Bestiary.hpp"

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <vector>

using namespace std;

int Bestiary::indexByName(const string& name) const {
  for( size_t i = 0; i < _creatures.size(); i++ ) {
    if( _creatures.at( i ).name() == name ) {
      return static_cast<int>( i );
    }
  }

  return -1;
}

bool Bestiary::addCreature( const Creature& CREATURE ) {
  _creatures.push_back( CREATURE );
  return true;
}

bool Bestiary::removeCreature(const string& name) {
  int index = indexByName( name );

  if( index < 0 ) {
    return false;
  }

  _creatures.erase( _creatures.begin() + index );
  return true;
}

void Bestiary::listAll() const {
  if( _creatures.empty() ) {
    cout << "[empty]" << endl;
    return;
  }

  // sort by threat descending
  vector<const Creature*> order;
  order.reserve( _creatures.size() );

  for( const Creature& creature : _creatures ) {
    order.push_back( &creature );
  }

  sort(
    order.begin(),
    order.end(),
    [](const Creature* left, const Creature* right) {
      return left->threatLevel() > right->threatLevel();
    }
  );

  for( const Creature* creaturePtr : order ) {
    cout << creaturePtr->description() << endl;
  }
}

Creature Bestiary::strongestCreature() const {
  if( _creatures.empty() ) {
    throw runtime_error( "No creatures in bestiary." );
  }

  return *max_element(
    _creatures.begin(),
    _creatures.end(),
    [](const Creature& left, const Creature& right) {
      return left.threatLevel() < right.threatLevel();
    }
  );
}

double Bestiary::averageThreat() const {
  if( _creatures.empty() ) {
    return 0.0;
  }

  double sum = 0.0;

  for( const Creature& creature : _creatures ) {
    sum += creature.threatLevel();
  }

  return sum / static_cast<double>( _creatures.size() );
}

vector<Creature> Bestiary::filterByElement(const string& element) const {
  vector<Creature> filtered;

  for( const Creature& creature : _creatures ) {
    if( creature.element() == element ) {
      filtered.push_back( creature );
    }
  }

  return filtered;
}

std::vector<Creature> Bestiary::generateEncounter( double TARGET_AVG_THREAT,
                                                   int COUNT ) const {
  std::vector<Creature> result;

  if( COUNT <= 0 || _creatures.empty() ) {
    return result;
  }

  // prebuild sorted list of pointers (ascending by threat)
  std::vector<const Creature*> sorted;
  sorted.reserve( _creatures.size() );

  for( const Creature& CREATURE : _creatures ) {
    sorted.push_back( &CREATURE );
  }

  std::sort(
    sorted.begin(),
    sorted.end(),
    []( const Creature* LEFT, const Creature* RIGHT ) {
      return LEFT->threatLevel() < RIGHT->threatLevel();
    }
  );

  const double TARGET_TOTAL =
      TARGET_AVG_THREAT * static_cast<double>( COUNT );
  double runningTotal = 0.0;

  // 1) seed with the creature whose threat is closest to TARGET_AVG_THREAT
  auto closest = std::min_element(
    sorted.begin(),
    sorted.end(),
    [TARGET_AVG_THREAT]( const Creature* LEFT, const Creature* RIGHT ) {
      return std::abs( LEFT->threatLevel() - TARGET_AVG_THREAT )
           < std::abs( RIGHT->threatLevel() - TARGET_AVG_THREAT );
    }
  );

  if( closest != sorted.end() ) {
    result.push_back( **closest );
    runningTotal += ( **closest ).threatLevel();
  }

  // 2) greedily add creatures (WITH REPLACEMENT) to bring total close to TARGET_TOTAL
  while( static_cast<int>( result.size() ) < COUNT ) {
    const Creature* bestCreature = nullptr;
    double bestImprovement = std::numeric_limits<double>::infinity();

    for( const Creature* CANDIDATE : sorted ) {
      double candidateTotal = runningTotal + CANDIDATE->threatLevel();
      double improvement = std::abs( TARGET_TOTAL - candidateTotal );

      if( improvement < bestImprovement ) {
        bestImprovement = improvement;
        bestCreature = CANDIDATE;
      }
    }

    if( bestCreature == nullptr ) {
      break;
    }

    result.push_back( *bestCreature );
    runningTotal += bestCreature->threatLevel();
  }

  return result;
}

bool Bestiary::loadFromFile(const string& path) {
  ifstream file( path );

  if( !file.is_open() ) {
    return false;
  }

  string line;

  while( getline( file, line ) ) {
    if( line.empty() ) {
      continue;
    }

    stringstream ss( line );
    string name;
    string type;
    string element;
    int level;
    double aggression;
    double resilience;
    double intelligence;

    // parse "name,type,element,level,a,r,i"
    if( !getline( ss, name, ',' ) ) {
      continue;
    }
    if( !getline( ss, type, ',' ) ) {
      continue;
    }
    if( !getline( ss, element, ',' ) ) {
      continue;
    }

    char comma;

    if( !( ss >> level ) ) {
      continue;
    }
    if( !( ss >> comma ) || comma != ',' ) {
      continue;
    }
    if( !( ss >> aggression ) ) {
      continue;
    }
    if( !( ss >> comma ) || comma != ',' ) {
      continue;
    }
    if( !( ss >> resilience ) ) {
      continue;
    }
    if( !( ss >> comma ) || comma != ',' ) {
      continue;
    }
    if( !( ss >> intelligence ) ) {
      continue;
    }

    addCreature(
      Creature( name, type, element, level, aggression, resilience, intelligence )
    );
  }

  return true;
}

bool Bestiary::saveToFile(const string& path) const {
  ofstream file( path );

  if( !file.is_open() ) {
    return false;
  }

  for( const Creature& creature : _creatures ) {
    file << creature.name() << ","
         << creature.type() << ","
         << creature.element() << ","
         << creature.level() << ","
         << creature.aggression() << ","
         << creature.resilience() << ","
         << creature.intelligence() << endl;
  }

  return true;
}
