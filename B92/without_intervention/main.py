from b92 import b92

run_example = input("Run example?(y/n): ").lower()

if run_example == "y":
    alice_bits = ['1','0','1','1','1','0']
    bob_bits = ['0','0','1','0','0','1']
    vector = ['1', '0', '0', '0', '1', '1']

    b92(alice_bits, bob_bits, vector)
else:
    b92()
