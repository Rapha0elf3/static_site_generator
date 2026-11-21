import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_multi_prop(self):
        node = HTMLNode("p", "test text", [HTMLNode("p", "test children", None,{"href": "https://www.google.com.br", "target": "_blank",} )], {"href": "https://www.google.com", "target": "_blank",} )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_single_prop(self):
        node = HTMLNode("p", "test text", [HTMLNode("p", "test children", None,{"href": "https://www.google.com.br", "target": "_blank",} )], {"href": "https://www.google.com"} )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_when_prop_none(self):
        node = HTMLNode("p", "test text", [HTMLNode("p", "test children", None,{"href": "https://www.google.com.br", "target": "_blank",} )], None)

        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_when_prop_empty(self):
        node = HTMLNode("p", "test text", [HTMLNode("p", "test children", None,{"href": "https://www.google.com.br", "target": "_blank",} )], {})

        self.assertEqual(node.props_to_html(), "")
