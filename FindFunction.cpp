/**
 * @author Yangruibo Ding
 * @author Saikat Chakraborty
**/
#include <stdio.h>

#include <iostream>

#include "llvm/Support/Host.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Frontend/FrontendAction.h"
#include "clang/Tooling/Tooling.h"
#include "clang/StaticAnalyzer/Frontend/FrontendActions.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Basic/SourceLocation.h"
#include "llvm/ADT/StringRef.h"
#include "clang/Basic/LangOptions.h"
#include "clang/Basic/SourceManager.h"
#include <iostream>
using namespace clang;
using namespace clang::driver;
using namespace clang::tooling;
using namespace llvm;
static cl::OptionCategory FindFunc("split-source options");

class FindFuncVisitor
        : public RecursiveASTVisitor<FindFuncVisitor> {

clang::SourceManager &SourceManager;


public:
  FindFuncVisitor(clang::SourceManager &SourceManager)
      : SourceManager(SourceManager) {}

  bool VisitFunctionDecl(const FunctionDecl *fd) {
    

    if (fd->hasBody(fd))
    {
        SourceLocation begin = fd->getSourceRange().getBegin();
        if (!SourceManager.isInSystemHeader(begin))
        {
            SourceRange sr = fd->getSourceRange();
            PresumedLoc begin = SourceManager.getPresumedLoc(sr.getBegin());
            PresumedLoc end = SourceManager.getPresumedLoc(sr.getEnd());

            std::cout << "{'function': '" << fd->getDeclName().getAsString() << "'"
            << ", 'file': '" << begin.getFilename() << "'"
            << ", 'begin': [" << begin.getLine() << ", " << begin.getColumn() << "]"
            << ", 'end': [" << end.getLine() << ", " << end.getColumn() << "]"
            << "}" << "\n";
        }
    }

    return true;
}

};

class FindFuncConsumer : public clang::ASTConsumer {
public:
    explicit FindFuncConsumer(clang::SourceManager &SM)
            : Visitor(SM) {}

    virtual void HandleTranslationUnit(clang::ASTContext &Context) {
        Visitor.TraverseDecl(Context.getTranslationUnitDecl());
    }
private:
    FindFuncVisitor Visitor;
};


class FindFuncAction : public clang::ASTFrontendAction {
public:
    virtual std::unique_ptr<clang::ASTConsumer> CreateASTConsumer(
            clang::CompilerInstance &Compiler, llvm::StringRef InFile) {
        return std::unique_ptr<clang::ASTConsumer>(
                new FindFuncConsumer(Compiler.getSourceManager()));
    }
};


int main(int argc, const char **argv) {
    CommonOptionsParser OptionsParser(argc, argv, FindFunc);
    ClangTool Tool(OptionsParser.getCompilations(),
                   OptionsParser.getSourcePathList());
    return Tool.run(newFrontendActionFactory<FindFuncAction>().get());

}
