import os
import unittest
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import servertools


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'No Scsynth on Travis-CI')
class Test(unittest.TestCase):

    def setUp(self):
        self.server = servertools.Server().boot()

    def tearDown(self):
        self.server.quit()

    def test_01(self):

        synth_a = servertools.Synth(synthdefs.test)
        synth_b = servertools.Synth(synthdefs.test)
        synth_c = servertools.Synth(synthdefs.test)
        synth_d = servertools.Synth(synthdefs.test)
        synth_e = servertools.Synth(synthdefs.test)

        synth_a.allocate()
        synth_b.allocate()

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 test
                    1000 test
            ''',
            ), server_state

        synth_a.replace_with(synth_c)

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 test
                    1002 test
            ''',
            ), server_state

        synth_b.replace_with([synth_d, synth_e])

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1003 test
                    1004 test
                    1002 test
            ''',
            ), server_state

        synth_c.replace_with([synth_a, synth_e])

        server_state = str(self.server.query_remote_nodes())
        assert systemtools.TestManager.compare(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1003 test
                    1005 test
                    1004 test
            ''',
            ), server_state
