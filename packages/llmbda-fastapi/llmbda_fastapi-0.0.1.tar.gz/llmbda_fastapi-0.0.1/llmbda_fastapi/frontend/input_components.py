"""
    All components are here
"""
from dataclasses import dataclass, field

class Component:
    """
    Base class for all components
    """

@dataclass
class APIKeyInput(Component):
    valueKey: str = ""
    type: str = "apiKeyInput"
    props: dict = field(default_factory=lambda: {
        "apiKey": ""
    })


@dataclass
class FieldSelector(Component):
    type: str = "fieldSelector"
    props: dict = field(
        default_factory=lambda: {"onlyTypes": ["vector"], "multiple": False}
    )


@dataclass
class FileUpload(Component):
    title: str = "Upload your files."
    description: str = "You can upload your files here."
    type: str = "fileUpload"
    props: dict = field(
        default_factory=lambda: {
            "accept": "*",  # optional, filters accepted file/mime-types. See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file#limiting_accepted_file_types
            "multiple": True,  # optional, enables multiple files uploaded
        }
    )


@dataclass
class AdvancedFilters(Component):
    valueKey: str = "filters"
    type: str = "advancedFilterInput"
    props: dict = field(default_factory=lambda: {"optional": True})


@dataclass
class BaseInput(Component):
    type: str = "baseInput"
    props: dict = field(
        default_factory=lambda: {
            "type": "text",
            "value": "default",
        }
    )

@dataclass
class BaseTextArea(Component):
    type: str = "baseTextArea"
    props: dict = field(
        default_factory=lambda: {
            "type": "text",
            "placeholder": "Enter value...",
            "rows" : 2,
            "maxlength" : 500
        }
    )
    
@dataclass
class PromptArea(Component):
    type: str = "playgroundPrompt"

@dataclass
class BaseDropdown(Component):
    type: str = "baseDropdown"
    props: dict = field(default_factory=lambda: {})

@dataclass
class BoolDropdown(Component):
    type: str = "baseDropdown"
    props: dict = field(default_factory=lambda: {
        "options": [
            {
                "label": "Yes",
                "value": True,
            },
            {
                "label": "No",
                "value": False,
            },
        ],
        "multiple": False,
        "optional": True,
        "value": True
    })

@dataclass
class SentenceListInput(Component):
    type: str = "sentenceListInput"
    props: dict = field(default_factory=lambda: {
    })

@dataclass
class BooleanChecklist(Component):
    type: str = "booleanChecklist"
    props: dict = field(default_factory=lambda: {
        "labelMap" : {"example":{"description": "This is what users see for example", "value" : False}}
    })

@dataclass
class TagsInput(Component):
    type: str = "tagsInput"
    props: dict = field(default_factory=lambda: {"props": {"separators": [","]}})

@dataclass
class TaxonomyBuilder(Component):
    type: str = "taxonomyBuilder"
    props: dict = field(default_factory=lambda: {})

@dataclass
class SliderInput(Component):
    type: str = "baseInput"
    props: dict = field(
        default_factory=lambda: {"type": "number", "max": 100, "step": 1, "min": 1}
    )

@dataclass
class DynamicTextInput(Component):
    type: str = "dynamicInput"
    props: dict = field(
        default_factory=lambda: {
            "outputLabel": "Output field name:",  # Optional, defaults to "This will be stored as:",
            "template": "_surveytag_.{ vector_fields }.{ value }",  # Required, use `{ value }` to reference current component's value. Can reference other fields by `valueKey`
        }
    )


@dataclass
class AggregateTagsSelector(Component):
    type: str = "aggregateTagsSelector"
    props: dict = field(
        default_factory=lambda: {
            "aggregationQuery": {  # Required
                "groupby": [
                    {
                        "name": "field",  #
                        "field": "{ field }",  # Use this to refer to the selected field
                        "agg": "category",
                    }
                ]
            },
            "aggregationResultField": "field",  # Required, sHould match `name` in aggregationQuery
            "maxRunResults": 20,  # maximum number of tags to get from aggregate, defaults to 20
        }
    )


@dataclass
class AggregateSelector(Component):
    type: str = "aggregateSelector"
    props: dict = field(
        default_factory=lambda: {
            "aggregationQuery": {  # Required
                "groupby": [
                    {
                        "name": "field",  #
                        "field": "{ field }",  # Use this to refer to the selected field
                        "agg": "category",
                    }
                ]
            },
            "aggregationResultField": "field",  # Required, sHould match `name` in aggregationQuery
            "maxRunResults": 20,  # maximum number of tags to get from aggregate, defaults to 20
        }
    )


@dataclass
class ExplorerSelector(Component):
    type: str = "explorerSelector"
    props: dict = field(default_factory=lambda: {})


@dataclass
class TagPairInput(Component):
    type: str = "pairInput"
    props: dict = field(default_factory=lambda: {"addTagText": "Add new tag"})


@dataclass
class DatasetInput(Component):
    type: str = "datasetNameInput"
    props: dict = field(default_factory=lambda: {})