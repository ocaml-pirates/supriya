from supriya.tools import nonrealtimetools
from supriya.tools import synthdeftools
from supriya.tools import ugentools
from nonrealtimetools_testbase import TestCase


class TestCase(TestCase):

    with synthdeftools.SynthDefBuilder() as builder:
        source = ugentools.WhiteNoise.ar()
        ugentools.Out.ar(bus=0, source=source)
    nonrepeatable_noise_synthdef = builder.build()

    with synthdeftools.SynthDefBuilder(rand_id=0, rand_seed=0) as builder:
        ugentools.RandID.ir(rand_id=builder['rand_id'])
        ugentools.RandSeed.ir(seed=builder['rand_seed'], trigger=1)
        source = ugentools.WhiteNoise.ar()
        ugentools.Out.ar(bus=0, source=source)
    repeatable_noise_synthdef = builder.build()

    with synthdeftools.SynthDefBuilder(rand_id=0, rand_seed=0) as builder:
        ugentools.RandID.ir(rand_id=builder['rand_id'])
        ugentools.RandSeed.ir(seed=builder['rand_seed'], trigger=1)
    seed_synthdef = builder.build()

    with synthdeftools.SynthDefBuilder(rand_id=0) as builder:
        ugentools.RandID.ir(rand_id=builder['rand_id'])
        source = ugentools.WhiteNoise.ar()
        ugentools.Out.ar(bus=0, source=source)
    maybe_repeatable_noise_synthdef = builder.build()

    def test_nonrepeatable(self):
        session = nonrealtimetools.Session(0, 1)
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.nonrepeatable_noise_synthdef,
                )
        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
        sampled_session = self._sample(output_file_path)
        for _ in range(10):
            output_file_path.unlink()
            exit_code, output_file_path = session.render()
            self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
            assert self._sample(output_file_path) != sampled_session

    def test_repeatable(self):
        session = nonrealtimetools.Session(0, 1)
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.repeatable_noise_synthdef,
                )
        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
        sampled_session = self._sample(output_file_path)
        for _ in range(10):
            output_file_path.unlink()
            exit_code, output_file_path = session.render()
            self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
            assert self._sample(output_file_path) == sampled_session

    def test_maybe_repeatable_but_wasnt(self):
        """
        Setting a RandID isn't enough. The RNG will be initialized randomly.
        """
        session = nonrealtimetools.Session(0, 1)
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.maybe_repeatable_noise_synthdef,
                )
        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
        sampled_session = self._sample(output_file_path)
        for _ in range(10):
            output_file_path.unlink()
            exit_code, output_file_path = session.render()
            self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
            assert self._sample(output_file_path) != sampled_session

    def test_maybe_repeatable_and_was(self):
        """
        Setting a RandID and seeding it in another synth locks us in.
        """
        session = nonrealtimetools.Session(0, 1)
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.maybe_repeatable_noise_synthdef,
                )
            session.add_synth(
                add_action='ADD_TO_HEAD',
                duration=0,
                synthdef=self.seed_synthdef,
                )
        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
        sampled_session = self._sample(output_file_path)
        for _ in range(10):
            output_file_path.unlink()
            exit_code, output_file_path = session.render()
            self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
            assert self._sample(output_file_path) == sampled_session

    def test_maybe_repeatable_and_almost_was(self):
        """
        Seeding is sensitive to node order.
        """
        session = nonrealtimetools.Session(0, 1)
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.maybe_repeatable_noise_synthdef,
                )
            session.add_synth(
                add_action='ADD_TO_TAIL',
                duration=0,
                synthdef=self.seed_synthdef,
                )
        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
        first_sampled_session = sorted(self._sample(output_file_path).items())
        for _ in range(10):
            output_file_path.unlink()
            exit_code, output_file_path = session.render()
            self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
            sampled_session = sorted(self._sample(output_file_path).items())
            assert first_sampled_session[0] != sampled_session[0]
            assert first_sampled_session[1:] == sampled_session[1:]

    def test_repeatable_via_session_method(self):
        session = nonrealtimetools.Session(0, 1)
        with session.at(0):
            session.add_synth(
                duration=1,
                synthdef=self.maybe_repeatable_noise_synthdef,
                rand_seed=0,
                )
            session.set_rand_seed(rand_id=0, rand_seed=23)
        d_recv_commands = self.build_d_recv_commands([
            session._build_rand_seed_synthdef(),
            self.maybe_repeatable_noise_synthdef,
            ])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/s_new', self.maybe_repeatable_noise_synthdef.anonymous_name,
                    1000, 0, 0,
                    'rand_seed', 0],
                ['/s_new', session._build_rand_seed_synthdef().anonymous_name,
                    1001, 0, 0,
                    'rand_id', 0, 'rand_seed', 23]]],
             [1.0, [['/n_free', 1000], [0]]]]
        exit_code, output_file_path = session.render()
        self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
        sampled_session = self._sample(output_file_path)
        for _ in range(10):
            output_file_path.unlink()
            exit_code, output_file_path = session.render()
            self.assert_ok(exit_code, 1, 44100, 1, file_path=output_file_path)
            assert self._sample(output_file_path) == sampled_session
