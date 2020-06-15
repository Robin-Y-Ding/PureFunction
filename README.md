# PureFunction
Extract functions as separate files from c/c++ files

## Usage

### Step-1: clang installation
Install `clang` from the instructions [here](http://clang.llvm.org/get_started.html)

### Step-2: Integrate `FindFunction.cpp` into clang as a tool
Create a new folder `clang-split-function` inside folder `llvm-project/clang/tools/`
and put the provided `CMakeLists.txt` and `FindFunction.cpp` in the new
folder. Edit `llvm-project/clang/tools/CMakeLists.txt` and add the fol-
lowing content into the file.
```bash
add_clang_subdirectory(clang-split-function)
```

Return to the `llvm-project/build` folder and run `make`. After it fin-
ishes, you can test the example tool by running the following command.
```bash
clang-split-function anyfile.c/cpp
```

### Step-3: Run `splitFunctions.py`
```bash
python3 splitFunctions.py <source_file_dir>
```
The output of `splitFunctions.py` is a json file containing the path for all available functions. 

## Referred links:
1. Clang Tutorial: Finding declarations. https://xinhuang.github.io/posts/2014-10-19-clang-tutorial-finding-declarations.html
2. clang-tutorial. https://github.com/loarabia/Clang-tutorial
3. How to write RecursiveASTVisitor based ASTFrontendActions. https://clang.llvm.org/docs/RAVFrontendAction.html
