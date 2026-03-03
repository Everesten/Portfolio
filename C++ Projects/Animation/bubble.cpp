/* CSCI 200: A4 – Bubbles
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 * Date: November 11th, 2025
 *
 * Description:
 *   Implements the Bubble class. Handles drawing, motion, and click detection
 *   for each bubble in the bubble-popping game.
 */

#include "bubble.hpp"
#include <cmath>
#include <algorithm>  // for std::max, std::min

Bubble::Bubble(float radius, const sf::Vector2f &pos, const sf::Color &color, float xVel, float yVel)
    : xDir(xVel), yDir(yVel)
{
    circle.setRadius(radius);
    circle.setFillColor(color);
    circle.setPosition(pos);
}

void Bubble::draw(sf::RenderWindow &window) const {
    window.draw(circle);
}

void Bubble::updatePosition(float windowWidth, float windowHeight) {
    sf::Vector2f pos = circle.getPosition();
    pos.x += xDir;
    pos.y += yDir;

    const float r = circle.getRadius();

    // Bounce on left/right edges
    if (pos.x < 0 || pos.x + 2 * r > windowWidth) {
        xDir = -xDir;
        pos.x = std::max(0.f, std::min(pos.x, windowWidth - 2 * r));
    }

    // Bounce on top/bottom edges
    if (pos.y < 0 || pos.y + 2 * r > windowHeight) {
        yDir = -yDir;
        pos.y = std::max(0.f, std::min(pos.y, windowHeight - 2 * r));
    }

    circle.setPosition(pos);
}

bool Bubble::checkClicked(float mouseX, float mouseY) const {
    sf::Vector2f center = circle.getPosition() + sf::Vector2f(circle.getRadius(), circle.getRadius());
    float dx = mouseX - center.x;
    float dy = mouseY - center.y;
    return std::sqrt(dx * dx + dy * dy) <= circle.getRadius();
}
