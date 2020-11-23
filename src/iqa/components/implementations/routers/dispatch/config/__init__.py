from typing import Optional


class _Attribute:
    def __init__(self, name: str, value: str, deprecated: bool = False) -> None:
        self.name: str = name
        self.value: str = value
        self.deprecated: bool = deprecated

    def get_config(self) -> Optional[str]:
        """Get in config format"""
        return '    %s: %s\n' % (self.name, self.value) if self.value else None

    def __str__(self) -> str:
        return self.value

    def __set__(self, instance, value: str) -> None:
        self.value = value


class _Section:
    section_name: Optional[str] = None
    deprecated: bool = False

    def get_config(self):
        sec = '%s: {\n' % self.section_name
        for x in self.__dict__.items():
            for value in x:
                if isinstance(value, _Attribute):
                    val = value.value
                    if val is not None:
                        sec += '    %s: %s\n' % (value.name, val)
        sec += '}'
        return sec

    def __str__(self) -> str:
        return self.get_config()

    def __getattribute__(self, name: str) -> str:
        value = object.__getattribute__(self, name)
        if hasattr(value, '__get__'):
            value = value.__get__(self, self.__class__)
        return value

    def __setattr__(self, name: str, value: str):
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            pass
        else:
            if hasattr(obj, '__set__'):
                return obj.__set__(self, value)
        return object.__setattr__(self, name, value)


class Config(list):
    """Qpid Dispatch configuration"""

    def __init__(self) -> None:
        super().__init__()

    def add_section(self, section: _Section) -> None:
        self.append(section)

    def get_config(self) -> str:
        conf: str = ''
        i: int = 0
        num_sections: int = len(self)
        for section in self:
            i += 1
            conf += '%s: {\n' % section.section_name
            for attributes in section.__dict__.items():
                for attr in attributes:
                    if isinstance(attr, _Attribute):
                        tmp_val: str = attr.value
                        if tmp_val is not None:
                            conf += '    %s: %s\n' % (attr.name, tmp_val)
            conf += '}\n'
            if i < num_sections:
                conf += '\n'
        return conf
