import itertools
import unittest
from pprint import pprint

import yaml

assert pprint


def map_by_attr(attr, items):
    return {getattr(i, attr): i for i in items}


class Atom:
    pass


class Property:
    name = "Property"
    value = None

    def __str__(self):
        if self.value is None:
            return self.name
        else:
            return f"{self.name}={self.value}"


class Relation:
    ONE_TO_ONE = 0
    ONE_TO_MANY = 1
    MANY_TO_ONE = 2
    MANY_TO_MANY_SYM = 3
    MANY_TO_MANY_ASYM = 4


class PositionRelation(Relation):
    name = "position"


class NamedProperty(Property):
    name = "named"


class TimelineProperty(Property):
    name = "timeline"


class LineageProperty(Property):
    name = "lineage"


class LivingProperty(Property):
    name = "living"


class CollectionProperty(Property):
    name = "collection"


class ContainerProperty(Property):
    name = "container"

    def __init__(self):
        self.value = list()

    def add(self, item):
        self.value.append(item)

    def remove(self, item):
        self.value.remove(item)


class Map(Atom):
    pass


class Exit(Atom):
    pass


class Thing(Atom):
    def __init__(self):
        self._props = dict()

    @property
    def properties(self):
        return self._props.values()

    def add_property(self, prop):
        self._props[prop.name] = prop

    def set_property(self, name, value):
        self._props[name].value = value

    def __str__(self):
        props = ", ".join(str(i) for i in self._props.values())
        return f"<Thing: {props}>"


class Person(Thing):
    pass


class Chest(Thing):
    pass


class YAMLLoader:
    def __init__(self):
        self.supers = {"thing": Thing}
        self.super_map = dict()
        self.super_props = dict()
        props = [
            CollectionProperty,
            ContainerProperty,
            LineageProperty,
            TimelineProperty,
            LivingProperty,
            NamedProperty,
        ]
        self.all_props = map_by_attr("name", props)

    def load(self):
        filename = "dw_script003.yaml"
        data = self.load_yaml(filename)

        for name, v in data.items():
            supr = v["super"]
            supr_class = self.supers.get(supr)
            if supr_class is None:
                # needs a search
                parent = self.super_map[supr]
                supr_class = self.supers.get(parent)
            assert name not in self.super_map
            self.super_props[name] = v.get("properties", [])
            self.super_map[name] = supr
            thing = supr_class()
            for prop_item in self.get_properties(name):
                prop = self.as_property(prop_item)
                thing.add_property(prop)
            self.set_property_values(thing, v)
            print(name, thing)

    def search(self, name):
        yield name
        yield self.super_map[name]

    def as_property(self, prop_config):
        if isinstance(prop_config, str):
            prop_name = prop_config
            attrs = None
        elif isinstance(prop_config, dict):
            assert len(prop_config) <= 1
            prop_name, attrs = list(prop_config.items())[0]
        else:
            raise ValueError
        prop_class = self.all_props[prop_name]
        prop = prop_class()  # type: Property
        if attrs is not None:
            prop.value = attrs
        return prop

    def set_property_values(self, thing, config):
        for prop in thing.properties:
            if prop.name in config:
                thing.set_property(prop.name, config[prop.name])

    def get_properties(self, name):
        names = self.search(name)
        props = (self.super_props.get(i, []) for i in names)
        props = list(itertools.chain(*props))
        return props

    @staticmethod
    def load_yaml(filename):
        with open(filename) as fp:
            return yaml.load(fp.read(), yaml.SafeLoader)


class Test(unittest.TestCase):
    def test(self):
        loader = YAMLLoader()
        loader.load()
