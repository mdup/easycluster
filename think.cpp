#include <iostream>
#include <chrono>
#include <thread>
#include <cmath>
#include <cassert>

void hardcore_computation(double p, double q) {
    // Your big number crunching work should go here.
    // Instead we calculate some fake result.
    std::this_thread::sleep_for(std::chrono::seconds(2));
    const double result = std::sin(p + 2*q);

    // Output the result.
    std::cout <<
        "{ \"params\":"                    "\n"
        "  { \"p\": " << p << ","          "\n"
        "    \"q\": " << q << " },"        "\n"
        "  \"result\": " << result << " }" "\n";
}

int main(int argc, const char **argv) {
    // Retrieve parameters for this run.
    assert(argc > 2);
    const double p = std::stod(argv[1]);
    const double q = std::stod(argv[2]);

    // Start the computation.
    hardcore_computation(p, q);

    return 0;
}
