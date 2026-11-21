from textnode import TextNode, TextType
from htmlnode import HTMLNode
def main():

    block = TextNode("macarico", TextType.BOLD, "https://www.boot.dev")
    print(block)
    html = HTMLNode("p", "test text", [HTMLNode("p", "test children")], {"href": "https://www.google.com", "target": "_blank",} )
    print(html)
main()
