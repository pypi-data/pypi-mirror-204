def Error(err, Opcode, Operand):
    a = ['"LDD 100"\n','import sys, types, traceback\n', 'def error():\n', '    try:\n', '        a\n', '    except:\n', '        ei = sys.exc_info()\n', '        back_frame = ei[2].tb_frame.f_back\n', '        back_tb = types.TracebackType(tb_next=None,\n', '                                      tb_frame=back_frame,\n', '                                      tb_lasti=2,\n', '                                      tb_lineno=10)\n', f"        traceback.print_exception({err}, {err}('guess what error(use trace table:-)'), tb=back_tb)\n", '        sys.exit(1)\n', 'error()\n']
    a[0] = f'"{Opcode} {Operand}"\n'
    with open('objectCode.py', 'w') as f:
        f.writelines(a)
    import Aciembler.objectCode



