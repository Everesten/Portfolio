#ifndef SCALENE_TRIANGLE_HPP
#define SCALENE_TRIANGLE_HPP

#include "Triangle.hpp"

class ScaleneTriangle : public Triangle {
public:
    // Validates a scalene triangle: all sides non-zero, satisfy triangle inequality, all sides different
    bool validate() const override {
        double a = dist(vertices[0], vertices[1]);
        double b = dist(vertices[1], vertices[2]);
        double c = dist(vertices[2], vertices[0]);

        if (!triangleInequality(a, b, c)) {
            return false;
        }

        return neq(a, b) && neq(b, c) && neq(a, c);
    }
};

#endif
