import re
from textnode import TextNode, TextType
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
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

