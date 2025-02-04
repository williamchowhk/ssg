import unittest
from htmlnode import HTMLNode,LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode("div", "hello", None, {"class":"test", "href":"https://google.com"} )
        self.assertEqual( node.props_to_html(), " class=\"test\" href=\"https://google.com\"" )

    def test_values(self):
        node = HTMLNode("div", "hello" )
        self.assertEqual( node.tag, "div" )
        self.assertEqual( node.value, "hello" )
        self.assertEqual( node.children, None )
        self.assertEqual( node.props, None )

    def test_leaf_node(self):
        node1 = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual( node1.to_html(), "<a href=\"https://www.google.com\">Click me!</a>" )
        self.assertEqual( node2.to_html(), "<p>This is a paragraph of text.</p>" );

if __name__ == "__main__":
    unittest.main()
