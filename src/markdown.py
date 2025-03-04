import re
from enum import Enum
from htmlnode import *
from textnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            texts = node.text.split(delimiter)
            for i in range(len(texts)):
                if i % 2 == 0:
                    new_nodes.append( TextNode( texts[i], TextType.TEXT ) )
                else:
                    new_nodes.append( TextNode( texts[i], text_type ) )
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_text = node.text
            matches = extract_markdown_images(node_text)
            for match in matches:
                sections = node_text.split(f"![{match[0]}]({match[1]})", 1)
                if len(sections[0]) > 0:
                    new_nodes.append( TextNode( sections[0], TextType.TEXT ) )
                new_nodes.append( TextNode( match[0], TextType.IMAGE, match[1] ) )
                node_text = sections[1]
            if len(node_text) > 0:
                new_nodes.append( TextNode( node_text, TextType.TEXT ) )
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_text = node.text
            matches = extract_markdown_links(node_text)
            for match in matches:
                sections = node_text.split(f"[{match[0]}]({match[1]})", 1)
                if len(sections[0]) > 0:
                    new_nodes.append( TextNode( sections[0], TextType.TEXT ) )
                new_nodes.append( TextNode( match[0], TextType.LINK, match[1] ) )
                node_text = sections[1]
            if len(node_text) > 0:
                new_nodes.append( TextNode( node_text, TextType.TEXT ) )
        else:
            new_nodes.append(node)
    return new_nodes

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    lines = list(map(str.strip, lines))
    blocks = []
    block = ""
    for line in lines:
        if len(line) == 0:
            if len(block) != 0:
                blocks.append(block)
            block = ""
        elif len(block) == 0:
            block = line
        else:
            block += "\n" + line
    if len(block) != 0:
        blocks.append(block)

    return blocks

def block_to_block_type(block):
    if re.findall(r"^[#]{1,6} ", block):
        return BlockType.HEADING
    if block[0:3] == "```" and block[-3:] == "```" and len(block) >= 6:
        return BlockType.CODE
    lines = block.split("\n")

    curType = None
    for line in lines:
        lineType = None
        if line[0] == ">":
            lineType = BlockType.QUOTE
        if line[0:2] == "* " or line[0:2] == "- ":
            lineType = BlockType.UNORDERED_LIST
        if curType != None and curType != lineType:
            return BlockType.PARAGRAPH
        curType = lineType
    if curType != None:
        return curType

    for i in range(0, len(lines) ):
        line = lines[i]
        matches = re.findall(r"^(\d+). ", line)
        if not matches:
            return BlockType.PARAGRAPH
        if int(matches[0]) != i + 1:
            return BlockType.PARAGRAPH

    return BlockType.ORDERED_LIST

def block_to_text(block, block_type):
    texts = [block]
    match block_type:
        case BlockType.HEADING:
            texts = [block[2:]]
        case BlockType.CODE:
            texts = [block[3:-3]]
        case BlockType.QUOTE:
            texts = block[1:].split("\n>")
        case BlockType.UNORDERED_LIST:
            if block[0] == "-":
                texts = block[2:].split("\n-")
            if block[0] == "*":
                texts = block[2:].split("\n*")
        case BlockType.ORDERED_LIST:
            texts = re.split(r"\n\d+. ", block[3:])
    return texts


def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        texts = block_to_text(block,block_type)
        match block_type:
            case BlockType.HEADING:
                nodes.append(LeafNode("h1", texts[0]))
            case BlockType.CODE:
                nodes.append(LeafNode("code", texts[0]))
            case BlockType.QUOTE:
                nodes.append(LeafNode("quote", texts[0]))
        if block_type == BlockType.PARAGRAPH:
            textnodes = text_to_textnodes(texts[0])
            htmlnodes = []
            for textnode in textnodes:
                htmlnodes.append(text_node_to_html_node(textnode))
            nodes.append(ParentNode("p", htmlnodes))
        if block_type == BlockType.UNORDERED_LIST:
            items = []
            for text in texts:
                items.append( LeafNode("li", text) )
            nodes.append(ParentNode("ul", items))
        if block_type == BlockType.ORDERED_LIST:
            items = []
            for text in texts:
                items.append( LeafNode("li", text) )
            nodes.append(ParentNode("ol", items))
    return ParentNode("div", nodes)

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter( new_nodes, "**", TextType.BOLD )
    new_nodes = split_nodes_delimiter( new_nodes, "*", TextType.ITALIC )
    new_nodes = split_nodes_delimiter( new_nodes, "`", TextType.CODE )
    new_nodes = split_nodes_image( new_nodes )
    new_nodes = split_nodes_link( new_nodes )
    return new_nodes

