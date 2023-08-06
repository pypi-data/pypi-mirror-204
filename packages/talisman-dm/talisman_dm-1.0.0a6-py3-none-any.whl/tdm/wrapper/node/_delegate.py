from dataclasses import replace


def getter_delegate(name: str):
    def f(self, *args, **kwargs):
        return getattr(self.markup, name)(*args, **kwargs)

    return f


def property_delegate(name: str):
    def f(self):
        return getattr(self.markup, name)

    return property(f)


def modifier_delegate(name: str, validators):
    def f(self, *args, **kwargs):
        for validator in validators:
            validator(self, *args, **kwargs)
        return replace(self, markup=getattr(self.markup, name)(*args, **kwargs))

    return f
