#include "Bestiary.hpp"
#include "Constants.hpp"

#include <exception>
#include <iostream>
#include <limits>

using namespace std;

static int menu() {
  cout << endl
       << "=== Arcane Bestiary Manager ===" << endl
       << "1) List all creatures" << endl
       << "2) Add creature" << endl
       << "3) Remove creature" << endl
       << "4) Show strongest creature" << endl
       << "5) Generate encounter (target avg, count)" << endl
       << "6) Average threat (all)" << endl
       << "7) Save & Exit" << endl
       << "> ";

  int choice;

  if( !( cin >> choice ) ) {
    return 7;
  }

  cin.ignore( numeric_limits<streamsize>::max(), '\n' );

  return choice;
}

int main() {
  Bestiary bestiary;

  if( bestiary.loadFromFile( constants::DATA_FILE ) ) {
    cout << "Loaded data from " << constants::DATA_FILE << "." << endl;
  } else {
    cout << "No data file found; starting empty." << endl;
  }

  while( true ) {
    const int choice = menu();

    if( choice == 1 ) {
      bestiary.listAll();
    } else if( choice == 2 ) {
      string name;
      string type;
      string element;
      int level;
      double aggression;
      double resilience;
      double intelligence;

      cout << "Name: ";
      cin.ignore( numeric_limits<streamsize>::max(), '\n' );
      getline( cin, name );

      cout << "Type: ";
      getline( cin, type );

      cout << "Element: ";
      getline( cin, element );

      cout << "Level (0-10): ";
      cin >> level;

      cout << "Aggression (0-10): ";
      cin >> aggression;

      cout << "Resilience (0-10): ";
      cin >> resilience;

      cout << "Intelligence (0-10): ";
      cin >> intelligence;

      cin.ignore( numeric_limits<streamsize>::max(), '\n' );

      if( bestiary.addCreature(
            Creature( name, type, element, level,
                      aggression, resilience, intelligence ) ) ) {
        cout << "Added." << endl;
      } else {
        cout << "A creature with that name already exists." << endl;
      }
    } else if( choice == 3 ) {
      string name;

      cout << "Remove by name: ";
      cin.ignore( numeric_limits<streamsize>::max(), '\n' );
      getline( cin, name );

      if( bestiary.removeCreature( name ) ) {
        cout << "Removed." << endl;
      } else {
        cout << "Not found." << endl;
      }
    } else if( choice == 4 ) {
      try {
        Creature strongest = bestiary.strongestCreature();
        cout << "Strongest -> " << strongest.description() << endl;
      } catch( const exception& e ) {
        cout << e.what() << endl;
      }
    } else if( choice == 5 ) {
      double targetAverage;
      int count;

      cout << "Target average threat: ";
      cin >> targetAverage;

      cout << "Count: ";
      cin >> count;

      cin.ignore( numeric_limits<streamsize>::max(), '\n' );

      vector<Creature> group = bestiary.generateEncounter( targetAverage, count );

      if( group.empty() ) {
        cout << "No encounter generated." << endl;
      } else {
        double totalThreat = 0.0;

        for( const Creature& creature : group ) {
          cout << "  " << creature.description() << endl;
          totalThreat += creature.threatLevel();
        }

        cout << "Group avg threat = "
             << ( totalThreat / static_cast<double>( group.size() ) )
             << endl;
      }
    } else if( choice == 6 ) {
      cout << "Average threat (all) = "
           << bestiary.averageThreat()
           << endl;
    } else {
      if( bestiary.saveToFile( constants::DATA_FILE ) ) {
        cout << "Saved to " << constants::DATA_FILE << ". Goodbye!" << endl;
      } else {
        cout << "Failed to save file. Goodbye!" << endl;
      }

      break;
    }
  }

  return 0;
}
