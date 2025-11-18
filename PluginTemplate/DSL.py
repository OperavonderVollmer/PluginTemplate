from abc import ABC, abstractmethod
from typing import List, Dict, Any


# -----------------------------
# Base Component Classes
# -----------------------------

class JSComponent(ABC):
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


class JSContainer(JSComponent):
    """Base class for components that may contain children."""

    def __init__(self, id: str, children: List["JSComponent"] = None, **props):
        super().__init__(id, **props)
        self.children = children or []

    def add(self, *children: "JSComponent"):
        self.children.extend(children)
        return self

    def serialize(self) -> Dict[str, Any]:
        base = super().serialize()
        base["children"] = [child.serialize() for child in self.children]
        return base


# -----------------------------
# Container Components
# -----------------------------

class JS_Div(JSContainer):
    type = "div"


class JS_Form(JSContainer):
    type = "form"


class JS_Section(JSContainer):
    type = "section"


# -----------------------------
# Leaf Components
# -----------------------------

class JS_Label(JSComponent):
    type = "label"

    def __init__(self, id: str, text: str, **props):
        super().__init__(id, text=text, **props)


class JS_TextBox(JSComponent):
    type = "input"

    def __init__(self, id: str, label: str, hint: str = "", **props):
        super().__init__(id, label=label, hint=hint, **props)


class JS_Select(JSComponent):
    type = "select"

    def __init__(self, id: str, label: str, options: List[str], **props):
        super().__init__(id, label=label, options=options, **props)


class JS_Checkbox(JSComponent):
    type = "checkbox"

    def __init__(self, id: str, label: str, options: List[str], **props):
        super().__init__(id, label=label, options=options, **props)


class JS_Radio(JSComponent):
    type = "radio"

    def __init__(self, id: str, label: str, options: List[str], **props):
        super().__init__(id, label=label, options=options, **props)


class JS_Button(JSComponent):
    type = "button"

    def __init__(self, id: str, text: str, **props):
        super().__init__(id, text=text, **props)


# -----------------------------
# Page Wrapper
# -----------------------------

class JS_Page:
    def __init__(self, title: str, root: JSContainer):
        self.title = title
        self.root = root

    def serialize(self):
        return {"title": self.title, "root": self.root.serialize()}
