import unittest
from htmlnode import HTMLNode,LeafNode,ParentNode

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
        self.assertEqual( node2.to_html(), "<p>This is a paragraph of text.</p>" )

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ])
        self.assertEqual( node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>" )

    def test_parent_node_2(self):
        node = ParentNode("p", [
                ParentNode("p", [
                 ParentNode("p", [
                  LeafNode("b", "Bold text"),
                  LeafNode(None, "Normal text"),
                  LeafNode("i", "italic text"),
                  LeafNode(None, "Normal text")
                 ], {'class':'test1'} )
                ], {'class':'test2'} )
               ] )
        self.assertEqual( node.to_html(), "<p><p class=\"test2\"><p class=\"test1\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p></p>" )

if __name__ == "__main__":
    unittest.main()
