# -*- coding: utf-8 -*-

from pycparser import parse_file, c_parser, c_generator


class C99(object):
    pass


class C99Function(Object):

    def __init__(kernel, src_path, func_name):
	self.kernel = kernel
	self.src_path = src_path
	self.func_name = func_name

    def open(self):
        return self

    def __enter__(self):
        pass

    def __exit__(self):
        pass





def translate_to_c(filename):
    """ Simply use the c_generator module to emit a parsed AST.
    """
    ast = parse_file(filename, use_cpp=True)
    generator = c_generator.CGenerator()
    print(generator.visit(ast))


def _zz_test_translate():
    # internal use
    src = r'''

    void f(char * restrict joe){}

int main(void)
{
    unsigned int long k = 4;
    int p = - - k;
    return 0;
}
'''
    parser = c_parser.CParser()
    ast = parser.parse(src)
    ast.show()
    generator = c_generator.CGenerator()

    print(generator.visit(ast))

    # tracing the generator for debugging
    #~ import trace
    #~ tr = trace.Trace(countcallers=1)
    #~ tr.runfunc(generator.visit, ast)
    #~ tr.results().write_results()


if __name__ == "__main__":
    _zz_test_translate()
    if len(sys.argv) > 1:
        translate_to_c(sys.argv[1])
    else:
        print("Please provide a filename as argument")
