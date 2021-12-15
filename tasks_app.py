from tasks import add
result = add.delay(30000, 1337)

print(result.ready())
print(result.get())
print(result.ready())