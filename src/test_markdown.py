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

    def test_split_images(self):
        node = TextNode("This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/bootdotdev.jpg)", TextType.TEXT,)
        tar = split_nodes_image([node])
        ref = [ TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/bootdotdev.jpg"),
              ]
        self.assertEqual(ref,tar)

    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        tar = split_nodes_link([node])
        ref = [ TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
              ]
        self.assertEqual(ref,tar)

    def test_text_to_textnodes(self):
        tar = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        ref = [ TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
              ]
        self.assertEqual(ref,tar)

    def test_markdown_to_blocks(self):
        tar = markdown_to_blocks('''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item''')
        ref = [ "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item" ]
        self.assertEqual(ref,tar)

    def test_block_type_heading(self):
        tar = [ block_to_block_type( "# heading" ),
                block_to_block_type( "## heading" ),
                block_to_block_type( "#### heading" ),
                block_to_block_type( "###### heading" ),
                block_to_block_type( "####### heading" ),
                block_to_block_type( "#heading" ),
                block_to_block_type( "heading" ),
                block_to_block_type( "###" ) ]
        ref = [ BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH ]
        self.assertEqual(ref,tar)

    def test_block_type_code(self):
        tar = [ block_to_block_type( "```code```" ),
                block_to_block_type( "```code1\ncode2\ncode3```" ),
                block_to_block_type( "```code1\n```\ncode3```" ),
                block_to_block_type( "``````" ),
                block_to_block_type( "``code``" ),
                block_to_block_type( "```code" ),
                block_to_block_type( "code```" ),
                block_to_block_type( "`code`" ),
                block_to_block_type( "code```code```code" ),
                block_to_block_type( "```" ) ]
        ref = [ BlockType.CODE,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH ]
        self.assertEqual(ref,tar)
    
    def test_block_type_quote(self):
        tar = [ block_to_block_type( ">line1\n>line2" ),
                block_to_block_type( ">line1" ),
                block_to_block_type( ">line1\n>line2>line3" ),
                block_to_block_type( ">>line1" ),
                block_to_block_type( ">line1\nline2" ),
                block_to_block_type( ">line1\n line2" ),
                block_to_block_type( "line1" ) ]
        ref = [ BlockType.QUOTE,
                BlockType.QUOTE,
                BlockType.QUOTE,
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH ]
        self.assertEqual(ref,tar)

    def test_block_type_list(self):
        tar = [ block_to_block_type( "- line1\n- line2" ),
                block_to_block_type( "* line1\n* line2" ),
                block_to_block_type( "- line1" ),
                block_to_block_type( "* line1" ),
                block_to_block_type( "1. line1\n2. line2" ),
                block_to_block_type( "1. line1\n2. line2\n3. line3" ),
                block_to_block_type( "1. line1\n1. line2" ) ]
        ref = [ BlockType.UNORDERED_LIST,
                BlockType.UNORDERED_LIST,
                BlockType.UNORDERED_LIST,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH ]
        self.assertEqual(ref,tar)

    def test_markdown_to_html(self):
        tar = markdown_to_html_node(
'''
# Heading

first paragraph

```code```

>item1
>item2

1. ol item1
2. ol item2

- ul item1
- ul item2

hello *world*

''')
        print(tar.to_html())

if __name__ == "__main__":
    unittest.main()


