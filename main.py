from antlr4 import *

from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaParserLabeledListener import JavaParserLabeledListener
from gen.JavaLexer import JavaLexer

import os

no_classes = 0  # Number of classes
no_class_public_attribute = dict()  # Number of each class public attribute
no_class_private_attribute = dict()  # Number of each class private attribute
no_class_protected_attribute = dict()  # Number of each class protected attribute


class MyListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_name = str()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        global no_classes
        no_classes += 1
        self.class_name = ctx.IDENTIFIER().getText()

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        try:
            if ctx.parentCtx.parentCtx.modifier(0).getText() == 'public':
                no_class_public_attribute[self.class_name] = \
                    no_class_public_attribute.get(self.class_name, 0) + 1

            if ctx.parentCtx.parentCtx.modifier(0).getText() == 'private':
                no_class_private_attribute[self.class_name] = \
                    no_class_private_attribute.get(self.class_name, 0) + 1

            if ctx.parentCtx.parentCtx.modifier(0).getText() == 'protected':
                no_class_protected_attribute[self.class_name] = \
                    no_class_protected_attribute.get(self.class_name, 0) + 1
        except:
            pass

def main():
    for root, dirs, files in os.walk('test_project'):
        for file in files:
            if file.endswith('.java'):
                stream = FileStream(os.path.join(root, file), encoding='utf8')
                lexer = JavaLexer(stream)
                token_stream = CommonTokenStream(lexer)
                parser = JavaParserLabeled(token_stream)
                listener = MyListener()
                tree = parser.compilationUnit()
                walker = ParseTreeWalker()
                walker.walk(t=tree, listener=listener)

    global no_classes
    print(no_classes)
    print(no_class_public_attribute)
    print(no_class_private_attribute)
    print(no_class_protected_attribute)
if __name__ == '__main__':
    main()
