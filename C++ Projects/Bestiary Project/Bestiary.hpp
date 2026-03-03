#ifndef BESTIARY_HPP
#define BESTIARY_HPP

#include "Creature.hpp"

#include <string>
#include <vector>

class Bestiary {
public:
  // CRUD
  bool addCreature( const Creature& CREATURE );
  bool removeCreature( const std::string& NAME );

  // Queries / reports
  void listAll() const;
  Creature strongestCreature() const; // throws if empty
  double averageThreat() const;

  std::vector<Creature> filterByElement( const std::string& ELEMENT ) const;

  // Encounter generation: greedy towards avgThreat * count
  std::vector<Creature> generateEncounter( double TARGET_AVG_THREAT,
                                           int COUNT ) const;

  // File I/O
  bool loadFromFile( const std::string& PATH );
  bool saveToFile( const std::string& PATH ) const;

  // Accessors
  std::size_t size() const {
    return _creatures.size();
  }

private:
  // helpers
  int indexByName( const std::string& NAME ) const;

  std::vector<Creature> _creatures;
};

#endif // BESTIARY_HPP
