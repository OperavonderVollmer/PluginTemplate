from abc import ABC, abstractmethod
from typing import List, Dict, Any


# -----------------------------
# Base Component Classes
# -----------------------------

class JS_Component(ABC):
    """Base class for all components."""

    type: str = None # type: ignore

    def __init__(self, id: str, classes: str = None, **props):
        self.id = id
        self.classes = classes
        self.props = props

    def add_class(self, class_name: str):
        if self.classes:
            self.classes += f" {class_name}"
        else:
            self.classes = class_name
        return self

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
# Headers
# -----------------------------

class JS_H1(JS_Component):
    type = "h1"

    def __init__(self, id: str, text: str, classes: str = None, **props):
        super().__init__(id=id, classes=classes, text=text, **props)

class JS_H2(JS_Component):
    type = "h2"

    def __init__(self, id: str, text: str, classes: str = None, **props):
        super().__init__(id=id, classes=classes, text=text, **props)


class JS_H3(JS_Component):
    type = "h3"

    def __init__(self, id: str, text: str, classes: str = None, **props):
        super().__init__(id=id, classes=classes, text=text, **props)

class JS_H4(JS_Component):
    type = "h4"

    def __init__(self, id: str, text: str, classes: str = None, **props):
        super().__init__(id=id, classes=classes, text=text, **props)

class JS_H5(JS_Component):
    type = "h5"

    def __init__(self, id: str, text: str, classes: str = None, **props):
        super().__init__(id=id, classes=classes, text=text, **props)

class JS_H6(JS_Component):
    type = "h6"

    def __init__(self, id: str, text: str, classes: str = None, **props):
        super().__init__(id=id, classes=classes, text=text, **props)

class JS_Header_Div(JS_Container):
    type = "div"

    def __init__(self, id: str, header: str, header_level: int, child: JS_Component, classes: str = None, **props):
        c = f"headerDivDefault {classes}" 
        super().__init__(id=id, classes=c, **props)

        # Map header_level to the corresponding class
        heading_class_map = {
            1: JS_H1,
            2: JS_H2,
            3: JS_H3,
            4: JS_H4,
            5: JS_H5,
            6: JS_H6,
        }

        HeadingClass = heading_class_map.get(header_level, JS_H1)  # Default to H1 if invalid

        # Create heading and label
        heading_component: JS_Component = HeadingClass(id=f"{id}_header", text=header)
        indented_child = child.add_class("inputFieldDefaults")
        # Add them as children of the div
        self.add(heading_component, indented_child)


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

