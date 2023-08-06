#include <iostream>

int main(int argc, char** argv) {
    // Read indefinitely from stdin until EOF
    while (std::cin) {
        std::string line;
        std::getline(std::cin, line);
        std::cout << "{\"command\": \"TURN\", \"direction\": \"NORTH\"}" << std::endl;
    }
}
