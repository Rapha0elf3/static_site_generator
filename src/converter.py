from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        elif not node.text:
            continue

        elif node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"unmatched '{delimiter}' in: {node.text!r}")

        else:
            splitted = node.text.split(delimiter)
            for i, section in enumerate(splitted):
                if not section:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(section, text_type))

    return new_nodes
