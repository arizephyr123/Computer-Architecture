# save the address to jump to
00000100 # SAVE
0 # R0
00001000 # address to jump to

# print 99
00000011 # PRINT_NUM
01000011
01100011 # 99
# call our subroutine to print Tim
01011001 # CALL
0 # R0

# halt
00000010 # HALT

# subroutine
00000001  # PRINT_TIM
00000001  # PRINT_TIM
00000001  # RET