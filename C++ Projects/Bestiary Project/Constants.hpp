#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <string>

namespace constants {

  // file name constant
  inline const std::string DATA_FILE = "creatures.txt";

  // threat weights
  constexpr double AGGRESSION_WEIGHT = 0.50;
  constexpr double RESILIENCE_WEIGHT = 0.30;
  constexpr double INTELLIGENCE_WEIGHT = 0.20;

  // level scale (level 0–10)
  constexpr double LEVEL_SCALE = 1.0 / 10.0;

}

#endif // CONSTANTS_HPP
