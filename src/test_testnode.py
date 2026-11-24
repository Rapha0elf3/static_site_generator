import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_tt_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)


    # Test text_node_to_html_node

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {'href': 'https://www.boot.dev'})

    def test_text_to_html_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {'src': 'https://www.boot.dev', 'alt': 'This is an image'})

    def test_text_to_html_no_text(self):
        node = TextNode("", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "")

    def test_text_to_html_with_invalid_type(self):
        node = TextNode("This is a text node", "TextType.CHUNGUS")
        with self.assertRaises(Exception) as cm:
            html_node = text_node_to_html_node(node)
        self.assertIn("invalid text type", str(cm.exception))

    def test_text_to_html_big_text(self):
        text = ""
        for i in range(10000):
            text += 'a'

        node = TextNode(text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, text)


if __name__ == "__main__":
    unittest.main()
