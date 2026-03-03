#include "Constants.hpp"
#include "Creature.hpp"

#include <iomanip>
#include <sstream>

using namespace std;

Creature::Creature()
  : _name(),
    _type(),
    _element(),
    _level( 0 ),
    _aggression( 0.0 ),
    _resilience( 0.0 ),
    _intelligence( 0.0 ) {
}

Creature::Creature( const string& NAME,
                    const string& TYPE,
                    const string& ELEMENT,
                    const int LEVEL,
                    const double AGGRESSION,
                    const double RESILIENCE,
                    const double INTELLIGENCE )
  : _name( NAME ),
    _type( TYPE ),
    _element( ELEMENT ),
    _level( LEVEL ),
    _aggression( AGGRESSION ),
    _resilience( RESILIENCE ),
    _intelligence( INTELLIGENCE ) {
}

// queries
const string& Creature::name() const {
  return _name;
}

const string& Creature::type() const {
  return _type;
}

const string& Creature::element() const {
  return _element;
}

int Creature::level() const {
  return _level;
}

double Creature::aggression() const {
  return _aggression;
}

double Creature::resilience() const {
  return _resilience;
}

double Creature::intelligence() const {
  return _intelligence;
}

// computations
double Creature::threatLevel() const {
  const double base =
      _aggression   * constants::AGGRESSION_WEIGHT +
      _resilience   * constants::RESILIENCE_WEIGHT +
      _intelligence * constants::INTELLIGENCE_WEIGHT;

  return base * ( _level * constants::LEVEL_SCALE );
}

string Creature::description() const {
  ostringstream out;

  out << _name << " ("
      << _type << ", "
      << _element << ", lvl " << _level << ") "
      << "A:" << _aggression
      << " R:" << _resilience
      << " I:" << _intelligence
      << " | Threat=" << fixed << setprecision( 2 ) << threatLevel();

  return out.str();
}
