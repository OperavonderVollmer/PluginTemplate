from abc import ABC, abstractmethod

class JS_Component(ABC):
    type: str = None

    def __init__(self, **props):
        self.props = props
        self.children = []

    def add(self, *children):
        for child in children:
            if not isinstance(child, JS_Component):
                raise TypeError("Child must be a JS_Component")
            self.children.append(child)
        return self

    @abstractmethod
    def serialize(self):
        ...


class JS_Div(JS_Component):
    type = "div"

    def serialize(self):
        return {
            "type": self.type,
            "props": self.props,
            "children": [c.serialize() for c in self.children]
        }


class JS_TextBox(JS_Component):
    type = "input"

    def __init__(self, id: str, label: str, hint: str):
        super().__init__(id=id, label=label, hint=hint)

    def serialize(self):
        return {
            "type": self.type,
            "props": self.props
        }


class JS_Label(JS_Component):
    type = "label"

    def __init__(self, text: str):
        super().__init__(text=text)

    def serialize(self):
        return {
            "type": self.type,
            "props": self.props
        }


class JS_Checkbox(JS_Component):
    type = "checkbox"

    def __init__(self, id: str, label: str, options: list):
        super().__init__(id=id, label=label, options=options)

    def serialize(self):
        return {
            "type": self.type,
            "props": self.props
        }


class JS_Radio(JS_Component):
    type = "radio"

    def __init__(self, id: str, label: str, options: list):
        super().__init__(id=id, label=label, options=options)

    def serialize(self):
        return {
            "type": self.type,
            "props": self.props
        }


class JS_Select(JS_Component):
    type = "select"

    def __init__(self, id: str, label: str, options: list):
        super().__init__(id=id, label=label, options=options)

    def serialize(self):
        return {
            "type": self.type,
            "props": self.props
        }
