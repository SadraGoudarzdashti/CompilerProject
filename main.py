from antlr4 import *

from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaParserLabeledListener import JavaParserLabeledListener
from gen.JavaLexer import JavaLexer

import os

no_classes = 0                       # Number of classes
no_class_public_attribute = dict()   # Number of each class(package.class) public attribute
no_class_private_attribute = dict()  # Number of each class(package.class) private attribute
no_class_protected_attribute = dict()  # Number of each class protected(package.class) attribute
class_package = list()               # list of (class_name, package_name)
package_class_method = list()        # list of (package_name, class_name, method_name)
classes_access = dict()              # key: (package, class), value: accessed class(package, class)
methods_access = dict()              # key: (package, class, method), value: accessed class(package, class, method)


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
        class_package.append((self.class_name, self.package_name))
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
        self.method_name = ''
        self.instances_in_method = dict()  # key:instance_name value:(package, class)

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name = ctx.IDENTIFIER().getText()
        classes_access[(self.package_name, self.class_name)] = set()

    def enterImportDeclaration(self, ctx: JavaParserLabeled.ImportDeclarationContext):
        self.imported.add(ctx.qualifiedName().getText())

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        self.method_name = ctx.IDENTIFIER().getText()
        package_class_method.append((self.package_name, self.class_name, self.method_name))

    def exitLocalVariableDeclaration(self, ctx: JavaParserLabeled.LocalVariableDeclarationContext):
        try:
            instance_class = ctx.variableDeclarators().variableDeclarator(0) \
                .variableInitializer().expression().creator() \
                .createdName().getText()
            for source_class, source_package in class_package:
                if ((self.package_name == source_package or source_package in self.imported) \
                    and instance_class == source_class) or \
                        (instance_class == source_package + '.' + source_class):

                    classes_access[(self.package_name, self.class_name)].add((source_package, source_class))
                    instance_name = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().getText()
                    self.instances_in_method[instance_name] = (source_package, source_class)
                    methods_access[(self.package_name, self.class_name, self.method_name)] = set()
        except:
            pass

    def enterMethodCall0(self, ctx:JavaParserLabeled.MethodCall0Context):
        method_name = ctx.IDENTIFIER().getText()
        obj_name = ctx.parentCtx.expression().getText()
        if obj_name in self.instances_in_method:
            methods_access[(self.package_name, self.class_name, self.method_name)].add(
                (self.instances_in_method[obj_name][0], self.instances_in_method[obj_name][1], method_name))

    def exitMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        self.method_name = ''
        self.instances_in_method = {}

def main():
    for root, dirs, files in os.walk('java'):
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

    for root, dirs, files in os.walk('java'):
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
    for class_name, package_name in class_package:
        i = 0
        for _, pc in classes_access.items():
            if (package_name, class_name) in pc:
                i += 1
        print(package_name + '.' + class_name, 'accessed by ', i, ' classes.')

    print("\n------------------------ NUMBER OF CLASSES EACH CLASS ACCESS --------------------------")
    for class_and_package_name, accessed in classes_access.items():
        print(class_and_package_name[0] + '.' + class_and_package_name[1], ':', len(accessed))

    print("\n------------------------ NUMBER OF METHODS ACCESSED BY EACH METHOD --------------------------")
    for package_name, class_name, method_name in package_class_method:
        i = 0
        for _, pcm in methods_access.items():
            if (package_name, class_name, method_name) in pcm:
                i += 1
        print(package_name + '.' + class_name + '.' + method_name, 'accessed by ', i, ' methods.')

    print("\n------------------------ NUMBER OF METHODS EACH METHOD ACCESS --------------------------")
    for pcm, accessed in methods_access.items():
        print(pcm[0] + '.' + pcm[1] + '.' + pcm[2], ':', len(accessed))


if __name__ == '__main__':
    main()
