from xml_parser import XMLParser

if __name__ == '__main__':
    # Hardcoded dict 'cause who wants to read from a JSON file
    data_dict = {
        'a': 2,
        'b': 3,
        'c': {
            'c1': 'yo',
            'c2': 'yoyo',
            'c3': {
                'c31': 'sup',
                'c32': 'supsup',
                'c33': None,
                'c34': [
                    {
                        'c341': 1,
                        'c342': 'forsenW'
                    },
                    {
                        'c341': 2,
                        'c342': 'aniZoom'
                    },
                    {
                        'c341': 3,
                        'c342': 'aniW'
                    },
                    {
                        'c341': 4,
                        'c342': 'sadge'
                    },
                    {
                        'c341': 5,
                        'c342': 'NotLikeThis'
                    }
                ]

            },
            'c4': 'stuff',
            'c5': [
                'c51',
                'c52',
                'c53'
            ]
        },
        'd': 'yes ¥ĘŜ YES',
        'e': None
    }
    # Init the parser (No arguments means it's using default options)
    parser = XMLParser()
    # Parse the hardcoded dict to an XML string
    xml_data: str = parser.parse_to_xml(data_dict)
    # Write parsed data to file
    parser.to_file('testo.xml', xml_data)
    # Printing result to console, 'cause why not, right?
    print(parser.parse_to_xml(data_dict))
