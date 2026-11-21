


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
        return f"HTMLNode(\ntag={self.tag!r}\nvalue={self.value!r}\nchildren={self.children}\nprops={self.props}\n)"
