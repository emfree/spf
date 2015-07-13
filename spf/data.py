import attr
import collections


class Node(object):
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.children = {}

    def serialize(self, threshold=None):
        res = {
            'name': self.name,
            'value': self.value
        }
        if self.children:
            serialized_children = [
                child.serialize(threshold)
                for _, child in sorted(self.children.items())
                if child.value >= threshold
            ]
            if serialized_children:
                res['children'] = serialized_children
        return res

    def add_stack(self, frames, value):
        self.value += value
        if not frames:
            return
        head = frames[0]
        child = self.children.get(head)
        if child is None:
            child = Node(name=head)
            self.children[head] = child
        child.add_stack(frames[1:], value)

    def value(self):
        return self.value


@attr.s
class Tag(object):
    client_id = attr.ib()
    timestamp = attr.ib()


# TODO (emfree) improve this and the preceding class? Kinda repetitive/murky
class PersistentNode(object):
    def __init__(self, name):
        self.name = name
        self.values = collections.OrderedDict()
        self.children = {}

    def serialize(self, tfilter=None, threshold=0):
        value = self.value()
        if not value or value < threshold:
            return {}
        res = {
            'name': self.name,
            'value': value
        }
        if self.children:
            children = []
            for k, child in sorted(self.children.items()):
                ser = child.serialize(tfilter)
                if ser:
                    children.append(ser)
            if children:
                res['children'] = children
        return res

    def add_tagged_stack(self, frames, value, tag):
        if not isinstance(tag, Tag):
            raise TypeError()
        if tag not in self.values:
            self.values[tag] = 0
        self.values[tag] += value
        if not frames:
            return
        head = frames[0]
        child = self.children.get(head)
        if child is None:
            child = PersistentNode(name=head)
            self.children[head] = child
        child.add_tagged_stack(frames[1:], value, tag)

    def value(self, tfilter=None):
        if tfilter is None:
            tfilter = lambda x: True
        return sum(v for k, v in self.values.items() if tfilter(k))


def from_file(filename):
    with open(filename) as f:
        raw = f.readlines()
    root = Node('root')
    for line in raw:
        frames, value = line.split()
        frames = frames.split(';')
        try:
            value = int(value)
        except ValueError:
            continue
        root.add_stack(frames, value)
    return root
