class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        formatted_string = ""
        for key, value in self.props.items():
            formatted_string += f' {key}="{value}"'
        return formatted_string

    def __repr__(self):
        return (f"HTMLNode(\ntag={self.tag!r}\nvalue={self.value!r}\nchildren={self.children}\nprops={self.props}\n)")

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Missing Value")

        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return (f"HTMLNode(\ntag={self.tag!r}\nvalue={self.value!r}\nprops={self.props}\n)")

class ParentNode(HTMLNode):

    def __init__(self, tag ,children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")

        if self.children is None:
            raise ValueError("Missing children")

        code = ""
        for child in self.children:
            code += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{code}</{self.tag}>"
