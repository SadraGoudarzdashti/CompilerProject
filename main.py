from antlr4 import *

from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaParserLabeledListener import JavaParserLabeledListener
from gen.JavaLexer import JavaLexer

import os

no_classes = 0                       # Number of classes
no_class_public_attribute = dict()   # Number of each class(package.class) public attribute
no_class_private_attribute = dict()  # Number of each class(package.class) private attribute
no_class_protected_attribute = dict()  # Number of each class protected(package.class) attribute
class_package = dict()               # key: class_name, value: package_name
classes_access = dict()              # key: (package, class), value: accessed class(package, class)


class FirstListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_name = str()
        self.package_name = ''

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        global no_classes
        no_classes += 1
        self.class_name = ctx.IDENTIFIER().getText()
        class_package[self.class_name] = self.package_name
        no_class_public_attribute[(self.package_name, self.class_name)] = 0
        no_class_private_attribute[(self.package_name, self.class_name)] = 0
        no_class_protected_attribute[(self.package_name, self.class_name)] = 0

    def exitFieldDeclaration(self, ctx: JavaParserLabeled.FieldDeclarationContext):
        try:
            if ctx.parentCtx.parentCtx.modifier(0).getText() == 'public':
                no_class_public_attribute[(self.package_name, self.class_name)] += 1

            if ctx.parentCtx.parentCtx.modifier(0).getText() == 'private':
                no_class_private_attribute[(self.package_name, self.class_name)] += 1

            if ctx.parentCtx.parentCtx.modifier(0).getText() == 'protected':
                no_class_protected_attribute[(self.package_name, self.class_name)] += 1
        except:
            pass


class SecondListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_name = str()
        self.package_name = ''
        self.imported = set()

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name = ctx.IDENTIFIER().getText()
        classes_access[(self.package_name, self.class_name)] = {}

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        self.imported.add(ctx.qualifiedName().getText())

    def exitLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        try:
            instance_class = ctx.variableDeclarators().variableDeclarator(0) \
                .variableInitializer().expression().creator() \
                .createdName().getText()
            for source_class, source_package in class_package.items():
                if ((self.package_name == source_package or source_package in self.imported) \
                    and instance_class == source_class) or \
                        (instance_class == source_package + '.' + source_class):

                    classes_access[(self.package_name, self.class_name)] = {(source_package, source_class)}
        except:
            pass


def main():
    for root, dirs, files in os.walk('C:\\Users\\novin\\Desktop\\java'):
        for file in files:
            if file.endswith('.java'):
                stream = FileStream(os.path.join(root, file), encoding='utf8')
                lexer = JavaLexer(stream)
                token_stream = CommonTokenStream(lexer)
                parser = JavaParserLabeled(token_stream)
                listener = FirstListener()
                tree = parser.compilationUnit()
                walker = ParseTreeWalker()
                walker.walk(t=tree, listener=listener)

    for root, dirs, files in os.walk('C:\\Users\\novin\\Desktop\\java'):
        for file in files:
            if file.endswith('.java'):
                stream = FileStream(os.path.join(root, file), encoding='utf8')
                lexer = JavaLexer(stream)
                token_stream = CommonTokenStream(lexer)
                parser = JavaParserLabeled(token_stream)
                listener = SecondListener()
                tree = parser.compilationUnit()
                walker = ParseTreeWalker()
                walker.walk(t=tree, listener=listener)

    global no_classes
    # print(no_classes)
    # print(no_class_public_attribute)
    # print(no_class_private_attribute)
    # print(no_class_protected_attribute)
    # print(classes_access)
    # print(class_package)
    print('---------------------------- NUMBER OF CLASSES : ', no_classes, ' ---------------------------')
    print("---------------------------- NUMBER OF ATTRIBUTES ------------------------------")
    print("++++++ PUBLIC ATTRS ++++++")
    for package_and_class_name, no in no_class_public_attribute.items():
        print(package_and_class_name[0] + '.' + package_and_class_name[1], ':', no)

    print("\n++++++ PRIVATE ATTRS ++++++")
    for package_and_class_name, no in no_class_private_attribute.items():
        print(package_and_class_name[0] + '.' + package_and_class_name[1], ':', no)

    print("\n++++++ PROTECTED ATTRS ++++++")
    for package_and_class_name, no in no_class_protected_attribute.items():
        print(package_and_class_name[0] + '.' + package_and_class_name[1], ':', no)

    print("\n------------------------ NUMBER OF CLASSES ACCESSED BY EACH CLASS --------------------------")
    for class_name, package_name in class_package.items():
        i = 0
        for _, cp in classes_access.items():
            if (package_name, class_name) in cp:
                i += 1
        print(class_name + '.' + package_name, 'accessed by ', i, ' classes.')

    print("\n------------------------ NUMBER OF CLASSES EACH CLASS ACCESS --------------------------")
    for class_and_package_name, accessed in classes_access.items():
        print(class_and_package_name[0] + '.' + class_and_package_name[1], ':', len(accessed))




if __name__ == '__main__':
    main()
