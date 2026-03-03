#ifndef EQUILATERAL_TRIANGLE_HPP
#define EQUILATERAL_TRIANGLE_HPP

#include "Triangle.hpp"

class EquilateralTriangle : public Triangle {
public:
    // Validates an equilateral triangle: all sides must be equal and satisfy triangle inequality
    bool validate() const override {
        double a = dist(vertices[0], vertices[1]);
        double b = dist(vertices[1], vertices[2]);
        double c = dist(vertices[2], vertices[0]);

        if (!triangleInequality(a, b, c)) {
            return false;
        }

        return eq(a, b) && eq(b, c);
    }
};

#endif
