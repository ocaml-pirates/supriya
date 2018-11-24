import supriya.synthdefs
import supriya.ugens


def test_SynthDefCompiler_rngs_01():

    sc_synthdef = supriya.synthdefs.SuperColliderSynthDef(
        'seedednoise',
        r"""
        arg rand_id=0, seed=0;
        RandID.ir(rand_id);
        RandSeed.ir(1, seed);
        Out.ar(0, WhiteNoise.ar());
        """
        )
    sc_compiled_synthdef = sc_synthdef.compile()

    with supriya.synthdefs.SynthDefBuilder(rand_id=0, seed=0) as builder:
        supriya.ugens.RandID.ir(rand_id=builder['rand_id'])
        supriya.ugens.RandSeed.ir(seed=builder['seed'], trigger=1)
        source = supriya.ugens.WhiteNoise.ar()
        supriya.ugens.Out.ar(bus=0, source=source)
    py_synthdef = builder.build('seedednoise')
    py_compiled_synthdef = py_synthdef.compile()

    # fmt: off
    test_compiled_synthdef = bytes(
        b'SCgf'
        b'\x00\x00\x00\x02'
        b'\x00\x01'
            b'\x0bseedednoise'
                b'\x00\x00\x00\x02'
                    b'?\x80\x00\x00'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x02'
                    b'\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x02'
                    b'\x07rand_id'
                    b'\x00\x00\x00\x00'
                    b'\x04seed'
                    b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x05'
                    b'\x07Control'
                        b'\x01'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00'
                            b'\x01'
                            b'\x01'
                    b'\x06RandID'
                        b'\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00'
                    b'\x08RandSeed'
                        b'\x00'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x00'
                            b'\x00\x00\x00\x01'
                            b'\x00'
                    b'\nWhiteNoise'
                        b'\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01'
                        b'\x00\x00'
                            b'\x02'
                    b'\x03Out'
                        b'\x02'
                        b'\x00\x00\x00\x02'
                        b'\x00\x00\x00\x00'
                        b'\x00\x00'
                            b'\xff\xff\xff\xff'
                            b'\x00\x00\x00\x01'
                            b'\x00\x00\x00\x03'
                            b'\x00\x00\x00\x00'
                b'\x00\x00'
        )
    # fmt: on

    assert sc_compiled_synthdef == test_compiled_synthdef
    assert py_compiled_synthdef == test_compiled_synthdef
