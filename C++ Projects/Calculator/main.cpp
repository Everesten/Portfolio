/* CSCI 200: A5 – Polygon Land
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 * Date: November 24th, 2025
 *
 * Description:
 * Reads polygon specifications, validates each according to type,
 * prints invalid polygons, and draws all valid polygons using SFML.
 */

#include <iostream>
#include <fstream>
#include <vector>

#include <SFML/Graphics.hpp>

#include "ScaleneTriangle.hpp"
#include "IsoscelesTriangle.hpp"
#include "EquilateralTriangle.hpp"
#include "Rhombus.hpp"

int main() {

    // Open input file
    std::ifstream fin("polygons.dat");
    if (!fin.is_open()) {
        std::cerr << "Error opening polygons.dat\n";
        return 1;
    }

    std::vector<Polygon*> polys;

    while (true) {
        char type;
        if (!(fin >> type)) {
            break;   // no more input
        }

        // Coordinates + color
        double x1, y1, x2, y2, x3, y3, x4, y4;
        int r, g, b;

        Polygon* p = nullptr;

        // Read the correct number of coordinates based on type
        if (type == 'S' || type == 'I' || type == 'E') {
            if (!(fin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3 >> r >> g >> b)) {
                break;
            }
        }
        else if (type == 'R') {
            if (!(fin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3 >> x4 >> y4 >> r >> g >> b)) {
                break;
            }
        }
        else {
            // Unknown type
            std::cout << "polygon is invalid - \"unknown type\"\n";
            // skip line but continue reading
            std::string dummy;
            std::getline(fin, dummy);
            continue;
        }

        // Instantiate the correct polygon
        switch (type) {
            case 'S': p = new ScaleneTriangle(); break;
            case 'I': p = new IsoscelesTriangle(); break;
            case 'E': p = new EquilateralTriangle(); break;
            case 'R': p = new Rhombus(); break;
        }

        // Assign coordinates
        p->setCoordinate(0, {x1, y1});
        p->setCoordinate(1, {x2, y2});
        p->setCoordinate(2, {x3, y3});
        if (type == 'R') {
            p->setCoordinate(3, {x4, y4});
        }

        // Validate
        if (p->validate()) {
            p->setColor(sf::Color(
                static_cast<std::uint8_t>(r),
                static_cast<std::uint8_t>(g),
                static_cast<std::uint8_t>(b)
            ));
            polys.push_back(p);
        }
        else {
            // Print invalid polygon
            std::cout << "polygon is invalid - \""
                      << type << " "
                      << x1 << " " << y1 << " "
                      << x2 << " " << y2 << " "
                      << x3 << " " << y3;

            if (type == 'R') {
                std::cout << " " << x4 << " " << y4;
            }

            std::cout << " " << r << " " << g << " " << b << "\"\n";

            delete p;
        }
    }

    // === SFML WINDOW ===
    sf::VideoMode mode({650u, 650u});
    sf::RenderWindow window(mode, "Polygon Land");

    while (window.isOpen()) {

        while (auto event = window.pollEvent()) {
            if (event->is<sf::Event::Closed>()) {
                window.close();
            }
        }

        window.clear();

        for (auto* p : polys) {
            p->draw(window);
        }

        window.display();
    }

    // Clean up memory
    for (auto* p : polys) {
        delete p;
    }

    return 0;
}
