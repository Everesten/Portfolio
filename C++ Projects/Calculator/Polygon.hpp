#ifndef POLYGON_HPP
#define POLYGON_HPP

#include <SFML/Graphics.hpp>
#include <cmath>
#include "Coordinate.hpp"

// Floating-point helpers
static const double EPS = 1e-6;

inline bool eq(double a, double b) {
    return std::fabs(a - b) < EPS;
}

inline bool neq(double a, double b) {
    return std::fabs(a - b) >= EPS;
}

inline double dist(const Coordinate& a, const Coordinate& b) {
    const double dx = b.x - a.x;
    const double dy = b.y - a.y;
    return std::sqrt(dx*dx + dy*dy);
}

inline bool triangleInequality(double a, double b, double c) {
    return (a > 0 && b > 0 && c > 0) &&
           (a + b > c) &&
           (a + c > b) &&
           (b + c > a);
}

// Abstract Polygon class
class Polygon {
public:
    // Default constructor
    Polygon()
        : m_numVertices(0),
          vertices(nullptr),
          m_color(sf::Color::White) {}

    // Destructor
    virtual ~Polygon() {
        delete[] vertices;
    }

    // Prevent copying (Rule of 3)
    Polygon(const Polygon&) = delete;
    Polygon& operator=(const Polygon&) = delete;

    // Set fill color
    void setColor(sf::Color color) {
        m_color = color;
    }

    // Set coordinate safely
    void setCoordinate(int idx, Coordinate coord) {
        if (idx >= 0 && idx < m_numVertices && vertices != nullptr) {
            vertices[idx] = coord;
        }
    }

    // Pure virtual validation (must be const)
    virtual bool validate() const = 0;

    // Draw the polygon
    void draw(sf::RenderTarget& window) const {
        if (m_numVertices == 0 || vertices == nullptr) {
            return; // nothing to draw
        }

        sf::ConvexShape shape;
        shape.setPointCount(static_cast<size_t>(m_numVertices));

        for (int i = 0; i < m_numVertices; ++i) {
            shape.setPoint(static_cast<size_t>(i),
                           sf::Vector2f(
                               static_cast<float>(vertices[i].x),
                               static_cast<float>(vertices[i].y)));
        }

        shape.setFillColor(m_color);
        window.draw(shape);
    }

protected:
    short m_numVertices;
    Coordinate* vertices;

private:
    sf::Color m_color;
};

#endif
