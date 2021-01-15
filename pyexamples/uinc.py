import sys, subprocess
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    misc_input('input', 'I', n_filer=1, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=1, caption="Input"),
    # ======== FIRST LEVEL ========
    # conv0_1x1
    to_Conv("conv0_1x1", 'I', n_filer=1, offset="(1.5,0,0)", to="(input-east)", height=64, depth=64, width=1, caption="1x1 Conv."),
    to_connection("input", "conv0_1x1"),

    # rn_0
    to_ConvRes("rn_0", 'I', n_filer=1, offset="(1.5,0,0)", to="(conv0_1x1-east)", height=64, depth=64, width=1, caption="ResNet"),
    to_connection("conv0_1x1", "rn_0"),
    # ri_0
    to_ConvResInc("ri_0", 'I', n_filer=1, offset="(1.5,0,0)", to="(rn_0-east)", height=64, depth=64, width=1, caption="ResInc"),
    to_connection("rn_0", "ri_0"),

    # ======== SECOND LEVEL ========
    # ds_0
    to_Conv("ds_0", '', 2, offset="(4,0,0)", to="(ri_0-east)", height=32, depth=32, width=2, caption="Down Conv.+ResInc"),
    to_connection("ri_0", "ds_0"),
    # ri_1
    to_ConvResInc("ri_1", 'I/2', 2, offset="(0,0,0)", to="(ds_0-east)", height=32, depth=32, width=2),

    # ======== THIRD LEVEL ========
    # ds_1
    to_Conv("ds_1", '', 4, offset="(1.5,0,0)", to="(ri_1-east)", height=16, depth=16, width=4, caption="Down Conv.+ ResInc"),
    to_connection("ri_1", "ds_1"),

    # ri_2
    to_ConvResInc("ri_2", 'I/4', 4, offset="(0,0,0)", to="(ds_1-east)", height=16, depth=16, width=4),

    # ======== FOURTH LEVEL ========
    # ds_2
    to_Conv("ds_2", '', 8, offset="(1.5,0,0)", to="(ri_2-east)", height=8, depth=8, width=8, caption="Down Conv. + ResInc"),
    to_connection("ri_2", "ds_2"),

    # ri_3
    to_ConvResInc("ri_3", 'I/8', 8, offset="(0,0,0)", to="(ds_2-east)", height=8, depth=8, width=8),

    # ======== FIFTH LEVEL (bottom) ========
    # ds_3
    to_Conv("ds_3", 'I/16', 16, offset="(1.25,0,0)", to="(ri_3-east)", height=4, depth=4, width=16, caption="Down Conv."),
    to_connection("ri_3", "ds_3"),

    # ri_4
    to_ConvResInc("ri_4", 'I/16', 16, offset="(1.25,0,0)", to="(ds_3-east)", height=4, depth=4, width=16, caption="ResInc"),
    to_connection("ds_3", "ri_4"),

    # ======== FOURTH LEVEL ========
    # us_3
    to_Copy("us_3_pt1", 'I/8', 8, offset="(1.5,0,0)", to="(ri_4-east)", height=8, depth=8, width=8, caption="Copy + Up Conv."),
    to_connection("ri_4", "us_3_pt1"),

    to_skip("ds_2", "us_3_pt1", pos=1.5),
    to_Conv("us_3_pt2", 'I/8', 8, offset="(0,0,0)", to="(us_3_pt1-east)", height=8, depth=8, width=8),
    # ri_5
    to_ConvResInc("ri_5", 'I/8', 8, offset="(1.5,0,0)", to="(us_3_pt2-east)", height=8, depth=8, width=16, caption="ResInc"),
    to_connection("us_3_pt2", "ri_5"),

    # ======== THIRD LEVEL ========
    # us_2
    to_Copy("us_2_pt1", 'I/4', 4, offset="(2,0,0)", to="(ri_5-east)", height=16, depth=16, width=4, caption="Copy + Up Conv."),
    to_connection("ri_5", "us_2_pt1"),
    to_skip("ds_1", "us_2_pt1", pos=1.5),
    to_Conv("us_2_pt2", 'I/4', 4, offset="(0,0,0)", to="(us_2_pt1-east)", height=16, depth=16, width=4),
    # ri_6
    to_ConvResInc("ri_6", 'I/4', 8, offset="(2,0,0)", to="(us_2_pt2-east)", height=16, depth=16, width=8, caption="ResInc"),
    to_connection("us_2_pt2", "ri_6"),

    # ======== SECOND LEVEL ========
    # us_1
    to_Copy("us_1_pt1", 'I/2', 2, offset="(2,0,0)", to="(ri_6-east)", height=32, depth=32, width=2, caption="Copy + Up Conv."),
    to_connection("ri_6", "us_1_pt1"),
    to_skip("ds_0", "us_1_pt1", pos=1.25),
    to_Conv("us_1_pt2", 'I/2', 2, offset="(0,0,0)", to="(us_1_pt1-east)", height=32, depth=32, width=2),

    # ri_7
    to_ConvResInc("ri_7", 'I/2', 2, offset="(2,0,0)", to="(us_1_pt2-east)", height=32, depth=32, width=4, caption="ResInc"),
    to_connection("us_1_pt2", "ri_7"),

    # ======== FIRST LEVEL ========
    # us_0
    to_Copy("us_0_pt1", 'I', 1, offset="(2.2,0,0)", to="(ri_7-east)", height=64, depth=64, width=1, caption="Copy+Conv."),
    to_connection("ri_7", "us_0_pt1"),
    to_skip("ri_0", "us_0_pt1", pos=1.1),
    to_Conv("us_0_pt2", 'I', 1, offset="(0,0,0)", to="(us_0_pt1-east)", height=64, depth=64, width=1),
    # ri_8
    to_ConvResInc("ri_8", 'I', 2, offset="(2.2,0,0)", to="(us_0_pt2-east)", height=64, depth=64, width=2, caption="ResInc"),
    to_connection("us_0_pt2", "ri_8"),

    # conv9_1x1
    to_ConvWest("conv9_1x1", 'I', 1, offset="(2.2,0,0)", to="(ri_8-east)", height=64, depth=64, width=1, caption= "Conv.+Copy"),
    to_connection("ri_8", "conv9_1x1"),

    to_CopyEast("us_0_pt1", 'I', 1, offset="(0,0,0)", to="(conv9_1x1-east)", height=64, depth=64, width=1),
    to_skip("rn_0", "us_0_pt1", pos=1.25),

    # rn_10
    to_ConvRes("rn_10", 'I', n_filer=2, offset="(2.2,0,0)", to="(conv9_1x1-east)", height=64, depth=64, width=2, caption="ResNet"),
    to_connection("us_0_pt1", "rn_10"),

    # dropout

    to_Conv("dropout", 'I', 1, offset="(2.2,0,0)", to="(rn_10-east)", height=64, depth=64, width=1, caption="Dropout"),
    to_connection("rn_10", "dropout"),

    misc_input('output', '', n_filer=1, offset="(2.2,0,0)", to="(dropout-east)", height=64, depth=64, width=1, caption="Output"),
    to_connection("dropout", "output"),

    to_end()
    ]

def main():
    namefile = os.path.splitext(sys.argv[0])[0]
    to_generate(arch, namefile + '.tex' )
    pdflatex_exe = 'pdflatex'
    if os.name == 'nt':
        pdflatex_exe+'.exe'
    subprocess.Popen(pdflatex_exe + ' ' + namefile + '.tex', shell=True).wait()

if __name__ == '__main__':
    main()
