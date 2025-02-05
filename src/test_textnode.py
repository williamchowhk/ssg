import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode,LeafNode,ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

class TestTextNode2(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

class TestTextNode3(unittest.TestCase):
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

class TestTextNode4(unittest.TestCase):
    def test_text_node_to_html_node(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("alt", TextType.IMAGE, "image.png")
        pnode = ParentNode("p", [text_node_to_html_node(node1), text_node_to_html_node(node2)] )
        self.assertEqual( pnode.to_html(), "<p><b>This is a text node</b><img src=\"image.png\" alt=\"alt\"></img></p>" )

if __name__ == "__main__":
    unittest.main()
