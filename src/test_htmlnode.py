import unittest
from htmlnode import HTMLNode, LeafNode


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


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_leaf_to_html_a_no_prop(self):
        node = LeafNode("a", "link!")
        self.assertEqual(node.to_html(), "<a>link!</a>")

    def test_leaf_to_html_a_with_prop(self):
        node = LeafNode("a", "ref link!", {"href": "https://www.google.com.br"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com.br">ref link!</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("h1", "The big title!")
        self.assertEqual(node.to_html(), "<h1>The big title!</h1>")
