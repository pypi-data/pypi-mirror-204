import unittest

import tzconv as m


class TestMatchTimeZone(unittest.TestCase):
    def test_different_pattern_is_not_matched(self):
        self.assertFalse(m.match_time_zone("foo", "asdf"))
        self.assertFalse(m.match_time_zone("foo/baz", "foo/bar"))

    def test_match_is_case_insensitive(self):
        self.assertTrue(m.match_time_zone("fOO", "Foo"))
        self.assertTrue(m.match_time_zone("Foo/bAR", "Foo/Bar"))

    def test_prefix_pattern_matches_name(self):
        self.assertTrue(m.match_time_zone("foo", "foobar"))
        self.assertTrue(m.match_time_zone("foo", "foo/bar"))
        self.assertTrue(m.match_time_zone("foo", "foob/ar"))
        self.assertTrue(m.match_time_zone("foo/b", "foo/bar"))

    def test_initials_pattern_match_name(self):
        self.assertTrue(m.match_time_zone("f", "foobar"))
        self.assertTrue(m.match_time_zone("f/b", "foo/bar"))
        self.assertTrue(m.match_time_zone("f/bb", "foo/bar_baz"))

    def test_abbreviations_pattern_matches_name(self):
        self.assertTrue(m.match_time_zone("fo", "foobar"))
        self.assertTrue(m.match_time_zone("fo/b", "foo/bar"))
        self.assertTrue(m.match_time_zone("fo/ba", "foo/bar"))
        self.assertTrue(m.match_time_zone("f/ba", "foo/bar"))
        self.assertTrue(m.match_time_zone("f/bar", "foo/bar"))
        self.assertTrue(m.match_time_zone("f/b_baz", "foo/bar_baz"))

    def test_abbreviations_must_match_first_letter_in_each_word(self):
        self.assertFalse(m.match_time_zone("oobar", "foobar"))
        self.assertFalse(m.match_time_zone("f/ar", "foo/bar"))
        self.assertFalse(m.match_time_zone("f/ar_baz", "foo/bar_baz"))
        self.assertFalse(m.match_time_zone("f/bar_az", "foo/bar_baz"))

    def test_pattern_can_skip_segments(self):
        self.assertTrue(m.match_time_zone("bar_baz", "foo/bar_baz"))
        self.assertTrue(m.match_time_zone("bar", "foo/bar_baz"))
        self.assertTrue(m.match_time_zone("ba", "foo/bar_baz"))
        self.assertTrue(m.match_time_zone("bb", "foo/bar_baz"))
        self.assertTrue(m.match_time_zone("foo/baz", "foo/bar/baz"))
        self.assertTrue(m.match_time_zone("f/baz", "foo/bar/baz"))
        self.assertTrue(m.match_time_zone("bar/baz", "foo/bar/baz"))
        self.assertTrue(m.match_time_zone("b/baz", "foo/bar/baz"))

    def test_pattern_cannot_insert_nonexisting_segments(self):
        self.assertFalse(m.match_time_zone("foo/bar/baz", "foo/baz"))
        self.assertFalse(m.match_time_zone("f/bar/baz", "foo/baz"))
        self.assertFalse(m.match_time_zone("f/bar", "foo/baz"))
        self.assertFalse(m.match_time_zone("foo/bar/baz", "bar/baz"))
        self.assertFalse(m.match_time_zone("f/bar/baz", "bar/baz"))
