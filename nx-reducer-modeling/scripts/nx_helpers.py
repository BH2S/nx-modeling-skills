
# nx_helpers.py — Utility functions for NX Open modeling scripts
# Import this in your build script and call save_stl() before save.

import NXOpen, NXOpen.UF as UF

def save_stl(stl_path, body=None):
    """
    Export the current work part body to STL.
    Call BEFORE wp.SaveAs() to save both .prt and .stl.
    If body is None, uses the first body in the work part.
    """
    uf = UF.UFSession.GetUFSession()
    wp = NXOpen.Session.GetSession().Parts.Work
    if not wp:
        print("STL ERROR: No work part")
        return False

    if body is None:
        bodies = list(wp.Bodies)
        if not bodies:
            print("STL ERROR: No bodies")
            return False
        body = bodies[0]

    import os
    out_dir = os.path.dirname(stl_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    fh = uf.Std.OpenBinaryStlFile(stl_path, False, 'NX Pipeline Export')
    uf.Std.PutSolidInStlFile(fh, 0, body.Tag, 0.0, 0.0, 0.01)
    uf.Std.CloseStlFile(fh)

    if os.path.exists(stl_path):
        print(f"STL exported: {stl_path} ({os.path.getsize(stl_path)} bytes)")
        return True
    print("STL ERROR: file not created")
    return False
