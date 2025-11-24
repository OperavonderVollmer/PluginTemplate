from abc import ABC, abstractmethod
from typing import List, Dict, Any


# -----------------------------
# Base Component Classes
# -----------------------------

class JS_Component(ABC):
    """Base class for all components."""

    type: str = None

    def __init__(self, id: str, **props):
        self.id = id
        self.props = props

    def serialize(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "id": self.id,
            "props": self.props
        }


class JS_Container(JS_Component):
    """Base class for components that may contain children."""

    def __init__(self, id: str, children: List["JS_Component"] = None, **props):
        super().__init__(id, **props)
        self.children = children or []

    def add(self, *children: "JS_Component"):
        self.children.extend(children)
        return self

    def serialize(self) -> Dict[str, Any]:
        base = super().serialize()
        base["children"] = [child.serialize() for child in self.children]
        return base


# -----------------------------
# Container Components
# -----------------------------

class JS_Div(JS_Container):
    type = "div"


class JS_Form(JS_Container):
    type = "form"


class JS_Section(JS_Container):
    type = "section"


# -----------------------------
# Leaf Components
# -----------------------------

class JS_Label(JS_Component):
    type = "label"

    def __init__(self, id: str, text: str, **props):
        super().__init__(id, text=text, **props)


class JS_TextBox(JS_Component):
    type = "input"

    def __init__(self, id: str, label: str, hint: str = "", **props):
        super().__init__(id, label=label, hint=hint, **props)


class JS_Select(JS_Component):
    type = "select"

    def __init__(self, id: str, label: str, options: List[str], **props):
        super().__init__(id, label=label, options=options, **props)


class JS_Checkbox(JS_Component):
    type = "checkbox"

    def __init__(self, id: str, label: str, options: List[str], **props):
        super().__init__(id, label=label, options=options, **props)


class JS_Radio(JS_Component):
    type = "radio"

    def __init__(self, id: str, label: str, options: List[str], **props):
        super().__init__(id, label=label, options=options, **props)


class JS_Button(JS_Component):
    type = "button"

    def __init__(self, id: str, text: str, **props):
        super().__init__(id, text=text, **props)


# -----------------------------
# Page Wrapper
# -----------------------------

class JS_Page:
    def __init__(self, title: str, root: JS_Container):
        self.title = title
        self.root = root

    def serialize(self):
        return {"title": self.title, "root": self.root.serialize()}
