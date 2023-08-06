// Implements 'associate' from indexing.py as a torch C++ extension.

#include <torch/extension.h>

#include <iostream>

// torch::Tensor associate(
//     const torch::Tensor& query_timestamps,
//     const torch::Tensor& target_timestamps,
// )

/*
    Idea: get interp1d result and apply resulting local offsets to slerp poses.

*/