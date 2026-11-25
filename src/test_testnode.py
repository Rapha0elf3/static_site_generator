import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from converter import split_nodes_delimiter


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




    # Test split_nodes_delimiter

    def test_converter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_converter_delimiter_pair(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)


    def test_converter_delimiter_at_begining(self):
        node = TextNode("_italic_ at the begining", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("italic", TextType.ITALIC),
            TextNode(" at the begining", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_converter_delimiter_at_end(self):
        node = TextNode("italic at the _end._", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("italic at the ", TextType.TEXT),
            TextNode("end.", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_converter_only_delimiter(self):
        node = TextNode("**all by myself**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("all by myself", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_converter_multiple_delimiter(self):
        node = TextNode("this **text** has two **texts**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("this ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" has two ", TextType.TEXT),
            TextNode("texts", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_converter_with_odd_number_of_delimiters(self):
        node = TextNode("this **text** has two **texts", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_converter_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.BOLD)
        expected = []
        self.assertEqual(new_nodes, expected)

    def test_converter_empty_list(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        expected = []
        self.assertEqual(new_nodes, expected)

    def test_converter_with_bold_node(self):
        node = TextNode("already bolded bro", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("already bolded bro", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_converter_with_unmatched_delimeter(self):
        node = TextNode("text with not **enough delimeters", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_converter_with_only_delimiter(self):
        node = TextNode("******", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_converter_multiple_delimiter(self):
        node = TextNode("one **bold** two **bold** three **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("one ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" two ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" three ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_converter_with_no_delimiter(self):
        node = TextNode("This is text without delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text without delimiter", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()
