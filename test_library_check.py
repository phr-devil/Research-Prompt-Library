"""Markdown link validator regression: existing file != valid GFM link."""
import unittest
from library_check import invalid_markdown_destination


class MarkdownLinkTests(unittest.TestCase):
    def test_unescaped_spaces_in_url_fail(self):
        self.assertTrue(invalid_markdown_destination("03_SCI论文/P02_SCI 论文章节正文撰写.md"))

    def test_percent_encoded_target_passes(self):
        self.assertFalse(invalid_markdown_destination("03_SCI论文/P02_SCI%20论文章节正文撰写.md"))

    def test_angle_bracketed_destination_passes(self):
        self.assertFalse(invalid_markdown_destination("<03_SCI论文/P02_SCI 论文章节正文撰写.md>"))

    def test_quoted_link_title_passes(self):
        self.assertFalse(invalid_markdown_destination('path/file.md "descriptive title"'))

    def test_bare_spaces_fail_even_with_title(self):
        self.assertTrue(invalid_markdown_destination('path/bad file.md "descriptive title"'))


if __name__ == "__main__":
    unittest.main()
