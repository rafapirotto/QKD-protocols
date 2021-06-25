from e91 import e91

run_example = input("Run example?(y/n): ").lower()

if run_example == "y":
    alice_bases = ['Z','Z','X','Z','Z','X']
    bob_bases = ['Z','Z','Z','X','X','X']

    e91(alice_bases, bob_bases)
else:
    e91()
