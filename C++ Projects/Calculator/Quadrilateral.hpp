#ifndef QUADRILATERAL_HPP
#define QUADRILATERAL_HPP

#include "Polygon.hpp"

class Quadrilateral : public Polygon {
public:
    // Default constructor: sets up a 4-vertex polygon
    Quadrilateral() {
        m_numVertices = 4;
        vertices = new Coordinate[static_cast<size_t>(m_numVertices)];

        // Initialize coordinates to {0,0}
        for (int i = 0; i < m_numVertices; ++i) {
            vertices[i] = {0.0, 0.0};
        }
    }
};

#endif
