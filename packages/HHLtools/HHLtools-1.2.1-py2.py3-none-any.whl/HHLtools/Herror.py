import sys, types, traceback
def error(err, info):
    try:
        raise err(info)
    except:
        ei = sys.exc_info()
        back_frame = ei[2].tb_frame.f_back.f_back
        back_tb = types.TracebackType(tb_next=None,
                                      tb_frame=back_frame,
                                      tb_lasti=back_frame.f_lasti,
                                      tb_lineno=back_frame.f_lineno)
        traceback.print_exception(ei[0], ei[1], tb=back_tb)
        sys.exit(1)

class DimensionError(Exception):
    pass

class IndexOutOfBoundError(Exception):
    pass