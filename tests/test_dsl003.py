class Atom:
    pass


class Property:
    pass


class Relation:
    ONE_TO_ONE = 0
    ONE_TO_MANY = 1
    MANY_TO_ONE = 2
    MANY_TO_MANY_SYM = 3
    MANY_TO_MANY_ASYM = 4


class ContainerProperty(Property):
    def __init__(self):
        self._children = list()

    def add(self, item):
        self._children.append(item)

    def remove(self, item):
        self._children.remove(item)


class Map(Atom):
    pass


class Exit(Atom):
    pass


class Thing(Atom):
    pass


class Person(Thing):
    pass


class Chest(Thing):
    pass


def main():
    import yaml

    supers = {
        "thing": Thing,
    }

    with open("dw_script003.yaml") as fp:
        data = yaml.load(fp.read(), yaml.SafeLoader)

    for k, v in data.items():
        supr = supers.get(v["super"])


if __name__ == "__main__":
    main()
