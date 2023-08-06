#pragma once

#include <vector>

namespace bamboo {
template <typename Session_t, typename T>
class SofieEvaluator {
    using input_t = std::vector<T>;
    using output_t = std::vector<T>;

    public:
        SofieEvaluator(unsigned int nSlots=0, const std::string& weightsFile="") {
            if (nSlots < 1) nSlots = 1;
            for (unsigned int i = 0; i < nSlots; ++i) {
                sessions_.emplace_back(weightsFile);
            }
        }
        ~SofieEvaluator() noexcept = default;

        output_t evaluate(unsigned int slot, input_t& input) {
            return sessions_[slot].infer(input.data());
        }

    private:
        std::vector<Session_t> sessions_;
};
}
