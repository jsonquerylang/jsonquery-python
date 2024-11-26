from pprint import pprint
from jsonquerylang import parse, stringify

# parse the human friendly text format into the corresponding JSON format
text_query = '.friends | filter(.city == "new York") | sort(.age) | pick(.name, .age)'
json_query = parse(text_query)
pprint(json_query)
# ['pipe',
#  ['get', 'friends'],
#  ['filter', ['eq', ['get', 'city'], 'New York']],
#  ['sort', ['get', 'age']],
#  ['pick', ['get', 'name'], ['get', 'age']]]

# stringify the JSON format into the corresponding text format
print(stringify(json_query))
# """
# .friends
#   | filter(.city == "new York")
#   | sort(.age)
#   | pick(.name, .age)
# """

# stringify with a custom indentation of 4 spaces
print(stringify(json_query, {"indentation": "    "}))
# """
# .friends
#     | filter(.city == "new York")
#     | sort(.age)
#     | pick(.name, .age)
# """

# now, both text_query and json_query can be used in the jsonquery() function,
# and json_query can be used in the compile() function.
