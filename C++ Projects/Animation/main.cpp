/* CSCI 200: A4 – Bubbles
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 * Date: November 11th, 2025
 *
 * Description:
 *   A bubble-popping game where you spawn and click bubbles for points.
 *   Pop as many as you can in 10 seconds, restart to try again, or press Q to quit.
 *
 * Resources used:
 *   SFML 3 documentation
 */

#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

#include <SFML/Graphics.hpp>

#include "bubble.hpp"

float randFloat(const float min, const float max, std::mt19937 &rng) {
    std::uniform_real_distribution<float> dist(min, max);
    return dist(rng);
}

int main() {
    // create a window
    const unsigned WIDTH = 640, HEIGHT = 640;
    sf::Vector2u windowSize(640, 640);
    sf::RenderWindow window(sf::VideoMode(windowSize), "A4: Bubbles");

    /////////////////////////////////////
    // BEGIN ANY FILE LOADING

    std::mt19937 rng(std::random_device{}());
    std::vector<Bubble> bubbles;

    auto makeRandomBubble = [&](void) {
        float radius = randFloat(10, 50, rng);
        float x = randFloat(radius, WIDTH - radius, rng);
        float y = randFloat(radius, HEIGHT - radius, rng);
        sf::Color color(
            static_cast<uint8_t>(randFloat(0, 255, rng)),
            static_cast<uint8_t>(randFloat(0, 255, rng)),
            static_cast<uint8_t>(randFloat(0, 255, rng))
        );
        float xVel = static_cast<float>(randFloat(-0.8f, 0.8f, rng));
        float yVel = static_cast<float>(randFloat(-0.8f, 0.8f, rng));
        return Bubble(radius, {x, y}, color, xVel, yVel);
    };

    for (int i = 0; i < 5; ++i)
        bubbles.push_back(makeRandomBubble());

    // HUD setup
    sf::Font font;
    if (!font.openFromFile("data/arial.ttf")) { 
        std::cout << "ERROR: Failed to load font arial.ttf";
    }

    int score = 0;
    float timeRemaining = 10.f;
    sf::Clock clock; // measure elapsed seconds each frame

    sf::Text scoreText(font);
    scoreText.setString("Score: 0");
    scoreText.setCharacterSize(20);
    scoreText.setPosition({10.f, 10.f});

    sf::Text timerText(font);
    timerText.setString("Time: 10");
    timerText.setCharacterSize(20);
    timerText.setPosition({10.f, 40.f});

    sf::Text countText(font);
    countText.setString("Bubbles: 5");
    countText.setCharacterSize(20);
    countText.setPosition({10.f, 70.f});

    //  END  ANY FILE LOADING
    /////////////////////////////////////

    // while the window is open
    while (window.isOpen()) {

        /////////////////////////////////////
        // BEGIN EVENT HANDLING HERE

        while (const std::optional event = window.pollEvent()) {
            // Close window
            if (event->is<sf::Event::Closed>()) {
                window.close();
            }
            // Key pressed
            else if (event->is<sf::Event::KeyPressed>()) {
                auto key = event->getIf<sf::Event::KeyPressed>();

                if (key->scancode == sf::Keyboard::Scan::Q || key->scancode == sf::Keyboard::Scan::Escape)
                    window.close();

                // Restart game
                else if (key->scancode == sf::Keyboard::Scan::R) {
                    bubbles.clear();
                    for (int i = 0; i < 5; ++i)
                        bubbles.push_back(makeRandomBubble());
                    score = 0;
                    timeRemaining = 10.f;
                    clock.restart();
                }

                // Add bubble
                else if (key->scancode == sf::Keyboard::Scan::Space && bubbles.size() < 10 && timeRemaining > 0.f)
                    bubbles.push_back(makeRandomBubble());
            }

            // Mouse pressed
            else if (event->is<sf::Event::MouseButtonPressed>()) {
                auto click = event->getIf<sf::Event::MouseButtonPressed>();
                if (click->button == sf::Mouse::Button::Left && timeRemaining > 0.f) {
                    float mx = static_cast<float>(click->position.x);
                    float my = static_cast<float>(click->position.y);
                    auto before = bubbles.size();
                    bubbles.erase(
                        std::remove_if(bubbles.begin(), bubbles.end(),
                            [&](const Bubble &b) { return b.checkClicked(mx, my); }),
                        bubbles.end()
                    );
                    score += static_cast<int>(before - bubbles.size());
                }
            }
        }

        //  END  EVENT HANDLING HERE
        /////////////////////////////////////

        /////////////////////////////////////
        // BEGIN ANIMATION UPDATING HERE

        if (timeRemaining > 0.f) {
            float dt = clock.restart().asSeconds();
            timeRemaining -= dt;
            if (timeRemaining < 0.f) timeRemaining = 0.f;

            for (auto &b : bubbles)
                b.updatePosition(WIDTH, HEIGHT);
        }

        // Update HUD text
        scoreText.setString("Score: " + std::to_string(score));
        timerText.setString("Time: " + std::to_string(static_cast<int>(timeRemaining)));
        countText.setString("Bubbles: " + std::to_string(bubbles.size()));

        //  END  ANIMATION UPDATING HERE
        /////////////////////////////////////

        /////////////////////////////////////
        // BEGIN DRAWING HERE

        window.clear(sf::Color::Black);

        for (const auto &b : bubbles)
            b.draw(window);

        window.draw(scoreText);
        window.draw(timerText);
        window.draw(countText);

        //  END  DRAWING HERE
        /////////////////////////////////////

        // display the current contents of the window
        window.display();
    }

    return 0;
}