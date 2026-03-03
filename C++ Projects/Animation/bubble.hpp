/* CSCI 200: A4 – Bubbles
 * Author: Genevieve (Varka) Carter
 * Date: November 11th, 2025
 *
 * Description:
 *   Header for the Bubble class. Defines the bubble’s shape, movement, and
 *   click-detection behavior for the bubble-popping game.
 */

#ifndef BUBBLE_HPP
#define BUBBLE_HPP

#include <SFML/Graphics.hpp>

class Bubble {
private:
    sf::CircleShape circle;
    float xDir;
    float yDir;

public:
    Bubble(float radius, const sf::Vector2f &pos, const sf::Color &color, float xVel, float yVel);

    void draw(sf::RenderWindow &window) const;
    void updatePosition(float windowWidth, float windowHeight);
    bool checkClicked(const float mouseX, const float mouseY) const;

    sf::Vector2f getPosition() const { return circle.getPosition(); }
    float getRadius() const { return circle.getRadius(); }
};

#endif
