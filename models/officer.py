from models.types.enums import State, Ethnicity, Gender
from models.source import Citation

from neomodel import (
    StructuredNode,
    RelationshipTo, RelationshipFrom, Relationship,
    StringProperty, DateProperty,
    UniqueIdProperty, One
)


class StateID(StructuredNode):
    """
    Represents a Statewide ID that follows an offcier even as they move between
    law enforcement agencies. For example, in New York, this would be
    the Tax ID Number.
    """
    id_name = StringProperty()  # e.g. "Tax ID Number"
    state = StringProperty(choices=State.choices())  # e.g. "NY"
    value = StringProperty()  # e.g. "958938"
    officer = RelationshipFrom('Officer', "HAS_STATE_ID", cardinality=One)

    def __repr__(self):
        return f"<StateID: Officer {self.officer_id}, {self.state}>"


class Officer(StructuredNode):
    __property_order__ = [
        "uid", "first_name", "middle_name",
        "last_name", "suffix", "ethnicity",
        "gender", "date_of_birth"
    ]

    uid = UniqueIdProperty()
    first_name = StringProperty()
    middle_name = StringProperty()
    last_name = StringProperty()
    suffix = StringProperty()
    ethnicity = StringProperty(choices=Ethnicity.choices())
    gender = StringProperty(choices=Gender.choices())
    date_of_birth = DateProperty()
    year_of_birth = StringProperty()

    # Relationships
    state_ids = RelationshipTo('StateID', "HAS_STATE_ID")
    units = RelationshipTo(
        'models.agency.Unit', "MEMBER_OF_UNIT")
    litigation = Relationship(
        'models.litigation.Litigation', "NAMED_IN")
    allegations = Relationship(
        'models.complaint.Allegation', "ACCUSED_OF")
    investigations = Relationship(
        'models.complaint.Investigation', "LEAD_BY")
    commands = Relationship(
        'models.agency.Unit', "COMMANDS")
    citations = RelationshipTo(
        'models.source.Source', "UPDATED_BY", model=Citation)

    def __repr__(self):
        return f"<Officer {self.id}>"
