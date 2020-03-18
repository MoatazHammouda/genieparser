import unittest
from unittest.mock import Mock

# pyATS
from pyats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.parser.asa.show_asp_drop import ShowAspDrop


# ============================================
# unit test for 'show asp drop'
# =============================================
class TestShowAspDrop(unittest.TestCase):
    """    unit test for
            * show asp drop
    """
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    # show asp drop
    golden_output = {'execute.return_value': '''
    Frame drop:
      Reverse-path verify failed (rpf-violated)                                   23
      Flow is denied by configured rule (acl-drop)                                29
      Slowpath security checks failed (sp-security-failed)                        11
      FP L2 rule drop (l2_acl)                                                    35
      FP no mcast output intrf (no-mcast-intrf)                                   31
    
    Last clearing: 10:43:33 EDT Mar 27 2019 by genie
    
    Flow drop:
    
    Last clearing: 10:43:33 EDT Mar 27 2019 by genie    
    '''}

    golden_parsed_output = {
        'flow_drop': {
            'last_clearing': '10:43:33 EDT Mar 27 2019 by genie',
        },
        'frame_drop': {
            'last_clearing': '10:43:33 EDT Mar 27 2019 by genie',
            'acl-drop': {
                'counts': 29,
            },
            'l2_acl': {
                'counts': 35,
            },
            'no-mcast-intrf': {
                'counts': 31,
            },
            'rpf-violated': {
                'counts': 23,
            },
            'sp-security-failed': {
                'counts': 11,
            },
        },
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowAspDrop(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        obj_context = ShowAspDrop(device=self.device)
        parsed_output = obj_context.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


if __name__ == '__main__':
    unittest.main()