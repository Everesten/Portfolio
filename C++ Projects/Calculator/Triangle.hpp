#ifndef TRIANGLE_HPP
#define TRIANGLE_HPP

#include "Polygon.hpp"

class Triangle : public Polygon {
public:
    // Default constructor sets up a 3-vertex polygon
    Triangle() {
        m_numVertices = 3;
        vertices = new Coordinate[static_cast<size_t>(m_numVertices)];
        
        // Initialize coordinates to {0,0}
        for (int i = 0; i < m_numVertices; ++i) {
            vertices[i] = {0.0, 0.0};
        }
    }
    // No validate since still abstract
};

#endif
