from typing import AnyStr, List, Dict, SupportsInt, SupportsFloat
# TODO - actually use typing imported above


# --------------------- Custom Exceptions ---------------------
class RequiredArgumentError(Exception):
    pass


class BooleanValueError(Exception):
    pass


# ------------------ Options passed to parser -----------------
class MetaOptions:
    def __init__(self, xml_version: float, encoding: str):
        self._xml_version = xml_version
        self._encoding = encoding

    # ---------- xml_version ----------
    @property
    def xml_version(self):
        return self._xml_version

    @xml_version.setter
    def xml_version(self, new_version):
        self._xml_version = float(new_version)

    @xml_version.deleter
    def xml_version(self):
        raise RequiredArgumentError()

    # ---------- encoding ----------
    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, new_encoding):
        'Some text'.encode(encoding=new_encoding)
        self._encoding = new_encoding

    @encoding.deleter
    def encoding(self):
        raise RequiredArgumentError()


class ParserOptions:
    def __init__(self, indent_value: int, root_tag_name: str, show_null_fields: bool):
        self._indent_value = indent_value
        self._root_tag_name = root_tag_name
        self._show_null_fields = show_null_fields

    # ---------- indent_value ----------
    @property
    def indent_value(self):
        return self._indent_value

    @indent_value.setter
    def indent_value(self, new_value):
        self._indent_value = int(new_value)

    @indent_value.deleter
    def indent_value(self):
        raise RequiredArgumentError()

    # ---------- root_tag_name ----------
    @property
    def root_tag_name(self):
        return self._root_tag_name

    @root_tag_name.setter
    def root_tag_name(self, new_encoding):
        'Some text'.encode(encoding=new_encoding)
        self._root_tag_name = new_encoding

    @root_tag_name.deleter
    def root_tag_name(self):
        raise RequiredArgumentError()

    # ---------- show_null_fields ----------
    @property
    def show_null_fields(self):
        return self._show_null_fields

    @show_null_fields.setter
    def show_null_fields(self, new_value):
        if new_value in [
            'True',  'true',  'TRUE',  'T', 't', 1, True,
            'False', 'false', 'FALSE', 'F', 'f', 0, False
        ]:
            self._show_null_fields = new_value
        else:
            raise BooleanValueError

    @show_null_fields.deleter
    def show_null_fields(self):
        raise RequiredArgumentError()


def get_default_meta_options():
    return MetaOptions(1.0, 'utf-8')


def get_default_parser_options():
    return ParserOptions(4, 'root', False)


# ---------------------- XML Parser class ---------------------
class XMLParser:
    def __init__(
            self,
            meta_options: MetaOptions = get_default_meta_options(),
            parser_options: ParserOptions = get_default_parser_options()
    ) -> None:
        self._meta_options = {
            'xml_version': meta_options.xml_version,
            'encoding': meta_options.encoding
        }
        self._parsing_options = {
            'indent_value': parser_options.indent_value,
            'root_tag_name': parser_options.root_tag_name,
            'show_null_fields': parser_options.show_null_fields
        }

    def to_file(self, file_name: str, xml_string: any, write_mode: str = 'wb') -> None:
        with open(f'{file_name}', write_mode) as xml_file:
            xml_file.write(xml_string.encode(self._meta_options['encoding']))
        return xml_string

    def parse_to_xml(self, data_dictionary: dict) -> str:
        # Contains meta tag and open root tag
        xml_buf: list = [
            self._make_tag('xml', 0, attributes=self._meta_options, meta=True),
            self._make_tag(self._parsing_options["root_tag_name"], 0)
        ]
        # Start iteration over passed dict
        for key, value in data_dictionary.items():
            # Indent level 1 since root is 0
            indent_level: int = 1
            # Recursion is used in _traverse_dict()
            xml_buf.append(self._traverse_dict(key, value, indent_level))
        # Once we iterated over the dict, close root tag
        xml_buf.append(self._make_tag(self._parsing_options["root_tag_name"], 0, close=True))
        # Return XML string - list comprehension to remove empty strings
        # Empty string can appear when a dict key is present with a value of None or ''
        return '\n'.join([x for x in xml_buf if x])

    def _traverse_dict(self, key: str, value: any, indent_level: int) -> str:
        # If dict
        if type(value) is dict:
            # Open tag
            result = [
                self._make_tag(key, indent_level)
            ]
            # Iterate over dict type value
            for val_key, val_value in value.items():
                # Note the recursion
                result.append(
                    self._traverse_dict(val_key, val_value, indent_level + 1)
                )
            # Close tag once it's done
            result.append(
                self._make_tag(key, indent_level, close=True)
            )
            # Return XML string - list comprehension to remove empty strings
            return '\n'.join([x for x in result if x])
        # If list
        elif type(value) is list:
            result = [self._traverse_dict(key, val, indent_level) for val in value]
            return '\n'.join([x for x in result if x])
        # If not dict or list, just wrap the value and move on
        else:
            # If given key has a value of None, it's not included in the XML
            if not value and not self._parsing_options['show_null_fields']:
                print(value)
                return ''
            else:
                return self._make_tag(
                    key, indent_level, wrap='' if value is None else value
                )

    def _make_tag(self, tag_name: str, indent_level: int,
                  close: bool = False, wrap: any = None,
                  attributes: dict = None, meta: bool = False) -> str:
        """
        Takes name of a tag and indentation level to create a line of XML.
        If close is True and wrap is not None, raises AssertionError.
        If close is True and attributes is not None, raises AssertionError.
        If meta is True and wrap is not None, raises AssertionError.
        If meta is True and close is True, raises AssertionError.
        if meta is True and indent_level is not 0, raises AssertionError.

        :param tag_name (str): name of tag to make              | <tag_name>
        :param indent_level (int): level of indentation         | {indent_level}<tag_name>
        :param close (bool): is it a closing tag?               | </tag_name>
        :param wrap (any): value around which tags are wrapped  | <tag_name>wrap</tag_name>
        :return: (str): created tag
        """
        if close:
            assert wrap is None, "Param Error - Can't wrap values in closing tag"
            assert attributes is None, "Param Error - Can't make closing tag with attributes"

        if meta:
            assert wrap is None, "Param Error - Meta tag can't wrap any value"
            assert close is False, "Param Error - Meta tag can't be closed"
            assert indent_level == 0, "Param Error - Meta tag is always on indent level 0"
            attr: str = ''
            if attributes:
                for key, value in attributes.items():
                    attr += f' {key}="{value}"'
            return f'<?xml{attr}?>'

        ind: str = self._spacing(indent_level)
        if wrap is not None:  # It can still be ''
            attrs: str = ''
            if attributes:
                for key, value in attributes.items():
                    attrs += f' {key}="{value}"'
            return f'{ind}<{tag_name}{attrs}>{wrap}</{tag_name}>'
        else:
            return f'{ind}<{"/" if close else ""}{tag_name}>'

    def _spacing(self, indent_level: int) -> str:
        return f'{" " * self._parsing_options["indent_value"] * indent_level}'
