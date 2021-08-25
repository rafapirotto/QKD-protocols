from getErrorRate import getChannelErrorRate

getChannelErrorRate(['0', '0', '0', '0', '0'], ['Z', 'Z', 'Z', 'Z', 'Z'])
getChannelErrorRate(['0', '0', '0', '0', '0'], ['X', 'X', 'X', 'X', 'X'])
getChannelErrorRate(['1', '1', '1', '1', '1'], ['Z', 'Z', 'Z', 'Z', 'Z'])
getChannelErrorRate(['1', '1', '1', '1', '1'], ['X', 'X', 'X', 'X', 'X'])

# results:
# [0.906494140625, 0.9617919921875, 0.9691162109375, 0.9549560546875, 0.96435546875]
# [0.916748046875, 0.9539794921875, 0.966796875, 0.9541015625, 0.965576171875]
# [0.9932861328125, 0.9881591796875, 0.9942626953125, 0.9920654296875, 0.98876953125]
# [0.9949951171875, 0.9918212890625, 0.9842529296875, 0.9892578125, 0.992919921875]