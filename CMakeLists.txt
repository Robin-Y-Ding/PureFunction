add_clang_executable(clang-split-function FindFunction.cpp)

target_link_libraries(clang-split-function PRIVATE clangTooling)
