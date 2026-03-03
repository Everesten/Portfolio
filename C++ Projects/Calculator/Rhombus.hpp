#ifndef RHOMBUS_HPP
#define RHOMBUS_HPP

#include "Quadrilateral.hpp"

class Rhombus : public Quadrilateral {
public:
    // Validates a rhombus: all sides equal and both triangles (0,1,2) & (0,2,3)
    // satisfy triangle inequality
    bool validate() const override {
        double L01 = dist(vertices[0], vertices[1]);
        double L12 = dist(vertices[1], vertices[2]);
        double L23 = dist(vertices[2], vertices[3]);
        double L30 = dist(vertices[3], vertices[0]);

        // diagonal
        double D02 = dist(vertices[0], vertices[2]);

        // must form two valid triangles
        if (!triangleInequality(L01, L12, D02)) {
            return false;
        }
        if (!triangleInequality(L23, L30, D02)) {
            return false;
        }

        // all four sides equal
        return eq(L01, L12) && eq(L12, L23) && eq(L23, L30);
    }
};

#endif
