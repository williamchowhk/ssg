import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode,LeafNode,ParentNode
from markdown import *

class TestMarkdown(unittest.TestCase):
    def test_split_nodes(self):
        tnode = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodes = split_nodes_delimiter([tnode], "`", TextType.CODE)
        leafnodes = []
        for node in nodes:
            leafnodes.append( text_node_to_html_node(node) )
        pnode = ParentNode("p", leafnodes )
        self.assertEqual( pnode.to_html(), "<p>This is text with a <code>code block</code> word</p>" )

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        ref=[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        tar=extract_markdown_images(text)
        self.assertEqual(ref,tar)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        ref = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        tar = extract_markdown_links(text)
        self.assertEqual(ref,tar)

if __name__ == "__main__":
    unittest.main()


