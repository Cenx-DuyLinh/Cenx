s = "A man, a plan, a canal: Panama"

fwd = ""
bwd = ""
for l in s:
    if ord(l) >= 65 and ord(l) <= 90:
        num_buffer = ord(l) + 32
    elif ord(l) >= 97 and ord(l) <= 122 or ord(l) >= 48 and ord(l) <= 57:
        num_buffer = ord(l)
    else:
        continue
    fwd = fwd + chr(num_buffer)
    bwd = chr(num_buffer) + bwd
if bwd == fwd:
    print("true")
else:
    print("false")
