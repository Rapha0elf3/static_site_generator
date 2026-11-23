import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):


    ## Testing props_to_html of HTMLNode
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

    ## Testing to_html of LeafNode
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

    ## Testing to_html of ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_child_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("a", [grandchild_node], {"href": "https://www.google.com.br"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https://www.google.com.br"><b>grandchild</b></a></div>',
        )

    def test_to_html_with_many_parents(self):
        cnode2 = LeafNode("a", "leaf Link", {"href": "https://www.google.com.br"})
        cnode1 = LeafNode("b", "leaf")
        pnode4 = ParentNode("p", [cnode1])
        pnode3 = ParentNode("span", [pnode4])
        pnode2 = ParentNode("p", [cnode2])
        pnode1 = ParentNode("div", [pnode2, pnode3])
        self.assertEqual(
            pnode1.to_html(),
            '<div><p><a href="https://www.google.com.br">leaf Link</a></p><span><p><b>leaf</b></p></span></div>',
        )

    def test_to_html_errors(self):
        # No tag
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "bold")])
            node.to_html()
        # Missing children
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()
