from abc import ABC, abstractmethod
from typing import List, Dict, Any


# -----------------------------
# Base Component Classes
# -----------------------------

class JS_Component(ABC):
    """Base class for all components."""

    type: str = None

    def __init__(self, id: str, classes: str = None, **props):
        self.id = id
        self.classes = classes
        self.props = props

    def serialize(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "id": self.id,
            "classes": self.classes,
            "props": self.props
        }


class JS_Container(JS_Component):
    """Base class for components that may contain children."""

    def __init__(self, id: str, classes: str = None, children: List["JS_Component"] = None, **props):
        super().__init__(id=id, classes=classes, **props)
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

    def __init__(self, id: str, text: str, classes: str = None, **props):
        super().__init__(id=id, classes=classes, text=text, **props)


class JS_TextBox(JS_Component):
    type = "input"

    def __init__(self, id: str, label: str, hint: str = "", classes: str = None, **props):
        super().__init__(id=id, classes=classes, label=label, hint=hint, **props)


class JS_Select(JS_Component):
    type = "select"

    def __init__(self, id: str, label: str, options: List[str], classes: str = None, **props):
        super().__init__(id=id, classes=classes, label=label, options=options, **props)


class JS_Checkbox(JS_Component):
    type = "checkbox"

    def __init__(self, id: str, label: str, options: List[str], classes: str = None, **props):
        super().__init__(id=id, classes=classes, label=label, options=options, **props)


class JS_Radio(JS_Component):
    type = "radio"

    def __init__(self, id: str, label: str, options: List[str], classes: str = None, **props):
        super().__init__(id=id, classes=classes, label=label, options=options, **props)


class JS_Button(JS_Component):
    type = "button"

    def __init__(self, id: str, text: str, classes: str = None, **props):
        super().__init__(id=id, classes=classes, text=text, **props)


# -----------------------------
# Page Wrapper
# -----------------------------

class JS_Page:
    def __init__(self, title: str, prompt: str, form: bool, description: str, root: JS_Container):
        self.title = title
        self.description = description
        self.prompt = prompt
        self.form = form
        self.root = root

    def serialize(self):
        return {"title": self.title, "description": self.description, "prompt": self.prompt, "form": self.form, "root": self.root.serialize()}

