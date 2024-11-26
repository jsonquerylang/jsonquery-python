from jsonquerylang import compile

# use the function `compile` to compile once and execute repeatedly
query = ["sort"]
execute = compile(query)
print(execute([32, 19, 23]))  # [19, 23, 32]
print(execute([5, 2, 7, 4]))  # [2, 4, 5, 7]
