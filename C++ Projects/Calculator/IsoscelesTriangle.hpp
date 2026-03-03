#ifndef ISOSCELES_TRIANGLE_HPP
#define ISOSCELES_TRIANGLE_HPP

#include "Triangle.hpp"

class IsoscelesTriangle : public Triangle {
public:
    // Validates an isosceles triangle: must satisfy triangle inequality
    // AND at least two sides must be equal
    bool validate() const override {
        double a = dist(vertices[0], vertices[1]);
        double b = dist(vertices[1], vertices[2]);
        double c = dist(vertices[2], vertices[0]);

        if (!triangleInequality(a, b, c)) {
            return false;
        }

        return eq(a, b) || eq(b, c) || eq(a, c);
    }
};

#endif
