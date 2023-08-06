"JMP 300"
import sys, types, traceback
def error():
    try:
        a
    except:
        ei = sys.exc_info()
        back_frame = ei[2].tb_frame.f_back
        back_tb = types.TracebackType(tb_next=None,
                                      tb_frame=back_frame,
                                      tb_lasti=2,
                                      tb_lineno=10)
        traceback.print_exception(SyntaxError, SyntaxError('guess what error(use trace table:-)'), tb=back_tb)
        sys.exit(1)
error()
