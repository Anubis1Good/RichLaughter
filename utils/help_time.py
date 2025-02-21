from datetime import datetime

t = 1740147825000
t //= 1000
d = datetime.fromtimestamp(t)
print(d)