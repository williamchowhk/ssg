import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
