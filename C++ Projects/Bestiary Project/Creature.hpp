#ifndef CREATURE_HPP
#define CREATURE_HPP

#include <string>

class Creature {
public:
  Creature();
  Creature( const std::string& NAME,
            const std::string& TYPE,
            const std::string& ELEMENT,
            int LEVEL,
            double AGGRESSION,
            double RESILIENCE,
            double INTELLIGENCE );

  // queries
  const std::string& name() const;
  const std::string& type() const;
  const std::string& element() const;

  int level() const;
  double aggression() const;
  double resilience() const;
  double intelligence() const;

  // computations
  double threatLevel() const;
  std::string description() const;

private:
  std::string _name;
  std::string _type;
  std::string _element;

  int _level;                // 0–10
  double _aggression;        // 0–10
  double _resilience;        // 0–10
  double _intelligence;      // 0–10
};

#endif // CREATURE_HPP
